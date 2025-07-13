# 🔥 FIREGRID · 财务自由提款格子图

> 🚀 Cyberpunk-style Retirement Withdrawal Visualizer  
> 一格一年，点亮你的财务自由之路

FIREGRID 是一款以【财务自由 & 提前退休】为核心理念的 **视觉化模拟器**，结合渐变色彩格子图展示你的每一年提款进度、资产变化、收益率波动等，让你能**理性规划每年花多少钱才安全**。

---

## 🎯 核心特性 Features

- 📅 一格代表一年：人生100年尽收眼底
- 📉 动态提款：根据每年收益动态调整提款额
- 🟪 可视化展示：蓝紫赛博格子图，一眼看清资产趋势
- ⚠️ 低于阈值提醒：遇到资产缩水会提示风险
- 🔧 可自定义：收益率、初始资产、支出目标都可配置
- 🌐 纯静态 HTML/CSS/JS，无需后端，支持 GitHub Pages 部署

---

## 🌐 在线体验 Live Demo

🔗 https://firegrid.111533.xyz/
 
（建议你部署 GitHub Pages 或 cloudflare-page 体验地址）

---

## 🚀 快速开始使用（本地运行）

```bash
git clone https://github.com/realzsan3/firegrid
cd firegrid
python financial_life_cycle.py  # 生成 progress.json 数据
python -m http.server          # 本地访问 http://localhost:8000
