# backtest.py
def backtest_strategy(df):
    df['Returns'] = df['Close'].pct_change()
    df['Strategy'] = df['Returns'] * df['Position']
    df['Cumulative'] = (1 + df['Strategy']).cumprod()
    return df
