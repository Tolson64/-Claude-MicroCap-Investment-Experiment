"""
提示词数据准备脚本
用于获取市场数据并格式化为提示词模板所需的格式
"""

import sys
from pathlib import Path
import pandas as pd
from system.market_data_fetcher import MarketDataFetcher
import argparse

# (prepare_initial_portfolio_data 和 validate_stock_list 函数保持不变，此处省略)

def prepare_initial_portfolio_data():
    """准备初始投资组合构建提示词所需的数据"""
    print("🚀 准备初始投资组合构建数据...")
    fetcher = MarketDataFetcher()
    print("📊 获取主要指数数据...")
    formatted_data = fetcher.format_for_prompt()
    print("\n" + "="*60)
    print("📋 以下数据可直接插入 INITIAL_PORTFOLIO_v1.1 提示词:")
    print("="*60)
    print(formatted_data)
    print("="*60)
    output_file = Path("initial_portfolio_data.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(formatted_data)
    print(f"✅ 数据已保存到: {output_file}")
    return formatted_data

def prepare_daily_portfolio_data(log_file: str = "daily_performance_log.csv"):
    """准备日常投资组合评估提示词所需的数据，从每日日志中读取最新持仓。"""
    print("📅 准备日常投资组合评估数据...")
    
    log_path = Path(log_file)
    
    if not log_path.exists():
        print(f"❌ 错误: 日志文件 {log_path} 不存在。")
        print("请先运行 daily_update.py 生成至少一天的日志。")
        return None

    print(f"📂 从 {log_path} 读取最新投资组合...")
    try:
        df = pd.read_csv(log_path, encoding='utf-8-sig')
        if df.empty:
            print("⚠️ 日志文件为空，无法准备数据。")
            return None

        # 找到最近一个交易日的数据
        latest_date = df['Date'].max()
        latest_df = df[df['Date'] == latest_date].copy()
        
        # 提取持仓数据 (排除TOTAL行)
        holdings_df = latest_df[latest_df['Ticker'] != 'TOTAL']
        # 提取总结数据 (TOTAL行)
        summary_row = latest_df[latest_df['Ticker'] == 'TOTAL'].iloc[0]

    except Exception as e:
        print(f"❌ 读取或处理日志文件时出错: {e}")
        return None

    # 将DataFrame转换为Markdown表格，用于提示词
    prompt_table = holdings_df.to_markdown(index=False, floatfmt=".2f")
    
    print("\n" + "="*60)
    print("📋 以下数据可直接插入 DAILY_PROMPT_v1.0 或 WEEKLY_RESEARCH_v1.0 提示词:")
    print("="*60)
    print(prompt_table)
    print(f"\n## 投资组合总结:")
    print(f"   - 总市值: ${summary_row['Total Value']:.2f}")
    print(f"   - 现金余额: ${summary_row['Cash Balance']:.2f}")
    print(f"   - 总权益: ${summary_row['Total Equity']:.2f}")
    print("="*60)
    
    # 保存提示词文本文件
    output_file = Path("daily_prompt_data.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# {latest_date} 投资组合数据\n\n")
        f.write(prompt_table)
        f.write(f"\n## 投资组合总结:\n")
        f.write(f"   - 总市值: ${summary_row['Total Value']:.2f}\n")
        f.write(f"   - 现金余额: ${summary_row['Cash Balance']:.2f}\n")
        f.write(f"   - 总权益: ${summary_row['Total Equity']:.2f}\n")
    
    print(f"✅ 提示词数据已保存到: {output_file}")
    return prompt_table

def validate_stock_list(tickers: list):
    """验证股票列表是否符合微型股标准"""
    print(f"🔍 验证股票列表: {', '.join(tickers)}")
    fetcher = MarketDataFetcher()
    print("\n" + "="*60)
    print("📊 股票验证结果:")
    print("="*60)
    valid_stocks = []
    invalid_stocks = []
    for ticker in tickers:
        print(f"\n检查 {ticker}...")
        is_valid, message = fetcher.validate_micro_cap(ticker)
        if is_valid:
            valid_stocks.append(ticker)
            print(f"✅ {message}")
        else:
            invalid_stocks.append(ticker)
            print(f"❌ {message}")
    print("\n" + "="*60)
    print("📋 验证总结:")
    print(f"✅ 符合标准: {', '.join(valid_stocks) if valid_stocks else '无'}")
    print(f"❌ 不符合标准: {', '.join(invalid_stocks) if invalid_stocks else '无'}")
    print("="*60)
    return valid_stocks, invalid_stocks

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="准备Claude投资实验的提示词数据")
    parser.add_argument(
        "--mode", 
        choices=["initial", "daily", "validate"],
        default="daily",
        help="运行模式: initial=初始投资组合, daily=日常评估, validate=验证股票"
    )
    parser.add_argument(
        "--tickers",
        nargs="+",
        help="要验证的股票代码列表（用于validate模式）"
    )
    
    args = parser.parse_args()
    
    if args.mode == "initial":
        prepare_initial_portfolio_data()
    elif args.mode == "daily":
        prepare_daily_portfolio_data()
    elif args.mode == "validate":
        if not args.tickers:
            print("❌ validate模式需要提供股票代码列表")
            return
        validate_stock_list(args.tickers)

if __name__ == "__main__":
    sys.exit(main())
