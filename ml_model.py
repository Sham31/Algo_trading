# ml_model.py
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def add_ml_features(df):
    df['MACD'] = df['Close'].ewm(12).mean() - df['Close'].ewm(26).mean()
    df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
    return df

def train_model(df):
    df = df.dropna()
    features = df[['RSI', 'MACD', 'Volume']]
    labels = df['Target']

    X_train, X_test, y_train, y_test = train_test_split(features, labels, shuffle=False)
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    accuracy = accuracy_score(y_test, preds)
    return model, accuracy
