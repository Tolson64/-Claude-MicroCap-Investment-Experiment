"""
GitHub Actions 自动数据更新脚本
每日自动运行，更新投资组合数据并记录到CSV文件
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
import pandas as pd

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from daily_update import main as daily_update_main
    from system.market_data_fetcher import MarketDataFetcher
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保所有依赖模块存在")
    sys.exit(1)

def get_beijing_time():
    """获取北京时间"""
    beijing_tz = timezone(timedelta(hours=8))
    return datetime.now(beijing_tz)

def check_market_hours():
    """检查是否在交易时间内（美股交易时间考虑）"""
    beijing_time = get_beijing_time()
    # 简化检查：跳过周末
    if beijing_time.weekday() >= 5:  # 周六(5)和周日(6)
        print(f"📅 今天是{['周一','周二','周三','周四','周五','周六','周日'][beijing_time.weekday()]}，跳过更新")
        return False
    return True

def update_readme_timestamp():
    """更新README中的最后更新时间戳"""
    readme_path = project_root / "README.md"
    if not readme_path.exists():
        print("⚠️ README.md文件不存在")
        return
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        beijing_time = get_beijing_time()
        timestamp = beijing_time.strftime("%Y年%m月%d日 %H:%M")
        
        # 查找并替换时间戳行
        import re
        pattern = r'\*最后更新: \d{4}年\d{1,2}月\d{1,2}日.*?\*'
        replacement = f'*最后更新: {timestamp} (自动更新)*'
        
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
        else:
            # 如果找不到现有时间戳，在投资组合表格后添加
            table_pattern = r'(\| TCRX.*?\| \$1\.45 \|)'
            if re.search(table_pattern, content):
                content = re.sub(
                    table_pattern, 
                    r'\1\n\n*最后更新: ' + timestamp + ' (自动更新)*', 
                    content
                )
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ README时间戳更新为: {timestamp}")
        
    except Exception as e:
        print(f"❌ 更新README时间戳失败: {e}")

def update_portfolio_table_in_readme():
    """更新README中的投资组合表格数据"""
    try:
        # 读取最新的投资组合数据
        portfolio_tracker = project_root / "portfolio_tracker.csv"
        if not portfolio_tracker.exists():
            print("⚠️ portfolio_tracker.csv不存在，跳过表格更新")
            return
        
        df = pd.read_csv(portfolio_tracker)
        
        # 计算当前持仓
        from daily_update import calculate_current_holdings
        current_holdings = calculate_current_holdings(df)
        
        if not current_holdings:
            print("ℹ️ 无当前持仓，跳过表格更新")
            return
        
        # 获取当前价格
        tickers = list(current_holdings.keys())
        from daily_update import get_latest_prices
        latest_prices = get_latest_prices(tickers)
        
        # 构建新的表格内容
        table_lines = [
            "| 股票代码 | 公司名称 | 持股数 | 买入价 | 当前状态 | 止损价 |",
            "|---------|----------|--------|--------|----------|--------|"
        ]
        
        company_names = {
            'CADL': 'Candel Therapeutics',
            'COYA': 'Coya Therapeutics', 
            'TCRX': 'TScan Therapeutics'
        }
        
        for ticker, holding in current_holdings.items():
            shares = int(holding['shares'])
            avg_cost = holding['total_cost'] / holding['shares']
            current_price = latest_prices.get(ticker, 0)
            stop_loss = holding.get('stop_loss', 'N/A')
            company_name = company_names.get(ticker, ticker)
            
            # 根据当前价格判断状态
            if current_price > 0:
                if current_price >= avg_cost:
                    status = "🟢 持有"
                else:
                    status = "🟡 持有"
            else:
                status = "🔄 持有"
            
            table_lines.append(
                f"| {ticker} | {company_name} | {shares} | ${avg_cost:.2f} | {status} | ${stop_loss} |"
            )
        
        # 更新README
        readme_path = project_root / "README.md"
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找并替换表格
        import re
        table_pattern = r'\| 股票代码.*?\n.*?\n(?:\|.*?\n)*'
        new_table = '\n'.join(table_lines) + '\n'
        
        content = re.sub(table_pattern, new_table, content)
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ README投资组合表格已更新")
        
    except Exception as e:
        print(f"❌ 更新投资组合表格失败: {e}")

def main():
    """主函数"""
    print("🤖 GitHub Actions 自动更新脚本启动")
    
    beijing_time = get_beijing_time()
    print(f"📅 当前北京时间: {beijing_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查是否需要更新
    if not check_market_hours():
        print("⏸️ 非交易日，跳过更新")
        return
    
    try:
        print("📊 开始更新投资组合数据...")
        
        # 运行每日更新脚本
        daily_update_main()
        print("✅ 投资组合数据更新完成")
        
        # 更新README中的投资组合表格
        update_portfolio_table_in_readme()
        
        # 更新README时间戳
        update_readme_timestamp()
        
        print("🎉 所有数据更新完成！")
        
    except Exception as e:
        print(f"❌ 更新过程中出现错误: {e}")
        raise  # 重新抛出异常，让GitHub Actions知道失败了

if __name__ == "__main__":
    main()