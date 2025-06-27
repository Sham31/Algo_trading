# strategy.py
import pandas as pd

def compute_rsi(df, period=14):
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    df['RSI'] = rsi
    return df

def apply_strategy(df):
    df['20DMA'] = df['Close'].rolling(window=20).mean()
    df['50DMA'] = df['Close'].rolling(window=50).mean()
    df = compute_rsi(df)

    df['Signal'] = (df['RSI'] < 30) & (df['20DMA'] > df['50DMA'])
    df['Position'] = df['Signal'].shift(1).ffill().fillna(False)
    return df
