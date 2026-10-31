import unittest

from arbitrage_scanner import scan


class TestArbitrage(unittest.TestCase):
    def test_spread(self):
        result = scan({"A": 60000, "B": 61200}, threshold_pct=1.0, fee_pct=0.1)
        self.assertEqual(result["buy_from"], "A")
        self.assertEqual(result["sell_to"], "B")
        self.assertAlmostEqual(result["gross_spread_pct"], 2.0)
        self.assertAlmostEqual(result["net_spread_pct"], 1.8)
        self.assertTrue(result["opportunity"])

    def test_no_opportunity(self):
        result = scan({"A": 60000, "B": 60300}, threshold_pct=1.0, fee_pct=0.1)
        self.assertFalse(result["opportunity"])

    def test_needs_two_sources(self):
        with self.assertRaises(ValueError):
            scan({"A": 60000})


if __name__ == "__main__":
    unittest.main()
