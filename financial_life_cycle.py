#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
financial_life_cycle.py   v2025‑07‑15‑r2
----------------------------------------
• “储蓄期 ➜ 退休期” 全生命周期模拟
• 自动生成 progress.json（供前端读取）
• 缺少参数时进入交互输入模式
• 退休期 Guardrail（可禁用）：
     - progress < 0.8  → 削减提款 20%
     - progress < 0.6  → 暂停提款并注入 retire_saving
• 新增：warning_level(0/1/2) & warning_msg 字段，前端可直接高亮/提示
"""

import csv
import random
import argparse
import sys
import json
from pathlib import Path
from textwrap import dedent

# ---------- 辅助 ----------

def prompt_float(text: str, default: float | None = None):
    """终端交互读取 float"""
    s = input(f"{text}{f' (默认 {default})' if default is not None else ''}: ").strip()
    return float(s) if s else default


def get_returns(args, years: int):
    """根据参数决定收益率序列"""
    if args.csv:
        rows = list(csv.DictReader(Path(args.csv).open(newline="")))
        if len(rows) < years:
            sys.exit("❌ CSV 行数不足 years / CSV rows fewer than years")
        return [float(r["return"]) for r in rows[:years]]

    if args.mu is not None:  # 随机模式
        return [random.gauss(args.mu, args.sigma or 0) for _ in range(years)]

    return [args.growth] * years  # 固定收益率


# ---------- 核心模拟 ----------

def simulate(args):
    target = args.expense / args.rate
    returns = get_returns(args, args.years)

    assets = args.assets
    phase = "Saving"
    records: list[dict] = []

    start_year = args.start_year
    retire_year = None
    accumulation_years = 0
    safe = True

    total_saved = 0.0
    total_withdrawn = 0.0
    prev_R = args.init_return if args.init_return is not None else args.growth

    print(f"\nGoal: spending {args.expense:,.0f} / rate {args.rate:.2%} → target {target:,.0f}")
    print("\n📊 Simulation begins:")
    print(f"{'Year':<6} {'Return':>7} {'Phase':^10} {'Start Assets':>15} "
          f"{'Cash‑flow':>12} {'End Assets':>15} {'Prog':>6}")

    warning_years: list[int] = []

    # —— Guardrail 固定阈值 ——
    CUT_THRESHOLD = 0.8
    PAUSE_THRESHOLD = 0.6
    CUT_PCT = 0.20  # 削减 20 %

    for yr, R in enumerate(returns, 1):
        start = assets

        # ========== 储蓄期 ==========
        if phase == "Saving":
            flow = args.saving
            assets = start * (1 + R) + flow
            accumulation_years += 1
            total_saved += flow

            if assets >= target:  # 达到目标 → 切换退休期
                phase = "Retirement"
                retire_year = start_year + yr - 1
                flow = 0

        # ========== 退休期 ==========
        else:
            # ① 标准提款：动态调整
            withdraw = start * args.rate + args.k * start * (prev_R - args.rate)
            primary_progress = start / target  # 进度基于年初资产

            # ② Guardrail（阈值调整）
            if not args.no_guardrail:
                if primary_progress < PAUSE_THRESHOLD:  # <0.6 暂停提款
                    withdraw = 0
                    flow = args.retire_saving + args.post_income  # 正现金流
                    action_tag = "PAUSE"
                elif primary_progress < CUT_THRESHOLD:  # 0.6~0.8 削减提款
                    withdraw *= (1 - CUT_PCT)
                    flow = -withdraw + args.post_income
                    action_tag = "CUT  "
                else:  # ≥0.8 正常
                    flow = -withdraw + args.post_income
                    action_tag = "NORM "
            else:  # 未启用 Guardrail
                flow = -withdraw + args.post_income
                action_tag = "NONE "

            assets = start * (1 + R) + flow
            total_withdrawn += withdraw

        # ---------- 进度与警报 ----------
        progress = min(assets / target, 1.0)
        warning_level = 0  # 0=无,1=轻,2=重
        warning_msg = ""
        if phase == "Retirement":
            if progress < PAUSE_THRESHOLD:
                warning_level = 2
                warning_msg = "🚨 严重警告：资产低于 60%，暂停提款并注资 Serious warning: assets below 60%, withdrawals suspended and capital injection"
            elif progress < CUT_THRESHOLD:
                warning_level = 1
                warning_msg = "⚠️  轻度警告：资产低于 80%，建议削减支出 Mild warning: assets below 80%, recommended to cut spending"

        if warning_level:
            print(warning_msg)
            safe = False
            warning_years.append(start_year + yr - 1)

        net_gain = assets - total_saved + total_withdrawn

        # ---------- 记录 ----------
        records.append({
            "year": start_year + yr - 1,
            "assets": round(assets),
            "progress": round(progress, 4),
            "return": round(R, 4),
            "phase": phase,
            "cash_flow": round(flow, 2),
            "warning": bool(warning_level),  # 兼容旧字段
            "warning_level": warning_level,   # 0/1/2
            "warning_msg": warning_msg        # 前端可直接展示
        })

        print(f"{start_year + yr - 1:<6} {R*100:>7.2f}% {phase:^10} "
              f"{start:>15,.0f} {flow:>12,.0f} {assets:>15,.0f} {progress*100:>6.1f}%")

        prev_R = R  # 更新上一年收益率

    # ---------- 汇总 ----------
    retired_flag = retire_year is not None
    if not retired_flag:
        safe = assets >= target

    summary = {
        "start_year": start_year,
        "retire_year": retire_year,
        "accumulation_years": accumulation_years,
        "final_assets": round(assets),
        "total_years": args.years,
        "safe": bool(safe),
        "retired": retired_flag,
        "warning_years": warning_years,
        "total_saved": round(total_saved, 2),
        "total_withdrawn": round(total_withdrawn, 2),
        "net_gain": round(net_gain, 2),
        "target_description": {
            "annual_spending": round(args.expense, 2),
            "withdraw_rate": round(args.rate, 4),
            "target_assets": round(target, 2),
        },
    }

    with open(args.json_out, "w", encoding="utf-8") as f:
        json.dump({"records": records, "summary": summary}, f, ensure_ascii=False, indent=2)
    print(f"\n📤 JSON exported → {Path(args.json_out).resolve()}")


# ---------- 参数解析 ----------

def parse_args():
    
    parser = argparse.ArgumentParser(
        prog="financial_life_cycle.py",
        formatter_class=argparse.RawTextHelpFormatter,
        description=dedent("""\
            💰 Financial Life‑Cycle Simulator / 财富生命周期模拟器
            ---------------------------------------------------
            • Simulate accumulation → retirement with dynamic withdrawals
            • 模拟储蓄 ➜ 退休全过程，动态提款 + 风险护栏 + JSON 导出
            """)
    )
     # -------- 核心参数 --------
    parser.add_argument("-e", "--expense", type=float,
                        help="Annual spending / 目标年支出")
    parser.add_argument("-r", "--rate", type=float,
                        help="Withdrawal rate r (e.g. 0.04 = 4%%) / 提款率")
    parser.add_argument("-a", "--assets", type=float,
                        help="Current total assets / 当前总资产")
    parser.add_argument("-s", "--saving", type=float,
                        help="Annual saving during accumulation / 储蓄期每年储蓄额")
    parser.add_argument("-y", "--years", type=int, default=40,
                        help="Years to simulate (default 40) / 模拟年数（默认40）")

    # -------- Guardrail & Cash --------
    parser.add_argument("--no_guardrail", action="store_true",
                        help="Disable guardrail logic / 关闭退休期护栏机制")
    parser.add_argument("--retire_saving", type=float, default=0,
                        help="Cash injection when progress <60%% / 进度<60%% 时注资")
    parser.add_argument("--post_income", type=float, default=0,
                        help="Side income in retirement / 退休期副业收入")
    parser.add_argument("-k", "--k", type=float, default=0.8,
                        help="Sensitivity coefficient k / 灵敏度系数 k")

    # -------- Return settings --------
    parser.add_argument("-g", "--growth", type=float, default=0.07,
                        help="Fixed annual return g / 固定年化收益率 g")
    parser.add_argument("--csv", help="CSV file with yearly returns / CSV 收益率文件")
    parser.add_argument("--mu", type=float,
                        help="Mean μ for normal returns / 正态收益均值 μ")
    parser.add_argument("--sigma", type=float,
                        help="Std σ for normal returns / 正态收益标准差 σ")

    # -------- Others --------
    parser.add_argument("--json_out", default="progress.json",
                        help="Output JSON filename / 输出 JSON 文件名")
    parser.add_argument("--start_year", type=int, default=2025,
                        help="Start year of simulation / 模拟起始年份")
    parser.add_argument("--init_return", type=float,
                        help="Previous year's return / 上一年收益率")
    # argparse 自动生成 -h/--help

    args = parser.parse_args()

    # ---- 交互模式 ----
    if None in (args.expense, args.rate, args.assets, args.saving):
        print("\n=== 交互模式 Interactive Mode ===")
        args.expense = args.expense or prompt_float("目标年支出 Annual spending")
        args.rate = args.rate or prompt_float("目标提款率 Withdrawal rate r", 0.04)
        args.assets = args.assets or prompt_float("当前总资产 Current assets")
        args.saving = args.saving or prompt_float("储蓄期每年储蓄额 Annual saving")
        args.years = int(prompt_float("模拟年数 Years", args.years))
        args.k = prompt_float("灵敏度系数 Adjustment sensitivity for retirement k", args.k)
        args.post_income = prompt_float("退休副业收入 Side income", args.post_income)
        args.retire_saving = prompt_float("进度<60% 注资 Retire saving", args.retire_saving)
        mode = input("收益率模式 固定/随机/CSV [f/r/c] Return mode: Fixed / Random / CSV, default f: ").lower() or "f"
        if mode == "r":
            args.mu = prompt_float("收益率均值 Average annual return μ", 0.07)
            args.sigma = prompt_float("收益率标准差 Return volatility σ", 0.15)
        elif mode == "c":
            args.csv = input("CSV 文件路径 CSV path: ").strip()
        else:
            args.growth = prompt_float("固定年收益率 Fixed annual return g", args.growth)
        args.init_return = prompt_float("上一年收益率 Initial return", args.init_return or args.growth)

    # ---- 参数冲突校验 ----
    if args.csv and args.mu is not None:
        sys.exit("❌ --csv conflicts with --mu/--sigma")

    return args


if __name__ == "__main__":
    simulate(parse_args())
