#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
financial_life_cycle.py   v2025‑07‑14
-------------------------------------
• “积累期 ➜ 退休期” 全生命周期模拟
• 自动生成 progress.json（供前端读取）
• 缺少参数时进入交互输入模式
• 每年结果打印 + 退休期资产警告
• 退休期提款额基于“上一年实际收益率”
  - 避免熊市多卖、牛市少花的问题
"""

import csv, random, argparse, sys, json
from pathlib import Path


def prompt_float(text, default=None):
    s = input(f"{text}{f' (默认 {default})' if default is not None else ''}: ").strip()
    return float(s) if s else default


def get_returns(args, years):
    if args.csv:
        rows = list(csv.DictReader(Path(args.csv).open(newline="")))
        if len(rows) < years:
            sys.exit("❌ CSV 行数不足 years")
        return [float(r["return"]) for r in rows[:years]]
    if args.mu is not None:
        return [random.gauss(args.mu, args.sigma or 0) for _ in range(years)]
    return [args.growth] * years


def simulate(args):
    target = args.expense / args.rate
    returns = get_returns(args, args.years)
    assets = args.assets
    phase = "积累"
    records = []

    start_year = args.start_year
    retire_year = None
    accumulation_years = 0
    safe = True

    total_saved = 0
    total_withdrawn = 0

    # 新增：上一年收益率，默认等于固定收益或 0
    prev_R = args.init_return if args.init_return is not None else args.growth

    target_description = {
        "annual_spending": round(args.expense, 2),
        "withdraw_rate": round(args.rate, 4),
        "target_assets": round(target, 2),
}
    
    print("\n" + f"目标：年支出 {args.expense:,.0f} / 提款率 {args.rate:.2%} = 自由所需资产 {target:,.0f}")
    print("\n📊 模拟开始：")
    print(f"{'年':<6} {'收益率':>7} {'阶段':^4} {'年初资产':>15} {'现金流':>12} {'年末资产':>15} {'进度':>6}")

    warning_years = []

    for yr, R in enumerate(returns, 1):
        start = assets

        if phase == "积累":
            flow = args.saving
            assets = start * (1 + R) + flow
            accumulation_years += 1
            total_saved += flow
            if assets >= target:
                phase, flow = "退休", 0
                retire_year = start_year + yr - 1
        else:  # 退休期
            # ────────── 核心改动：基于上一年收益率 prev_R 计算提款 ──────────
            withdraw = start * args.rate + args.k * start * (prev_R - args.rate)
            flow = -withdraw + args.post_income
            assets = start * (1 + R) + flow
            total_withdrawn += withdraw

        progress = min(assets / target, 1.0)

        warning = False
        if phase == "退休" and progress < 1e-3 and assets < target * 0.5:
            print("⚠️  资产跌破安全阈值，请谨慎！")
            safe = False
            warning = True
            warning_years.append(start_year + yr - 1)

        net_gain = assets - total_saved + total_withdrawn  # 净收益计算

        records.append(
            {
                "year": start_year + yr - 1,
                "assets": round(assets),
                "progress": round(progress, 4),
                "return": round(R, 4),
                "phase": phase,
                "cash_flow": round(flow, 2),
                "warning": warning,
            }
        )

        print(
            f"{start_year + yr - 1:<6} {R*100:>7.2f}% {phase:^4} {start:>15,.0f} {flow:>12,.0f} {assets:>15,.0f} {progress*100:>6.1f}%"
        )

        # —— 关键：循环尾部更新上一年收益率 ——
        prev_R = R

    # ---- 收尾：确定是否已退休 & 生成 summary ----
    retired_flag = retire_year is not None

    if not retired_flag:
        retire_year = None
        safe = assets >= target  # 未退休时重新评估安全性

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
        "target_description": target_description,
    }

    export_data = {"records": records, "summary": summary}

    with open(args.json_out, "w", encoding="utf-8") as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    print(f"\n📤 已导出 JSON 数据：{Path(args.json_out).resolve()}")


# ────────── 解析参数/进入交互 ──────────

def parse_args():
    p = argparse.ArgumentParser(description="财富生命周期模拟 + JSON 导出", add_help=False)
    p.add_argument("-e", "--expense", type=float, help="目标年支出")
    p.add_argument("-r", "--rate", type=float, help="目标提款率 r")
    p.add_argument("-a", "--assets", type=float, help="当前总资产")
    p.add_argument("-s", "--saving", type=float, help="积累期每年储蓄额")
    p.add_argument("-y", "--years", type=int, default=40, help="模拟年数 (默认40)")
    p.add_argument("-k", "--k", type=float, default=0.8, help="灵敏度系数 k,动态调整退休期提款额")
    p.add_argument("--post_income", type=float, default=0, help="退休期年副业收入")
    p.add_argument("-g", "--growth", type=float, default=0.07, help="固定收益率")
    p.add_argument("--csv", help="CSV 数据文件路径")
    p.add_argument("--mu", type=float, help="收益率均值 μ（随机）")
    p.add_argument("--sigma", type=float, help="收益率标准差 σ（随机）")
    p.add_argument("--json_out", default="progress.json", help="导出 JSON 文件名")
    p.add_argument("--start_year", type=int, default=2025, help="模拟起始年份")
    # —— 新增：初始化上一年收益率 ——
    p.add_argument(
        "--init_return",
        type=float,
        help="第一年退休前用于计算提款的上一年收益率 (默认同 g)",
    )
    p.add_argument("-h", "--help", action="help")
    args = p.parse_args()

    need_prompt = None in (args.expense, args.rate, args.assets, args.saving)
    if need_prompt:
        print("\n=== 交互模式 ===")
        args.expense = args.expense or prompt_float("目标年支出 (元)")
        args.rate = args.rate or prompt_float("目标提款率 r (如 0.04)")
        args.assets = args.assets or prompt_float("当前总资产 (元)")
        args.saving = args.saving or prompt_float("积累期每年储蓄额 (元)")
        args.years = int(prompt_float("模拟年数", args.years))
        args.k = prompt_float("灵敏度系数 k", args.k)
        args.post_income = prompt_float("退休后每年副业收入", args.post_income)
        mode = input("收益率模式 固定 / 随机 / CSV [f/r/c] (默认 f): ").lower() or "f"
        if mode == "r":
            args.mu = prompt_float("收益率均值 μ", 0.07)
            args.sigma = prompt_float("收益率标准差 σ", 0.15)
        elif mode == "c":
            args.csv = input("CSV 文件路径: ").strip()
        else:
            args.growth = prompt_float("固定年收益率 g", args.growth)
        args.init_return = prompt_float("上一年收益率 (初始)", args.init_return if args.init_return is not None else args.growth)

    if args.csv and args.mu is not None:
        sys.exit("❌ --csv 与 --mu/--sigma 不能同时使用")
    return args

# ────────── 入口点 ──────────

if __name__ == "__main__":
    simulate(parse_args())
