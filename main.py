# main.py
from notifier import send_telegram_alert
from data_fetcher import fetch_stock_data
from strategy import apply_strategy
from backtest import backtest_strategy
from google_sheets import connect_to_sheet, log_to_sheet
from ml_model import add_ml_features, train_model
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


send_telegram_alert("🔔 This is a test alert from my trading bot!")

tickers = ['RELIANCE.NS', 'INFY.NS', 'TCS.NS'] 
sheet_name = "AlgoTradingSheet"

def run():
    sheet = connect_to_sheet(sheet_name)
    summary = []

    for ticker in tickers:
        df = fetch_stock_data(ticker)
        df = apply_strategy(df)
        df = backtest_strategy(df)
        df = add_ml_features(df)

        model, accuracy = train_model(df)
        df = df.reset_index()
        latest = df.iloc[-1]

        
        try:
            if latest['Signal'].item() == True:
                send_telegram_alert(f"📈 BUY SIGNAL for {ticker}\nPrice: ₹{latest['Close']:.2f}")
            elif latest['Signal'].item() == False and latest['Position'].item() == True:
                send_telegram_alert(f"📉 SELL SIGNAL for {ticker}\nPrice: ₹{latest['Close']:.2f}")
        except Exception as e:
            print(f"⚠️ Could not evaluate signal for {ticker}: {e}")



       

        log_to_sheet(sheet, f"{ticker}_Log", df.tail(30))
        summary.append({
            "Ticker": ticker,
            "Latest Signal": bool(latest['Signal'].item()),
            "Cumulative Return": float(latest['Cumulative']),
            "ML Accuracy": accuracy
        })

    summary_df = pd.DataFrame(summary)
    log_to_sheet(sheet, "Summary", summary_df)
    print("Trading logic executed and logged.")

if __name__ == "__main__":
    run() 




