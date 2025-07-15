# 🔥 FIREGRID · Cyberpunk Retirement Withdrawal Grid

> 🚀 A cyberpunk-style visual simulator for FIRE (Financial Independence, Retire Early)
> One square = One year. Illuminate your path to financial freedom.

**FIREGRID** uses a colorful grid chart to visualize your yearly asset growth, withdrawal flow, and risk signals — helping you build a sustainable withdrawal plan across your entire financial life cycle.

---

## 🎯 Key Highlights

* 📆 **Annual Grid View**: See your entire financial journey in one glance
* 📈 **Dynamic Withdrawal Strategy**: Adjust withdrawal based on actual market returns
* 💡 **Dual-Phase Simulation**: Accumulation → Retirement modeled seamlessly
* ⚠️ **Multi-Level Risk Alerts**: Auto-detect when assets fall below critical thresholds
* 🎨 **Cyberpunk Aesthetic**: Neon gradients + glowing grid for futuristic vibes
* ⚙️ **Fully Customizable**: Configure savings, income, asset returns, thresholds, and more
* 🌐 **Pure Frontend Deployment**: Works with static HTML + JSON, deployable via GitHub Pages

---

## 🌐 Live Demo

> ![示意图](https://firegrid.111533.xyz/assets/og-image.jpg)

🔗 [live Demo](https://firegrid.111533.xyz)

> Static frontend with fully local JSON data — ideal for free deployment on GitHub Pages or Cloudflare Pages.

---

## 🛠 Feature Overview

| Feature                   | Description                                                   | Parameters                                          |
| ------------------------- | ------------------------------------------------------------- | --------------------------------------------------- |
| ✅ Full Lifecycle Model    | Simulates accumulation and retirement phases                  | `--saving`, `--rate`, `--k`, `--post_income`        |
| ✅ Dynamic Withdrawals     | Withdraw amount adjusts based on previous year's return       | `--init_return`                                     |
| ✅ Flexible Return Modes   | Use fixed rate, normal distribution, or import from CSV       | `--growth`, `--mu`/`--sigma`, `--csv`               |
| ✅ Risk Guardrails         | Alerts when asset level falls below 80% or 60% of FIRE target | Built-in logic (customizable via `--retire_saving`) |
| ✅ Yearly Reports + JSON   | Outputs detailed yearly report and summary as `progress.json` | `--json_out`                                        |
| ✅ Interactive CLI         | Missing parameters? Enters interactive mode automatically     | —                                                   |
| ✅ Argument Conflict Check | Prevents invalid combinations (e.g., `--csv` with `--mu`)     | —                                                   |
| ✅ Custom Start Year       | Aligns simulation with real-world calendar                    | `--start_year`                                      |
---

## 🚀 Quick Start

```bash
git clone https://github.com/realzsan3/firegrid
cd firegrid

# Run simulation and generate progress.json
python financial_life_cycle.py

# Launch local server (open http://localhost:8000)
python -m http.server 8000
```

---

## 🔍 Use Cases

| Scenario                | Description                                                                  |
| ----------------------- | ---------------------------------------------------------------------------- |
| ✅ Post-retirement plan  | Model sustainable long-term withdrawals while avoiding sequence risk         |
| ✅ Temporary "Gap Year"  | Simulate survival without income for a few years during sabbatical/life gaps |
| ✅ FIRE Target Planning  | Reverse-calculate how much you need to retire with your desired lifestyle    |
| ✅ Portfolio Stress Test | Run FIREGRID with actual or simulated returns to test withdrawal viability   |

---

## 🧠 Simulation Logic

FIREGRID simulates your financial journey based on:

* 💼 Accumulating savings during working years
* 🎯 Switching to retirement phase once FIRE asset goal is reached
* 📉 Dynamic withdrawals based on last year's return (with adjustable sensitivity `k`)
* 🛑 Risk guardrails:

  * < 80% → recommend cutback
  * < 60% → pause withdrawals + optional cash injection
* 🧾 Generates a full yearly log and summary exportable as JSON

---

## ⚠️ Limitations

This is a simplified, annualized model suitable for **education, content creation, and light planning**.

To use in production-grade tools or serious financial planning, consider adding:

* 🎲 Monte Carlo simulation + historical backtesting
* 📉 Multi-asset portfolio + inflation modeling
* 🛡️ Dynamic guardrails & scenario planning
* 🧪 Stress-tested parameters based on real-world data

---

## 💬 Inspiration

Inspired by Chinese finance influencer **E大** on Weibo, and enhanced via ChatGPT-assisted modeling.
Original discussions:
📎 [Weibo post 1](https://weibo.com/7519797263/PACdkCFJD)｜[Weibo post 2](https://weibo.com/7519797263/PAJ8UmLb4)

---

## ❤️ For Dreamers of Freedom

> “It’s not that you can’t be free because you’re broke —
> It’s that you haven’t yet built your **path to possibility**.”

If you’ve ever dreamed of **living on your terms**, FIREGRID is your sandbox.

---

## 📈 Star History

<a href="https://www.star-history.com/#realzsan3/firegrid&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=realzsan3/firegrid&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=realzsan3/firegrid&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=realzsan3/firegrid&type=Date" />
 </picture>
</a>

