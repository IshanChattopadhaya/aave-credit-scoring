# src/scoring.py

import pandas as pd
import joblib
import numpy as np
import os


def log_transform(df, cols):
    for col in cols:
        df[col] = np.log1p(df[col])
    return df


def score_wallets(
    feature_path="data/wallet_features.csv",
    model_path="data/credit_model.pkl",
    output_path="data/wallet_scores.csv"
):
    # Check files
    if not os.path.exists(feature_path):
        print(f"Feature file not found: {feature_path}")
        return
    if not os.path.exists(model_path):
        print(f"Model file not found: {model_path}")
        return

    # Load model
    model = joblib.load(model_path)

    # Load features
    df = pd.read_csv(feature_path)

    # Define features and apply same log1p transform
    feature_cols = [
        'total_deposit', 'total_borrow', 'total_repay',
        'repay_borrow_ratio', 'total_liquidation', 'tx_count'
    ]
    log_cols = ['total_deposit', 'total_borrow', 'total_repay', 'tx_count']
    df = log_transform(df, log_cols)

    #  Predict probabilities
    X = df[feature_cols]
    probs = model.predict_proba(X)[:, 1]  # probability of class 1 (reliable)

    #  Convert to credit score
    df['credit_score'] = (probs * 1000).round().astype(int)

    #  Save scores
    df[['wallet', 'credit_score']].to_csv(output_path, index=False)
    print(f" Wallet scores saved to: {output_path}")

    #  Optional: preview
    print(df[['wallet', 'credit_score']].head(10))

    return df[['wallet', 'credit_score']]


if __name__ == "__main__":
    score_wallets()

