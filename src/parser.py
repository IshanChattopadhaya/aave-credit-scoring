# src/parser.py
import json
import os

def parse_transactions(json_file_path):
    """
    Parse raw JSON transactions and return a list of normalized transaction dictionaries.
    Each record will have: wallet, action, timestamp, assetSymbol, amount_usd
    """
    parsed = []

    if not os.path.exists(json_file_path):
        print(f"File not found: {json_file_path}")
        return []

    with open(json_file_path, 'r') as f:
        data = json.load(f)

    for tx in data:
        try:
            wallet = tx['userWallet']
            action = tx['action'].lower()
            ts = tx['timestamp']

            raw_amount = float(tx['actionData']['amount'])
            price_usd = float(tx['actionData']['assetPriceUSD'])
            symbol = tx['actionData']['assetSymbol']

            # Normalize amount: assume token has 6 (like USDC) or 18 (like MATIC) decimals
            # Simplified: infer from amount size
            if raw_amount > 1e20:  # e.g., 145000000000000000000
                amount = raw_amount / 1e18
            elif raw_amount > 1e6:
                amount = raw_amount / 1e6
            else:
                amount = raw_amount  # fallback

            amount_usd = amount * price_usd

            parsed.append({
                'wallet': wallet,
                'action': action,
                'timestamp': ts,
                'assetSymbol': symbol,
                'amount_usd': amount_usd
            })

        except Exception as e:
            print(f"Skipping record due to error: {e}")
            continue

    return parsed

if __name__ == "__main__":
    from pprint import pprint

    #  Use raw string to avoid Windows path issues
    json_file_path = r"C:\Users\NandiniC\Desktop\aave-credit-scoring\data\user-transactions.json"

    result = parse_transactions(json_file_path)
    pprint(result[:5])  # show first 5 parsed transactions