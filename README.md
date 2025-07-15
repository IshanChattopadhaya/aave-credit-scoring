# DeFi Credit Scoring on Aave V2 Wallets

This project implements a machine learning-based credit scoring system that assigns scores between **0 and 1000** to user wallets interacting with the **Aave V2 protocol**, based solely on historical transaction behavior.

---

## Problem Statement

> **Objective**: Build a robust, explainable ML model using transaction-level JSON records from Aave V2 to score wallet reliability.

Each wallet is analyzed and given a credit score:
- **High score (700–1000)**: Reliable and responsible behavior
- **Medium score (301–699)**: Moderate usage or responsibility
- **Low score (0–300)**: Risky, spammy, or bot-like behavior

---

## Architecture Overview

user-transactions.json
        │
        ▼
  [parser.py] → Normalized transactions
        │
        ▼
  [feature_engineering.py] → Wallet-level features
        │
        ▼
  [train_model.py] → Trains a classifier model
        │
        ▼
  [scoring.py] → Applies model, generates scores (0–1000)
        │
        ▼
wallet_scores.csv
