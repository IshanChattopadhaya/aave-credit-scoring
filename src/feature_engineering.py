# src/feature_engineering.py

from collections import defaultdict
import pandas as pd

def compute_wallet_features(parsed_data):
    """
    Given a list of parsed transactions, compute aggregated features per wallet.
    Returns a DataFrame: one row per wallet.
    """

    wallets = defaultdict(lambda: {
        'total_deposit': 0,
        'total_borrow': 0,
        'total_repay': 0,
        'total_redeem': 0,
        'total_liquidation': 0,
        'tx_count': 0,
        'unique_actions': set(),
        'timestamps': []
    })

    for tx in parsed_data:
        wallet = tx['wallet']
        action = tx['action']
        amount = tx['amount_usd']
        ts = tx['timestamp']

        wallets[wallet]['tx_count'] += 1
        wallets[wallet]['unique_actions'].add(action)
        wallets[wallet]['timestamps'].append(ts)

        if action == 'deposit':
            wallets[wallet]['total_deposit'] += amount
        elif action == 'borrow':
            wallets[wallet]['total_borrow'] += amount
        elif action == 'repay':
            wallets[wallet]['total_repay'] += amount
        elif action == 'redeemunderlying':
            wallets[wallet]['total_redeem'] += amount
        elif action == 'liquidationcall':
            wallets[wallet]['total_liquidation'] += amount

    # Now convert to flat list of dicts
    result = []
    for wallet, data in wallets.items():
        # Basic ratios
        repay_borrow_ratio = (data['total_repay'] / data['total_borrow']) if data['total_borrow'] > 0 else 0
        redeem_deposit_ratio = (data['total_redeem'] / data['total_deposit']) if data['total_deposit'] > 0 else 0

        # Temporal stats
        active_days = len(set(pd.to_datetime(data['timestamps'], unit='s').date))
        time_span = max(data['timestamps']) - min(data['timestamps']) if len(data['timestamps']) > 1 else 0

        result.append({
            'wallet': wallet,
            'total_deposit': data['total_deposit'],
            'total_borrow': data['total_borrow'],
            'total_repay': data['total_repay'],
            'total_redeem': data['total_redeem'],
            'total_liquidation': data['total_liquidation'],
            'tx_count': data['tx_count'],
            'unique_actions': len(data['unique_actions']),
            'repay_borrow_ratio': repay_borrow_ratio,
            'redeem_deposit_ratio': redeem_deposit_ratio,
            'active_days': active_days,
            'activity_span_seconds': time_span
        })

    return pd.DataFrame(result)
