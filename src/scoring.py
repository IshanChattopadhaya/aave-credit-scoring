# src/scoring.py

# src/scoring.py

import pandas as pd
import numpy as np
import joblib

def score_wallets(feature_path="data/wallet_features.csv",
                  model_path="data/credit_model_xgb.pkl",
                  output_path="data/wallet_scores.csv"):

    # Load model
    model = joblib.load(model_path)

    # Load feature names used during training
    with open("data/feature_names.txt", "r") as f:
        features = [line.strip() for line in f.readlines()]

    # Load wallet features
    df = pd.read_csv(feature_path)

    # Ensure all expected features are present
    for col in features:
        if col not in df.columns:
            df[col] = 0

    # Only keep the columns used during training
    df = df[['wallet'] + features]

    # Fill NaNs
    df[features] = df[features].fillna(0)

    # Apply log1p transformation to skewed features (must match train script)
    log_features = [f for f in features if f in [
        'total_deposit', 'total_borrow', 'total_repay', 'total_redeem',
        'total_liquidation', 'tx_count', 'active_days', 'activity_span_seconds'
    ]]
    for col in log_features:
        df[col] = np.log1p(df[col])

    # Extract X in exact order
    X = df[features]

    # Predict and clip
    repay_score = model.predict(X)
    repay_score = np.clip(repay_score, 0, 1)

    # Convert to 0–1000 credit score
    df['credit_score'] = (repay_score * 1000).astype(int)

    # Save output
    df[['wallet', 'credit_score']].to_csv(output_path, index=False)
    print(f"Credit scores saved to {output_path}")
