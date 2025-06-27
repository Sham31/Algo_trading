import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.graph_objects as go
import subprocess

# --- Google Sheets Setup ---
def load_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    return client.open(sheet_name)

def get_df(sheet, tab_name):
    try:
        ws = sheet.worksheet(tab_name)
        data = ws.get_all_records()
        return pd.DataFrame(data)
    except:
        return pd.DataFrame()

# --- App UI ---
st.set_page_config(page_title="Algo Trading Dashboard", layout="wide")
st.title("📈 Algo Trading Dashboard")

sheet = load_sheet("AlgoTradingSheet")

# --- Summary Section ---
st.header("📊 Portfolio Summary")
summary_df = get_df(sheet, "Summary")

if not summary_df.empty:
    st.dataframe(summary_df, use_container_width=True)
    st.metric("💹 Best Performing", summary_df.loc[summary_df['Cumulative Return'].idxmax()]['Ticker'])
else:
    st.warning("Summary data not found.")

# --- Stock Logs Section ---
st.header("📌 Stock Signal Viewer")
selected_stock = st.selectbox("Choose Stock", ['RELIANCE.NS', 'INFY.NS', 'TCS.NS'])

log_df = get_df(sheet, f"{selected_stock}_Log")

# 🔧 Flatten MultiIndex columns if any
log_df.columns = [' '.join(col).strip() if isinstance(col, tuple) else col for col in log_df.columns]

# 📋 Show available columns for debugging
# st.write("Available columns:", log_df.columns.tolist())

if not log_df.empty:
    # Dynamically find columns
    close_col = next((col for col in log_df.columns if 'Close' in col), None)
    rsi_col = next((col for col in log_df.columns if 'RSI' in col), None)

    # --- Plot Price with Buy/Sell Markers ---
    if close_col:
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=log_df['Date'] if 'Date' in log_df else log_df.index,
            y=log_df[close_col],
            mode='lines',
            name='Close Price'
        ))

        if 'Signal' in log_df.columns:
            buy_signals = log_df[log_df['Signal'] == True]
            fig.add_trace(go.Scatter(
                x=buy_signals['Date'] if 'Date' in buy_signals else buy_signals.index,
                y=buy_signals[close_col],
                mode='markers',
                name='Buy',
                marker=dict(color='green', symbol='triangle-up', size=10)
            ))

        if 'Position' in log_df.columns:
            sell_signals = log_df[(log_df['Position'] == True) & (log_df['Signal'] == False)]
            fig.add_trace(go.Scatter(
                x=sell_signals['Date'] if 'Date' in sell_signals else sell_signals.index,
                y=sell_signals[close_col],
                mode='markers',
                name='Sell',
                marker=dict(color='red', symbol='triangle-down', size=10)
            ))

        fig.update_layout(title=f"{selected_stock} Price with Buy/Sell Signals",
                          xaxis_title='Date',
                          yaxis_title='Price',
                          height=500)

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ 'Close' column not found.")

    # --- RSI Chart ---
    if rsi_col:
        st.subheader("📉 RSI")
        st.bar_chart(log_df[[rsi_col]], use_container_width=True)
    else:
        st.warning("⚠️ 'RSI' column not found.")

    # --- Recent Data Table ---
    st.subheader("📄 Last 10 Signal Entries")
    st.dataframe(log_df.tail(10), use_container_width=True)

else:
    st.warning("Log data not available yet.")

# --- ML Accuracy Overview ---
st.header("🧠 ML Insights")
if not summary_df.empty:
    for _, row in summary_df.iterrows():
        try:
            acc = float(row['ML Accuracy'])
            st.metric(label=row['Ticker'], value=f"🎯 Accuracy: {round(acc * 100, 2)}%")
        except:
            st.metric(label=row['Ticker'], value="⚠️ Accuracy not available")

# --- Run main.py Button ---
st.header("⚙️ Run Strategy")
if st.button("▶️ Run Now"):
    with st.spinner("Running strategy... please wait."):
        try:
            result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
            st.success("Strategy executed successfully!")
            st.code(result.stdout)
        except Exception as e:
            st.error("Error running script:")
            st.code(str(e))
