# src/train_model.py

import pandas as pd
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


def generate_labels(df):
    """
    Create proxy labels:
    - Label = 1 if repay_borrow_ratio > 0.5 and no liquidation
    - Label = 0 otherwise
    """
    df['label'] = ((df['repay_borrow_ratio'] > 0.5) & (df['total_liquidation'] == 0)).astype(int)
    print("Label distribution:\n", df['label'].value_counts())
    return df


def log_transform(df, cols):
    for col in cols:
        df[col] = np.log1p(df[col])  # log(1 + x), safe for zeroes
    return df


def train_credit_model(
    csv_path="data/wallet_features.csv",
    save_path="data/credit_model.pkl"
):
    # Load feature data
    df = pd.read_csv(csv_path)

    # Step 1: Create proxy labels
    df = generate_labels(df)

    # Step 2: Feature selection
    feature_cols = [
        'total_deposit', 'total_borrow', 'total_repay',
        'repay_borrow_ratio', 'total_liquidation', 'tx_count'
    ]

    # Step 3: Log-transform high-range features
    log_cols = ['total_deposit', 'total_borrow', 'total_repay', 'tx_count']
    df = log_transform(df, log_cols)

    # Step 4: Prepare X and y
    X = df[feature_cols]
    y = df['label']

    # Step 5: Split and train
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Step 6: Evaluate
    y_pred = model.predict(X_test)
    print("\n📊 Classification Report:\n")
    print(classification_report(y_test, y_pred))

    # Step 7: Save model
    joblib.dump(model, save_path)
    print(f"\n✅ Model saved to: {save_path}")


if __name__ == "__main__":
    train_credit_model()

