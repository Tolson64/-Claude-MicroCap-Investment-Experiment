import pandas as pd
import yfinance as yf
import os
from datetime import datetime

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TRACKER_FILE = os.path.join(SCRIPT_DIR, 'portfolio_tracker.csv')
PERFORMANCE_LOG_FILE = os.path.join(SCRIPT_DIR, 'daily_performance_log.csv')
INDEX_TICKERS = {
    'S&P 500': '^GSPC',
    'Russell 2000': '^RUT',
    'XBI': 'XBI'
}

def get_latest_prices(tickers):
    """Fetches the latest market prices for a list of tickers."""
    if not tickers:
        return pd.Series(dtype=float)
    data = yf.download(tickers, period="1d", progress=False, auto_adjust=True)
    if not data.empty:
        return data['Close'].iloc[-1]
    return pd.Series(dtype=float)

def calculate_current_holdings(df):
    """Calculates current holdings and average cost basis from transaction log."""
    holdings = {}
    # Ensure 'Fee' column exists and fill NaN with 0
    if 'Fee' not in df.columns:
        df['Fee'] = 0
    df['Fee'] = df['Fee'].fillna(0)

    for _, row in df.iterrows():
        ticker = row['Ticker']
        action = row['Action'].upper()
        shares = row['Shares']
        price = row['Price']
        fee = row['Fee']
        
        if ticker not in holdings:
            holdings[ticker] = {'shares': 0, 'total_cost': 0, 'stop_loss': row.get('StopLoss')}
        
        if action == 'BUY':
            holdings[ticker]['shares'] += shares
            holdings[ticker]['total_cost'] += (shares * price) + fee # Add fee to cost
        elif action == 'SELL':
            holdings[ticker]['shares'] -= shares
            # We don't adjust total_cost on sell, as cost basis is based on buys
            
    # Filter out stocks that have been completely sold
    active_holdings = {t: d for t, d in holdings.items() if d['shares'] > 0}
    
    # Convert to DataFrame
    summary = []
    for ticker, data in active_holdings.items():
        if data['shares'] > 0:
            avg_cost = data['total_cost'] / data['shares']
            summary.append({
                'Ticker': ticker,
                'Shares': data['shares'],
                'Cost Basis': avg_cost,
                'Stop Loss': data['stop_loss']
            })
            
    return pd.DataFrame(summary)

def run_daily_update():
    """Main function to update portfolio performance based on the tracker file."""
    try:
        # 1. Read the master transaction log
        transactions_df = pd.read_csv(TRACKER_FILE)
        
        # 2. Calculate current holdings and cost basis
        holdings_df = calculate_current_holdings(transactions_df)

        if holdings_df.empty:
            print("No active holdings found in portfolio_tracker.csv.")
            return

        # 3. Fetch latest prices for holdings and indices
        stock_tickers = holdings_df['Ticker'].tolist()
        all_tickers_to_fetch = stock_tickers + list(INDEX_TICKERS.values())
        latest_prices = get_latest_prices(all_tickers_to_fetch)

        # 4. Prepare today's performance data
        today_records = []
        total_portfolio_value = 0
        total_investment_cost = 0
        today_str = datetime.now().strftime('%Y-%m-%d')

        for _, row in holdings_df.iterrows():
            ticker = row['Ticker']
            shares = row['Shares']
            cost_basis = row['Cost Basis']
            investment_cost = shares * cost_basis
            current_price = latest_prices.get(ticker, 0)
            total_value = shares * current_price
            pnl = total_value - investment_cost
            
            record = {
                'Date': today_str,
                'Ticker': ticker,
                'Shares': shares,
                'Cost Basis': cost_basis,
                'Stop Loss': row['Stop Loss'],
                'Current Price': current_price,
                'Total Value': total_value,
                'PnL': pnl,
                'Action': 'HOLD',
            }
            today_records.append(record)
            total_portfolio_value += total_value
            total_investment_cost += investment_cost

        # 5. Create the TOTAL summary row and add index data
        # Calculate cash balance based on all transactions, including fees
        if 'Fee' not in transactions_df.columns:
            transactions_df['Fee'] = 0
        transactions_df['Fee'] = transactions_df['Fee'].fillna(0)

        buys = transactions_df[transactions_df['Action'].str.upper() == 'BUY']
        sells = transactions_df[transactions_df['Action'].str.upper() == 'SELL']
        
        total_buy_cost = (buys['Shares'] * buys['Price']).sum() + buys['Fee'].sum()
        total_sell_revenue = (sells['Shares'] * sells['Price']).sum() - sells['Fee'].sum()
        
        # Assuming initial capital of 100 for now. This could be made more robust.
        initial_capital = 100.00 
        cash_balance = initial_capital - total_buy_cost + total_sell_revenue
        
        total_equity = total_portfolio_value + cash_balance
        total_pnl = total_portfolio_value - total_investment_cost

        total_record = {
            'Date': today_str,
            'Ticker': 'TOTAL',
            'Total Value': total_portfolio_value,
            'PnL': total_pnl,
            'Cash Balance': cash_balance,
            'Total Equity': total_equity,
            'S&P 500': latest_prices.get(INDEX_TICKERS['S&P 500']),
            'Russell 2000': latest_prices.get(INDEX_TICKERS['Russell 2000']),
            'XBI': latest_prices.get(INDEX_TICKERS['XBI']),
        }
        
        # 6. Append to the performance log file
        output_df = pd.DataFrame(today_records)
        
        # Create a temporary DataFrame for the total row to merge
        total_df = pd.DataFrame([total_record])
        
        # Use merge to align columns, fill non-matching with NaN
        final_output_df = pd.concat([output_df, total_df], ignore_index=True)
        
        column_order = [
            'Date', 'Ticker', 'Shares', 'Cost Basis', 'Stop Loss', 
            'Current Price', 'Total Value', 'PnL', 'Action', 'Cash Balance', 
            'Total Equity', 'S&P 500', 'Russell 2000', 'XBI'
        ]
        
        # Reorder and ensure all columns are present
        final_output_df = final_output_df.reindex(columns=column_order)

        file_exists = os.path.exists(PERFORMANCE_LOG_FILE)
        
        # If file exists, load it to check headers
        if file_exists:
            existing_df = pd.read_csv(PERFORMANCE_LOG_FILE)
            # If headers don't match, we might need to handle it (e.g., backup and create new)
            if not all(col in existing_df.columns for col in column_order):
                print("Log file headers are outdated. Consider backing up and creating a new one.")
                # For this implementation, we'll just append with the new headers
                final_output_df.to_csv(PERFORMANCE_LOG_FILE, mode='a', header=True, index=False, float_format='%.2f')
            else:
                 final_output_df.to_csv(PERFORMANCE_LOG_FILE, mode='a', header=False, index=False, float_format='%.2f')
        else:
            final_output_df.to_csv(PERFORMANCE_LOG_FILE, mode='a', header=True, index=False, float_format='%.2f')


        print(f"Successfully prepared daily performance for {today_str}.")
        print("--- Portfolio Summary ---")
        print(final_output_df.to_markdown(index=False, floatfmt=".2f"))

    except FileNotFoundError:
        print(f"Error: Tracker file not found at {TRACKER_FILE}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_daily_update()