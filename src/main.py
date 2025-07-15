# src/main.py

import os
from parser import parse_transactions
from feature_engineering import compute_wallet_features
from scoring import score_wallets

def run_pipeline(
    raw_json_path="data/user-transactions.json",
    intermediate_csv_path="data/wallet_features.csv",
    model_path="data/credit_model_xgb.pkl",
    output_csv_path="data/wallet_scores.csv"
):
    print(" Starting credit scoring pipeline...")

    # Step 1: Parse JSON
    print(" Parsing raw transactions...")
    tx_data = parse_transactions(raw_json_path)

    if not tx_data:
        print(" No transactions parsed. Exiting.")
        return

    # Step 2: Feature Engineering
    print(" Building wallet-level features...")
    df_wallets = compute_wallet_features(tx_data)
    df_wallets.to_csv(intermediate_csv_path, index=False)

    # Step 3: ML Scoring
    print(" Generating credit scores...")
    score_wallets(
        feature_path=intermediate_csv_path,
        model_path=model_path,
        output_path=output_csv_path
    )

    print(" Credit scoring pipeline completed.")


if __name__ == "__main__":
    run_pipeline()
