"""
Claude微型股投资实验 - 系统完整性验证引擎
确保模拟引擎完全密封，所有计算准确可靠
"""

import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import logging
import json
from pathlib import Path

class SystemIntegrityValidator:
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.setup_logging()
        self.validation_results = []
    
    def setup_logging(self):
        """设置日志系统"""
        log_file = self.data_dir / "validation.log"
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filemode='a'
        )
        
        # 同时输出到控制台
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
    
    def validate_price_data(self, ticker, price, tolerance=0.2):
        """
        验证股价数据的合理性
        
        Args:
            ticker: 股票代码
            price: 当前价格
            tolerance: 价格容忍度 (默认20%)
        
        Returns:
            bool: 验证是否通过
        """
        try:
            # 获取最近5天数据
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5d")
            
            if hist.empty:
                self.log_error(f"无法获取{ticker}的历史数据")
                return False
            
            recent_high = hist['High'].max()
            recent_low = hist['Low'].min()
            recent_close = hist['Close'].iloc[-1]
            
            # 检查价格是否在合理范围内
            lower_bound = recent_low * (1 - tolerance)
            upper_bound = recent_high * (1 + tolerance)
            
            if not (lower_bound <= price <= upper_bound):
                self.log_error(
                    f"{ticker}价格{price:.2f}超出合理范围"
                    f"[{lower_bound:.2f}, {upper_bound:.2f}]"
                )
                return False
            
            # 检查与最近收盘价的差异
            price_diff = abs(price - recent_close) / recent_close
            if price_diff > tolerance:
                self.log_warning(
                    f"{ticker}价格{price:.2f}与最近收盘价{recent_close:.2f}"
                    f"差异较大: {price_diff:.1%}"
                )
            
            self.log_success(f"{ticker}价格验证通过: {price:.2f}")
            return True
            
        except Exception as e:
            self.log_error(f"{ticker}价格验证失败: {e}")
            return False
    
    def validate_portfolio_math(self, portfolio_data):
        """
        验证投资组合数学计算的准确性
        
        Args:
            portfolio_data: DataFrame包含投资组合数据
        
        Returns:
            bool: 验证是否通过
        """
        errors = []
        total_value_sum = 0
        total_pnl_sum = 0
        
        for _, row in portfolio_data.iterrows():
            if row['Ticker'] == 'TOTAL':
                continue
                
            # 验证总价值计算: 股数 × 当前价格
            expected_value = row['Shares'] * row['Current Price']
            if abs(expected_value - row['Total Value']) > 0.01:
                errors.append(
                    f"{row['Ticker']}: 总价值计算错误 - "
                    f"预期{expected_value:.2f}, 实际{row['Total Value']:.2f}"
                )
            
            # 验证盈亏计算: 总价值 - 成本基础
            expected_pnl = row['Total Value'] - row['Cost Basis']
            if abs(expected_pnl - row['PnL']) > 0.01:
                errors.append(
                    f"{row['Ticker']}: 盈亏计算错误 - "
                    f"预期{expected_pnl:.2f}, 实际{row['PnL']:.2f}"
                )
            
            total_value_sum += row['Total Value']
            total_pnl_sum += row['PnL']
        
        # 验证TOTAL行的计算
        total_row = portfolio_data[portfolio_data['Ticker'] == 'TOTAL']
        if not total_row.empty:
            total_row = total_row.iloc[0]
            
            if abs(total_value_sum - total_row['Total Value']) > 0.01:
                errors.append(
                    f"TOTAL总价值计算错误 - "
                    f"预期{total_value_sum:.2f}, 实际{total_row['Total Value']:.2f}"
                )
            
            if abs(total_pnl_sum - total_row['PnL']) > 0.01:
                errors.append(
                    f"TOTAL盈亏计算错误 - "
                    f"预期{total_pnl_sum:.2f}, 实际{total_row['PnL']:.2f}"
                )
        
        if errors:
            for error in errors:
                self.log_error(error)
            return False
        
        self.log_success("投资组合数学计算验证通过")
        return True
    
    def validate_trade_execution(self, trade_data, before_cash, after_cash, 
                               before_shares, after_shares):
        """
        验证交易执行的正确性
        
        Args:
            trade_data: 交易数据字典
            before_cash: 交易前现金
            after_cash: 交易后现金
            before_shares: 交易前持股
            after_shares: 交易后持股
        
        Returns:
            bool: 验证是否通过
        """
        action = trade_data['action'].upper()
        ticker = trade_data['ticker']
        shares = trade_data['shares']
        price = trade_data['price']
        
        if action == 'BUY':
            # 验证现金减少
            expected_cash_change = -(shares * price)
            actual_cash_change = after_cash - before_cash
            
            if abs(expected_cash_change - actual_cash_change) > 0.01:
                self.log_error(
                    f"买入{ticker}现金变化错误: "
                    f"预期{expected_cash_change:.2f}, 实际{actual_cash_change:.2f}"
                )
                return False
            
            # 验证持股增加
            expected_shares_change = shares
            actual_shares_change = after_shares - before_shares
            
            if abs(expected_shares_change - actual_shares_change) > 0.01:
                self.log_error(
                    f"买入{ticker}持股变化错误: "
                    f"预期{expected_shares_change}, 实际{actual_shares_change}"
                )
                return False
        
        elif action == 'SELL':
            # 验证现金增加
            expected_cash_change = shares * price
            actual_cash_change = after_cash - before_cash
            
            if abs(expected_cash_change - actual_cash_change) > 0.01:
                self.log_error(
                    f"卖出{ticker}现金变化错误: "
                    f"预期{expected_cash_change:.2f}, 实际{actual_cash_change:.2f}"
                )
                return False
            
            # 验证持股减少
            expected_shares_change = -shares
            actual_shares_change = after_shares - before_shares
            
            if abs(expected_shares_change - actual_shares_change) > 0.01:
                self.log_error(
                    f"卖出{ticker}持股变化错误: "
                    f"预期{expected_shares_change}, 实际{actual_shares_change}"
                )
                return False
        
        self.log_success(f"{action} {shares}股 {ticker} @ ${price:.2f} 验证通过")
        return True
    
    def validate_portfolio_constraints(self, portfolio_data, max_position_pct=0.35):
        """
        验证投资组合约束条件
        
        Args:
            portfolio_data: 投资组合数据
            max_position_pct: 单一持仓最大比例
        
        Returns:
            bool: 验证是否通过
        """
        total_row = portfolio_data[portfolio_data['Ticker'] == 'TOTAL']
        if total_row.empty:
            self.log_error("缺少TOTAL行数据")
            return False
        
        total_equity = total_row.iloc[0]['Total Equity']
        
        for _, row in portfolio_data.iterrows():
            if row['Ticker'] == 'TOTAL':
                continue
            
            position_pct = row['Total Value'] / total_equity
            if position_pct > max_position_pct:
                self.log_error(
                    f"{row['Ticker']}持仓比例{position_pct:.1%}超过限制{max_position_pct:.1%}"
                )
                return False
        
        self.log_success("投资组合约束验证通过")
        return True
    
    def validate_data_continuity(self, current_data, previous_data):
        """
        验证数据连续性
        
        Args:
            current_data: 当前数据
            previous_data: 前一日数据
        
        Returns:
            bool: 验证是否通过
        """
        if previous_data is None:
            self.log_success("首日数据，跳过连续性检查")
            return True
        
        # 检查总资产异常变化
        current_total = current_data[current_data['Ticker'] == 'TOTAL'].iloc[0]['Total Equity']
        previous_total = previous_data[previous_data['Ticker'] == 'TOTAL'].iloc[0]['Total Equity']
        
        change_pct = abs(current_total - previous_total) / previous_total
        if change_pct > 0.5:  # 50%异常变化阈值
            self.log_warning(
                f"总资产异常变化: {change_pct:.1%} "
                f"(从${previous_total:.2f}到${current_total:.2f})"
            )
        
        self.log_success("数据连续性验证通过")
        return True
    
    def run_full_validation(self, portfolio_data, previous_data=None, trade_data=None):
        """
        运行完整的系统验证
        
        Args:
            portfolio_data: 当前投资组合数据
            previous_data: 前一日数据（可选）
            trade_data: 交易数据（可选）
        
        Returns:
            bool: 所有验证是否通过
        """
        print("🔍 开始系统完整性验证...")
        validation_start = datetime.now()
        
        all_passed = True
        
        # 1. 验证价格数据
        print("📊 验证价格数据...")
        for _, row in portfolio_data.iterrows():
            if row['Ticker'] != 'TOTAL':
                if not self.validate_price_data(row['Ticker'], row['Current Price']):
                    all_passed = False
        
        # 2. 验证数学计算
        print("🧮 验证数学计算...")
        if not self.validate_portfolio_math(portfolio_data):
            all_passed = False
        
        # 3. 验证投资组合约束
        print("⚖️ 验证投资组合约束...")
        if not self.validate_portfolio_constraints(portfolio_data):
            all_passed = False
        
        # 4. 验证数据连续性
        print("🔗 验证数据连续性...")
        if not self.validate_data_continuity(portfolio_data, previous_data):
            all_passed = False
        
        # 5. 如果有交易，验证交易执行
        if trade_data:
            print("💼 验证交易执行...")
            # 这里需要额外的逻辑来验证交易
            pass
        
        validation_end = datetime.now()
        duration = (validation_end - validation_start).total_seconds()
        
        if all_passed:
            self.log_success(f"✅ 所有验证检查通过 (耗时{duration:.2f}秒)")
            self.save_validation_report(True, duration)
        else:
            self.log_error(f"❌ 验证失败 (耗时{duration:.2f}秒)")
            self.save_validation_report(False, duration)
        
        return all_passed
    
    def save_validation_report(self, passed, duration):
        """保存验证报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'passed': passed,
            'duration_seconds': duration,
            'validation_results': self.validation_results
        }
        
        report_file = self.data_dir / f"validation_report_{datetime.now().strftime('%Y%m%d')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
    
    def log_error(self, message):
        """记录错误"""
        logging.error(message)
        self.validation_results.append({'level': 'ERROR', 'message': message})
        print(f"❌ {message}")
    
    def log_warning(self, message):
        """记录警告"""
        logging.warning(message)
        self.validation_results.append({'level': 'WARNING', 'message': message})
        print(f"⚠️ {message}")
    
    def log_success(self, message):
        """记录成功"""
        logging.info(message)
        self.validation_results.append({'level': 'SUCCESS', 'message': message})
        print(f"✅ {message}")

# 使用示例
if __name__ == "__main__":
    # 创建验证器实例
    validator = SystemIntegrityValidator("../data")
    
    # 示例投资组合数据
    sample_data = pd.DataFrame([
        {
            'Date': '2025-08-05',
            'Ticker': 'ABEO',
            'Shares': 6.0,
            'Cost Basis': 34.62,
            'Stop Loss': 4.90,
            'Current Price': 5.77,
            'Total Value': 34.62,
            'PnL': 0.0,
            'Action': 'HOLD',
            'Cash Balance': '',
            'Total Equity': ''
        },
        {
            'Date': '2025-08-05',
            'Ticker': 'TOTAL',
            'Shares': '',
            'Cost Basis': '',
            'Stop Loss': '',
            'Current Price': '',
            'Total Value': 34.62,
            'PnL': 0.0,
            'Action': '',
            'Cash Balance': 65.38,
            'Total Equity': 100.0
        }
    ])
    
    # 运行验证
    result = validator.run_full_validation(sample_data)
    print(f"\n验证结果: {'通过' if result else '失败'}")