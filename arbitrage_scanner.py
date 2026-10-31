"""Crypto arbitrage scanner (price comparison only).

Compares the same asset's price across sources, finds the cheapest
buy and most expensive sell, and computes the spread before and after
an assumed fee. It does not execute trades, move funds, or connect
to any exchange account. Prices are supplied as input (or mocked in
tests), so the core logic is fully testable offline.
"""
import argparse
import json
import sys


def scan(prices, threshold_pct=1.0, fee_pct=0.1):
    """Scan a {source: price} map and return the best opportunity.

    Gross spread = (max - min) / min * 100.
    Net spread subtracts fees on both legs (2 * fee_pct).
    """
    if len(prices) < 2:
        raise ValueError("Need at least two price sources")
    for source, price in prices.items():
        if price <= 0:
            raise ValueError(f"Price for {source} must be positive")
    buy_source = min(prices, key=prices.get)
    sell_source = max(prices, key=prices.get)
    low, high = prices[buy_source], prices[sell_source]
    gross = (high - low) / low * 100
    net = gross - 2 * fee_pct
    return {
        "buy_from": buy_source, "buy_price": low,
        "sell_to": sell_source, "sell_price": high,
        "gross_spread_pct": gross, "net_spread_pct": net,
        "fee_pct_per_leg": fee_pct,
        "opportunity": net >= threshold_pct,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Crypto arbitrage scanner")
    parser.add_argument("--prices", required=True, help="JSON map, e.g. '{\"A\": 60000, \"B\": 61200}'")
    parser.add_argument("--threshold", type=float, default=1.0, help="Minimum net spread % to flag")
    parser.add_argument("--fee-pct", type=float, default=0.1, help="Fee % per leg")
    args = parser.parse_args(argv)
    try:
        prices = {k: float(v) for k, v in json.loads(args.prices).items()}
        result = scan(prices, args.threshold, args.fee_pct)
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
