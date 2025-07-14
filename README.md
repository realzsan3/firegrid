# 🔥 FIREGRID · 财务自由提款格子图

> 🚀 赛博朋克风财务自由退休提款可视化模拟器
> 一格代表一年，点亮你的财务自由之路

FIREGRID 结合渐变色格子图直观展示每年资产、提款进度和收益波动，帮助你理性规划退休提款策略，提前掌控财务自由节奏。

---

## 🎯 核心特性

* 📅 **年度格子视图**：人生百年财务一览无余
* 📉 **动态提款**：根据上一年实际收益智能调整提款额
* 🟪 **炫酷赛博朋克视觉**：蓝紫渐变格子，极具科技感
* ⚠️ **风险预警**：资产跌破安全阈值自动提示
* 🔧 **高度自定义**：灵活配置收益率模型、起始资产、年支出目标等
* 🌐 **纯前端展示**：静态页面 + JSON，支持 GitHub Pages 轻松部署

---

## 🛠 功能概览

| 功能        | 说明                                          | 相关参数                                      |
| --------- | ------------------------------------------- | ----------------------------------------- |
| 积累期与退休期模拟 | 自动按年切换阶段，模拟储蓄与提款流程                          | `--saving`、`--rate`、`--k`、`--post_income` |
| 动态提款计算    | 基于上一年收益率调整退休提款，避免熊市多卖牛市少花                   | `--init_return`                           |
| 收益率输入模式   | 支持固定收益、随机正态分布或CSV导入收益率序列                    | `--growth`、`--mu`/`--sigma`、`--csv`       |
| 安全阈值风险预警  | 退休期资产低于目标50%并且进度极低时自动提示风险                   | 代码内固定，可自行调整                               |
| 详细年报输出    | 命令行逐年打印资产、收益、提款及进度                          | —                                         |
| JSON数据导出  | 输出包含年报明细和汇总的 `progress.json`，前端直接读取         | `--json_out`                              |
| CLI交互模式   | 缺少参数时自动进入交互式输入                              | —                                         |
| 参数冲突检查    | 自动禁止无效参数组合，例如 `--csv` 与 `--mu/--sigma` 不能共用 | —                                         |
| 可自定义起始年份  | 方便和前端页面时间轴对齐                                | `--start_year`                            |

---

## 🌐 在线演示

🔗 [https://firegrid.111533.xyz/](https://firegrid.111533.xyz/)

（建议使用 GitHub Pages 或 Cloudflare Pages 部署，实现零成本托管）

---

## 🚀 快速开始

```bash
git clone https://github.com/realzsan3/firegrid
cd firegrid
python financial_life_cycle.py  # 运行模拟，生成 progress.json
python -m http.server 8000      # 启动本地服务，访问 http://localhost:8000
```

---

## 📖 说明

* 资产模拟基于真实收益率序列或自定义参数生成
* 退休提款动态调整，更贴合市场波动
* 前端纯静态，轻量且易于二次开发
* 欢迎贡献和反馈，助力财务自由社区！


# Star History

<a href="https://www.star-history.com/#realzsan3/firegrid&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=realzsan3/firegrid&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=realzsan3/firegrid&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=realzsan3/firegrid&type=Date" />
 </picture>
</a>