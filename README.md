# CryptoArbitrageScanner

A Python tool that compares one asset's price across sources, finds the cheapest buy and most expensive sell, and computes the gross and net spread after fees.

## Installation

No third-party dependencies. Requires Python 3.9 or later.

## Usage

```bash
python arbitrage_scanner.py --prices '{"ExchangeA": 60000, "ExchangeB": 61200}'
```

Example output:

```json
{
  "buy_from": "ExchangeA",
  "buy_price": 60000.0,
  "sell_to": "ExchangeB",
  "sell_price": 61200.0,
  "gross_spread_pct": 2.0,
  "net_spread_pct": 1.8,
  "fee_pct_per_leg": 0.1,
  "opportunity": true
}
```

Change the threshold and fee assumptions:

```bash
python arbitrage_scanner.py --prices '{"A": 60000, "B": 61200}' --threshold 1.0 --fee-pct 0.2
```

## How it works

- Gross spread = `(max_price - min_price) / min_price * 100`.
- Net spread = `gross_spread - 2 * fee_pct`, because a round trip pays a fee on each leg.
- An opportunity is flagged only when `net_spread >= threshold`.

## Tests

```bash
python -m unittest discover -s tests -v
```

Tests use mock price data, so they run offline and need no exchange account.

## Limitations

- Price snapshots go stale fast; a spread on paper may vanish before any trade.
- Real arbitrage also faces slippage, withdrawal times, network fees, and liquidity limits, which this simple model does not cover.
- This tool only compares prices. It never trades, moves funds, or needs a private key or API key.

## License

MIT. See `LICENSE`.
