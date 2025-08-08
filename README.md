# 🚀 Claude微型股投资实验 | Claude Micro-Cap Investment Experiment

> **实时AI投资实验** - 用100美元验证Claude AI的投资决策能力

[![实验状态](https://img.shields.io/badge/状态-进行中-green.svg)]()
[![起始资金](https://img.shields.io/badge/起始资金-$100-blue.svg)]()
[![实验期](https://img.shields.io/badge/实验期-2025.8--2025.12-orange.svg)]()
[![AI模型](https://img.shields.io/badge/AI模型-Claude_Sonnet_4-purple.svg)]()

**🔥 这是一个真实资金的AI投资实验** - Claude AI管理真实的微型股投资组合

## 🎯 实验核心问题

每天都能看到AI选股的广告，但大多数都是垃圾。这让我开始思考一个有趣的问题：

**强大的大型语言模型如Claude能否利用实时数据真正产生Alpha收益？**

用100美元真金白银来验证这个假设。

## 📊 当前投资组合表现

| 股票代码 | 公司名称 | 持股数 | 买入价 | 当前状态 | 止损价 |
|---------|----------|--------|--------|----------|--------|
| CADL | Candel Therapeutics | 3 | $6.34 | 🟢 持有 | $5.75 |
| COYA | Coya Therapeutics | 4 | $6.50 | 🟢 持有 | $5.89 |
| TCRX | TScan Therapeutics | 5 | $1.75 | 🟢 持有 | $1.45 |

*最后更新: 2025年8月8日*

## ⚡ 每日交易流程

- 📈 **数据输入**：提供投资组合的实时交易数据
- 🛡️ **风险控制**：严格执行止损规则（15-20%）
- 🧠 **日常决策**：Claude Sonnet 4处理日常投资组合管理
- 🔬 **深度分析**：每周使用Claude Opus 4 + Research进行深度重新评估
- 📊 **透明报告**：性能数据每周在博客发布 [SubStack链接](https://nathanbsmith729.substack.com)

## 📚 项目文档

### 📋 提示词模板
- [标准化提示词](./prompts/PROMPT_TEMPLATES.md) - 所有AI决策的标准化模板
- [工作流检查表](./WORKFLOW_CHECKLIST.md) - 完整的操作流程

### 📈 实时数据
- [投资组合跟踪](./portfolio_tracker.csv) - 每日交易记录
- [绩效日志](./daily_performance_log.csv) - 历史表现数据

### 🔧 技术组件
- [数据获取脚本](./prepare_prompt_data.py) - 自动化市场数据获取
- [投资组合更新](./daily_update.py) - 每日组合更新
- [验证引擎](./system/validation_engine.py) - 数据完整性检查

### 📊 分析报告
- [每日预测报告](./报告合集/) - Claude的投资分析和预测
- [小红书文案](./小红书文案/) - 社交媒体内容和可视化报告
  
## Claude's Initial Investment Strategy (2025-08-05)

Based on a deep analysis of the micro-cap biotech sector, Claude has formulated a high-risk, high-reward investment strategy for the 4-month period.

**Full detailed analysis available here:** [2025-08-05_claude_initial_strategy.md](./reports/2025-08-05_claude_initial_strategy.md)

### Core Thesis
The investment is built on three pillars:
1.  **Valuation & Policy:** The biotech sector is at a historical valuation low, with an expected favorable shift in FDA policy and interest rates.
2.  **Catalyst Density:** The 4-month investment window is packed with critical catalysts like FDA decisions and clinical trial data releases.
3.  **Selective Strategy:** The portfolio focuses on financially stable companies with clear, differentiated pipelines, avoiding purely speculative plays.

### Final Portfolio

| Ticker | Company Name        | Shares | Entry Price | Investment Value | Stop Loss |
|--------|---------------------|--------|-------------|------------------|-----------|
| CADL   | Candel Therapeutics | 5      | $6.28       | $31.40           | $5.30     |
| COYA   | Coya Therapeutics   | 4      | $6.10       | $24.40           | $4.90     |
| TCRX   | TScan Therapeutics  | 20     | $1.67       | $33.40           | $1.35     |

### Trading Strategy
- **Phased Entry:** Initial positions in CADL and COYA, followed by PMN and TCRX on technical pullbacks.
- **Strict Stop-Loss:** A firm 15-20% stop-loss is set for each individual stock.
- **Dynamic Adjustments:** Positions will be managed based on catalyst outcomes and market reactions.

# Performance Example (8/5 – 12/5)

---

![Week 4 Performance](%288-5%20-%2012-5%29%20Results.png)

---
- Currently stomping on the Russell 2K.

# Features of This Repo
Live trading scripts — Used to evaluate prices and update holdings daily

LLM-powered decision engine — Claude picks the trades

Performance tracking — CSVs with daily PnL, total equity, and trade history

Visualization tools — Matplotlib graphs comparing Claude vs Index

Logs & trade data — Auto-saved logs for transparency

# Why This Matters
AI is being hyped across every industry, but can it really manage money without guidance?

This project is an attempt to find out, with transparency, data, and a real budget.

# Tech Stack
Basic Python 

Pandas + yFinance for data & logic

Matplotlib for visualizations

Claude Sonnet 4 for daily decisions, Claude Opus 4 with Research for weekly deep analysis

# Follow Along
The experiment runs August 2025 to December 2025.
Every trading day I will update the portfolio CSV file.
If you feel inspired to do something similar, feel free to use this as a blueprint.

Updates are posted weekly on my blog — more coming soon!

One final shameless plug: (https://substack.com/@nathanbsmith?utm_source=edit-profile-page)

# 🚀 快速开始指南

## 实验启动流程

### 第0天：初始投资组合构建
1. **准备市场数据**：
   - 获取当日S&P 500和Russell 2000价格数据
   - 记录当前日期
   
2. **使用初始构建提示词**：
   - 打开 `prompts/PROMPT_TEMPLATES.md`
   - 使用 `INITIAL_PORTFOLIO_v1.1` 提示词
   - **重要**：在Claude中开启深度研究功能 ✅
   - 将市场数据插入提示词模板中的相应位置

3. **执行投资组合构建**：
   - 在Claude Opus 4中运行完整提示词
   - 获得包含具体股票、价格、股数的投资建议
   - 记录投资理念总结（供后续参考）

4. **风险验证**：
   - 使用 `RISK_CHECK_v1.0` 验证每个投资建议
   - 确保符合35%集中度限制和其他风险参数

5. **执行交易**：
   - 根据建议执行实际交易
   - 使用 `TRADE_EXECUTION_v1.0` 确认交易细节
   - 更新投资组合记录

### 第1-6天：日常管理
- 使用 `DAILY_PROMPT_v1.0`（Claude Sonnet 4）
- 插入当日投资组合数据表格
- 监控止损线和风险状况
- 执行必要的交易调整

### 第7天：周度深度分析
- 使用 `WEEKLY_RESEARCH_v1.0`（Claude Opus 4 + Research）
- 全面重新评估投资组合
- 寻找新的投资机会
- 更新投资理念总结

## 数据获取和准备

### 安装依赖
```bash
pip install -r requirements.txt
```

### 快速系统测试
```bash
python tmp_rovodev_test_system.py
```

### 数据获取脚本使用

#### 1. 准备初始投资组合数据
```bash
python prepare_prompt_data.py --mode initial
```
- 生成 `initial_portfolio_data.txt`
- 包含当日S&P 500和Russell 2000数据
- 可直接复制到 `INITIAL_PORTFOLIO_v1.1` 提示词中

#### 2. 准备日常评估数据
```bash
python prepare_prompt_data.py --mode daily
```
- 生成 `daily_portfolio_data.txt`
- 包含投资组合当前价值和盈亏
- 可直接复制到 `DAILY_PROMPT_v1.0` 提示词中

#### 3. 验证股票是否符合微型股标准
```bash
python prepare_prompt_data.py --mode validate --tickers ABEO IINN ACTU
```
- 验证市值是否低于3亿美元
- 检查流动性和基本信息
- 确保符合投资标准

### 必需的市场数据（自动获取）：
- ✅ 实时股票价格（yfinance）
- ✅ 日交易量和流动性
- ✅ 市值验证（<$300M）
- ✅ 主要指数表现（S&P 500, Russell 2000）
- ✅ 52周高低点
- ✅ 公司基本信息

### 投资组合数据格式：
```
| 股票代码 | 持股数量 | 买入价格 | 当前价格 | 市值 | 盈亏 | 盈亏% | 止损价格 |
|---------|---------|---------|---------|------|------|-------|---------|
| ABEO    | 4       | $5.77   | $6.25   | $25  | +$1.92| +8.3% | $4.90   |
```

## 提示词使用说明

### 关键原则：
1. **严格按模板执行**：不得随意修改核心结构
2. **开启深度研究**：初始构建和周度分析必须使用Research功能
3. **数据完整性**：确保所有[插入]部分都有实际数据
4. **版本控制**：使用最新版本的提示词模板

### 模型选择：
- **Claude Opus 4 + Research**：初始构建、周度深度分析
- **Claude Sonnet 4**：日常评估、风险检查、交易确认

---

# Key Improvements from Previous ChatGPT Experiment

This Claude experiment addresses critical issues identified in the original ChatGPT micro-cap experiment:

## 🎯 Consistency Improvements
- **100% Standardized Prompts**: All prompts are pre-written and version-controlled to ensure complete consistency
- **Prompt Templates**: Structured templates for daily, weekly, and trade execution prompts
- **Decision Framework**: Clear decision-making criteria and risk parameters

## 🔒 System Integrity 
- **Airtight Simulation Engine**: Comprehensive validation before any trade logging
- **Automated Verification**: Cross-checking all calculations and data integrity
- **Audit Trail**: Complete transparency in all decision-making processes

## 🧠 Enhanced AI Capabilities
- **Claude Sonnet 4**: Fast, efficient model for daily portfolio decisions and risk management
- **Claude Opus 4**: Advanced model reserved for weekly deep research and comprehensive analysis
- **Research Functionality**: Deep research capabilities for comprehensive market analysis
- **Dual-Model Strategy**: Optimized cost-efficiency while maintaining analytical depth

## 🚀 快速开始

### 环境配置
```bash
# 克隆项目
git clone https://github.com/YOUR_USERNAME/Claude-MicroCap-Investment-Experiment.git
cd Claude-MicroCap-Investment-Experiment

# 安装依赖
pip install -r requirements.txt

# 运行数据获取测试
python prepare_prompt_data.py --mode validate --tickers CADL COYA TCRX
```

### 💻 技术栈
- **Python 3.8+** - 主要编程语言
- **yfinance** - 实时股票数据获取
- **pandas** - 数据处理和分析
- **matplotlib** - 数据可视化
- **Claude AI** - 投资决策引擎
  - Sonnet 4: 日常决策
  - Opus 4 + Research: 深度分析

### 🤝 参与贡献

发现问题或有改进建议？
- 📧 联系邮箱: nathanbsmith.business@gmail.com
- 🐛 提交Issue: [GitHub Issues](../../issues)
- 🔄 提交PR: [Pull Requests](../../pulls)

---

⚠️ **风险提示**: 本项目仅用于教育和研究目的，不构成投资建议。投资有风险，入市需谨慎。