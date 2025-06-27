# Algo_trading



A Python-based mini algo-trading system that:

- Connects to live stock data via Yahoo Finance
- Uses RSI + Moving Average crossover strategy
- Logs trade signals to Google Sheets
- Includes ML prediction and a Streamlit dashboard
- Sends Telegram alerts for Buy/Sell signals

---

##  Strategy Logic

- **Buy** when RSI < 30 and 20-DMA crosses above 50-DMA
- **Sell** when position was held and signal turns false

---

## Tech Stack

- Python, Pandas, YFinance
- Google Sheets API
- Scikit-Learn (Logistic Regression)
- Streamlit Dashboard
- Telegram Bot API

---

##  Project Structure

main.py # Core script to run logic and log to sheet
dashboard.py # Streamlit dashboard
strategy.py # RSI + MA crossover strategy
ml_model.py # Machine learning predictions
notifier.py # Telegram alerts
google_sheets.py # Google Sheets logging



---

##  Run the Project

1. Clone the repo
2. Create and activate a virtual environment
3. Install dependencies:

```bash
pip install -r requirements.txt
Add your creds.json from Google Cloud

Run the main bot: python main.py
Launch the dashboard: streamlit run dashboard.py
