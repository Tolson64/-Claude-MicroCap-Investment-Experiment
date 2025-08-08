# Experiment Workflow Checklist (v2 - Automated)

This document outlines the daily and weekly tasks for the Claude Micro-Cap Investment Experiment. This version incorporates the `prepare_prompt_data.py` script to automate data preparation for AI analysis.

---

## 每日工作清单 (每个交易日)

**目标**: 监控现有持仓，获取Claude的日常建议，并更新当日的投资组合表现。

### 步骤 1: 准备AI提示词数据 (收盘后)
- **操作**: 打开您的命令行终端，运行以下命令：
  ```bash
  python prepare_prompt_data.py --mode daily
  ```
- **结果**: 脚本会自动读取 `daily_performance_log.csv` 的最新数据，并将其格式化后保存在 `daily_prompt_data.txt` 文件中。同时，它也会在屏幕上显示这些数据。

### 步骤 2: 执行每日AI分析 (收盘后)
- **模型**: `Claude Sonnet 4`。
- **提示词**: 使用 `prompts/PROMPT_TEMPLATES.md` 中的 `DAILY_PROMPT_v1.0` 模板。
- **操作**: 打开 `daily_prompt_data.txt` 文件，将其中的全部内容复制并粘贴到提示词模板中。
- **目标**: 获取Claude对当前持仓的明确建议（例如“HOLD”或“SELL”）。

### 步骤 3: 决策与交易记录 (如果需要)
- 根据Claude的建议，由您自己做出最终决策。
- 如果决定**卖出**某支股票，并在第二天开盘时完成了交易，您需要**手动**在 `portfolio_tracker.csv` 文件中**新加一行**来记录这笔卖出操作。
  - *卖出示例*: `2025-08-06,TCRX,SELL,20,1.95,N/A`

### 步骤 4: 更新每日业绩 (收盘后)
- **这是每天的最后一个动作。**
- **操作**: 在命令行终端，运行以下命令：
  ```bash
  python daily_update.py
  ```
- **结果**: 脚本会自动读取 `portfolio_tracker.csv`，获取最新价格，并将当天的最终业绩**追加**到 `daily_performance_log.csv` 的末尾。

---

## 周日工作清单 (每周一次的深度分析)

**目标**: 对投资组合进行全面复盘，寻找新的投资机会，并为下一周的交易做好计划。

### 步骤 1: 准备AI提示词数据
- **操作**: 和日常工作一样，运行以下命令：
  ```bash
  python prepare_prompt_data.py --mode daily
  ```
- **结果**: 最新的投资组合数据会被保存在 `daily_prompt_data.txt` 中。

### 步骤 2: 执行周度深度AI分析
- **模型**: `Claude Opus 4` 并**开启深度研究功能**。
- **提示词**: 使用 `prompts/PROMPT_TEMPLATES.md` 中的 `WEEKLY_RESEARCH_v1.0` 模板。
- **操作**: 将 `daily_prompt_data.txt` 的内容粘贴到提示词模板中。
- **目标**: 获得深入分析，并发现潜在的**新投资机会**。

### 步骤 3: 验证新股票 (如果需要)
- 如果Claude建议了新的投资标的，使用 `validate` 模式来快速检查它们是否符合标准。
- **操作**: 运行命令，将 `TICKER1 TICKER2` 替换为真实的股票代码：
  ```bash
  python prepare_prompt_data.py --mode validate --tickers TICKER1 TICKER2
  ```

### 步骤 4: 决策与交易记录 (如果需要)
- 如果您决定**买入**一支新股票：
- 在下周一开盘后，执行交易。
- 交易完成后，**手动**在 `portfolio_tracker.csv` 文件中**新加一行**来记录这笔新的买入操作。
  - *买入示例*: `2025-08-11,NEW_STOCK,BUY,50,2.50,2.10`