# 系统完整性验证框架

## 🔒 模拟引擎密封性保证

### 核心原则
确保在记录任何交易前，模拟引擎的计算和逻辑完全准确、可靠、可审计。

---

## 📊 数据完整性检查清单

### 每日数据验证 (DAILY_VALIDATION)
```
□ 股价数据来源验证
  - yfinance数据是否成功获取
  - 价格是否在合理范围内（±20%日波动检查）
  - 数据时间戳是否正确

□ 投资组合计算验证
  - 持股数量 × 当前价格 = 总价值
  - 成本基础计算是否正确
  - 盈亏计算：(当前价值 - 成本基础)
  - 现金余额是否平衡

□ 总资产验证
  - 总资产 = 所有持仓价值 + 现金余额
  - 与前一日数据的连续性检查
  - 异常波动预警（>±15%单日变化）
```

### 交易执行验证 (TRADE_VALIDATION)
```
□ 交易前检查
  - 现金是否足够（买入）
  - 持股是否足够（卖出）
  - 价格是否在当日交易范围内
  - 是否违反投资组合限制（35%单一持仓）

□ 交易计算验证
  - 买入：现金减少 = 股数 × 价格 + 手续费
  - 卖出：现金增加 = 股数 × 价格 - 手续费
  - 新的成本基础计算
  - 新的持股数量

□ 交易后验证
  - 总资产守恒（除手续费外）
  - 所有数据更新正确
  - CSV文件写入成功
```

---

## 🔧 自动化验证脚本

### validation_engine.py
```python
import pandas as pd
import yfinance as yf
from datetime import datetime
import logging

class SystemIntegrityValidator:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            filename=f'{self.data_dir}/validation.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def validate_price_data(self, ticker, price):
        """验证股价数据的合理性"""
        try:
            # 获取最近5天数据
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5d")
            
            if hist.empty:
                self.log_error(f"无法获取{ticker}的历史数据")
                return False
            
            recent_high = hist['High'].max()
            recent_low = hist['Low'].min()
            
            # 检查价格是否在合理范围内
            if not (recent_low * 0.8 <= price <= recent_high * 1.2):
                self.log_error(f"{ticker}价格{price}超出合理范围[{recent_low*0.8:.2f}, {recent_high*1.2:.2f}]")
                return False
            
            return True
        except Exception as e:
            self.log_error(f"价格验证失败: {e}")
            return False
    
    def validate_portfolio_math(self, portfolio_data):
        """验证投资组合数学计算"""
        errors = []
        
        for _, row in portfolio_data.iterrows():
            if row['Ticker'] == 'TOTAL':
                continue
                
            # 验证总价值计算
            expected_value = row['Shares'] * row['Current Price']
            if abs(expected_value - row['Total Value']) > 0.01:
                errors.append(f"{row['Ticker']}: 总价值计算错误")
            
            # 验证盈亏计算
            expected_pnl = row['Total Value'] - row['Cost Basis']
            if abs(expected_pnl - row['PnL']) > 0.01:
                errors.append(f"{row['Ticker']}: 盈亏计算错误")
        
        if errors:
            for error in errors:
                self.log_error(error)
            return False
        return True
    
    def validate_trade_execution(self, trade_data, before_cash, after_cash, before_portfolio, after_portfolio):
        """验证交易执行的正确性"""
        action = trade_data['action']
        ticker = trade_data['ticker']
        shares = trade_data['shares']
        price = trade_data['price']
        
        if action.upper() == 'BUY':
            expected_cash_change = -(shares * price)
            actual_cash_change = after_cash - before_cash
            
            if abs(expected_cash_change - actual_cash_change) > 0.01:
                self.log_error(f"买入交易现金变化错误: 预期{expected_cash_change}, 实际{actual_cash_change}")
                return False
        
        elif action.upper() == 'SELL':
            expected_cash_change = shares * price
            actual_cash_change = after_cash - before_cash
            
            if abs(expected_cash_change - actual_cash_change) > 0.01:
                self.log_error(f"卖出交易现金变化错误: 预期{expected_cash_change}, 实际{actual_cash_change}")
                return False
        
        return True
    
    def validate_total_equity_conservation(self, before_total, after_total, trade_fees=0):
        """验证总资产守恒（除手续费外）"""
        expected_change = -trade_fees
        actual_change = after_total - before_total
        
        # 允许小幅价格波动，但不应有大的资产"凭空消失"
        if abs(actual_change - expected_change) > before_total * 0.05:  # 5%容忍度
            self.log_error(f"总资产异常变化: {actual_change:.2f}, 预期: {expected_change:.2f}")
            return False
        return True
    
    def log_error(self, message):
        """记录错误"""
        logging.error(message)
        print(f"❌ 验证失败: {message}")
    
    def log_success(self, message):
        """记录成功"""
        logging.info(message)
        print(f"✅ 验证通过: {message}")
    
    def run_full_validation(self, portfolio_data):
        """运行完整验证"""
        print("🔍 开始系统完整性验证...")
        
        # 验证价格数据
        for _, row in portfolio_data.iterrows():
            if row['Ticker'] != 'TOTAL':
                if not self.validate_price_data(row['Ticker'], row['Current Price']):
                    return False
        
        # 验证数学计算
        if not self.validate_portfolio_math(portfolio_data):
            return False
        
        self.log_success("所有验证检查通过")
        return True
```

---

## 📋 验证检查表

### 启动前检查 (PRE_START_CHECKLIST)
```
□ 所有Python依赖包已安装
□ 数据目录结构正确创建
□ CSV文件模板准备就绪
□ 提示词模板版本确认
□ 券商账户连接测试
□ 初始资金确认 ($100)
□ 风险参数设置确认
□ 日志系统正常工作
```

### 每日操作检查 (DAILY_OPERATION_CHECKLIST)
```
□ 运行系统完整性验证
□ 股价数据获取成功
□ 投资组合计算验证通过
□ Claude提示词使用正确模板
□ 交易决策记录完整
□ 风险检查通过
□ 数据备份完成
□ 日志文件更新
```

### 交易执行检查 (TRADE_EXECUTION_CHECKLIST)
```
□ 交易前系统验证
□ Claude交易建议确认
□ 风险管理检查通过
□ 券商账户执行成功
□ 模拟系统数据更新
□ 交易后验证通过
□ 交易日志记录
□ 系统状态确认
```

---

## 🚨 异常处理流程

### 数据异常处理
1. **价格数据异常**
   - 暂停交易
   - 手动验证数据源
   - 等待数据修复后继续

2. **计算错误**
   - 立即停止操作
   - 检查代码逻辑
   - 修复后重新验证

3. **系统不一致**
   - 回滚到最后已知正确状态
   - 分析不一致原因
   - 修复后重新同步

### 紧急恢复程序
```
1. 备份当前所有数据
2. 恢复到最后验证通过的状态
3. 手动核对券商账户实际持仓
4. 重新同步模拟系统
5. 运行完整验证
6. 确认系统完整性后继续
```

---

## 📊 质量保证指标

### 系统可靠性指标
- **数据准确率**: >99.9%
- **计算错误率**: <0.1%
- **系统可用性**: >99.5%
- **验证通过率**: 100%

### 监控报告
- 每日验证报告
- 每周系统健康检查
- 每月完整性审计
- 异常事件记录

这个系统确保了实验的科学性和可靠性，解决了原ChatGPT实验中的系统完整性问题。