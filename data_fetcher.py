# data_fetcher.py
import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, period='6mo', interval='1d'):
    df = yf.download(ticker, period=period, interval=interval)
    df.dropna(inplace=True)
    return df
