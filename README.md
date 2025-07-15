# DeFi Credit Scoring on Aave V2 Wallets

This project implements a **machine learning-based credit scoring system** for wallets interacting with the **Aave V2 protocol**. It processes raw DeFi transaction data and generates credit scores between **0 and 1000**, where higher scores reflect more responsible behavior.

---

## Problem Statement

> **Objective**: Given historical transaction-level data from Aave V2, build a robust, explainable ML model that scores each wallet based on its behavior.

Each wallet is assigned a credit score based on its on-chain activity:

- **High (700–1000)** → Trusted, active, repayment-focused behavior  
- **Medium (301–699)** → Moderate risk, decent usage  
- **Low (0–300)** → Risky, spammy, bot-like, or exploitative behavior

---

## Key Features Engineered

From the raw JSON, we engineer meaningful features at the wallet level:

| Feature                  | Description                                               |
|--------------------------|-----------------------------------------------------------|
| `total_deposit`          | Total USD value deposited                                 |
| `total_borrow`           | Total borrowed value                                      |
| `total_repay`            | Amount repaid                                             |
| `total_redeem`           | Withdrawals / redemptions                                 |
| `total_liquidation`      | Value liquidated                                          |
| `repay_borrow_ratio`     | Indicates repayment behavior                              |
| `redeem_deposit_ratio`   | Indicates withdrawal vs deposit tendencies                |
| `tx_count`               | Total transaction count                                   |
| `unique_actions`         | Number of distinct actions performed                      |
| `active_days`            | Active usage span in days                                 |
| `activity_span_seconds`  | Total duration of wallet activity                         |

---

## 🏗️ Project Architecture

user-transactions.json
│
▼
[parser.py] → Normalized transactions
│
▼
[feature_engineering.py] → Wallet-level features
│
▼
[train_model.py] → Trains a Regression model
│
▼
[scoring.py] → Applies model, generates scores (0–1000)
│
▼
wallet_scores.csv → Final output
│
▼
analysis.md → Score segment analysis


## Model Details

- **Model**: XGBoost Regressor  
- **Target Variable**: `repay_ratio = total_repay / (total_borrow + ε)`  
- **Scaling**: Repay ratio scaled to `[0, 1]`, then mapped to credit scores `[0, 1000]`  
- **Preprocessing**: Log transformation (`log1p`) on skewed features  
- **Evaluation**: RMSE, R² on test split

## Directory Structure

aave-credit-scoring/
├── data/
│   ├── user-transactions.json
│   ├── wallet_features.csv
│   └── wallet_scores.csv
├── src/
│   ├── parser.py
│   ├── feature_engineering.py
│   ├── train_model.py
│   ├── scoring.py
│   └── main.py
├── analysis.md
└── README.md



