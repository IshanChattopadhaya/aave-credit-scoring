# src/train_model.py
import pandas as pd
import numpy as np
import joblib
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Load wallet features
df = pd.read_csv("data/wallet_features.csv")

# Compute continuous target: repay-to-borrow ratio as proxy for creditworthiness
df['repay_ratio'] = df['total_repay'] / (df['total_borrow'] + 1e-6)
df['repay_ratio'] = df['repay_ratio'].clip(0, 1)

# Full feature set
features = [
    'total_deposit',
    'total_borrow',
    'total_repay',
    'total_redeem',
    'total_liquidation',
    'tx_count',
    'unique_actions',
    'repay_borrow_ratio',
    'redeem_deposit_ratio',
    'active_days',
    'activity_span_seconds'
]

# Fill NaNs with 0 (in case of division or missing fields)
df[features] = df[features].fillna(0)

# Apply log1p transform to reduce skew (except ratios and counts)
log_features = [
    'total_deposit',
    'total_borrow',
    'total_repay',
    'total_redeem',
    'total_liquidation',
    'tx_count',
    'activity_span_seconds',
    'active_days'
]
df[log_features] = np.log1p(df[log_features])

# Final dataset
X = df[features]
y = df['repay_ratio']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train XGBoost Regressor
model = xgb.XGBRegressor(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=5,
    objective='reg:squarederror',
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("\n XGBoost Regressor Evaluation:")
print(f"R² Score: {r2_score(y_test, y_pred):.4f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}")

# Save model
joblib.dump(model, "data/credit_model_xgb.pkl")

# Save the feature names used
with open("data/feature_names.txt", "w") as f:
    f.write("\n".join(features))

print("\n Model trained and saved successfully.")


