import datetime

class TickerAnalyzer:
    WEEKDAYS = 7

    def __init__(self, tickers):
        tickers.sort(key=lambda t: t.date)
        self.tickers = tickers

    def max(self, date, period_in_days, field):
        start_date = date - datetime.timedelta(days=period_in_days)
        if self.tickers[0].date > start_date: raise ValueError("invalid period")

        max = 0.0
        for ticker in self.tickers:
            if ticker.date >= start_date and ticker.date < date:
                value = float(getattr(ticker, field))
                if value > max: max = value

        return max

    def test_52w_max_adj_close(self):
        count = 0
        count_price_under_max_1d = 0
        count_price_under_max_3d = 0
        count_price_under_max_7d = 0

        for idx, ticker in enumerate(self.tickers):
            try:
                max = self.max(ticker.date, 52 * self.WEEKDAYS, "adj_close")
                if ticker.adj_close > max:
                    count += 1
                    if self.tickers[idx+1].adj_close < max: count_price_under_max_1d += 1
                    if self.tickers[idx+3].adj_close < max: count_price_under_max_3d += 1
                    if self.tickers[idx+7].adj_close < max: count_price_under_max_7d += 1
            except (IndexError, ValueError):
                next

        return {
            "count": count,
            "count_price_under_max_1d": count_price_under_max_1d,
            "count_price_under_max_3d": count_price_under_max_3d,
            "count_price_under_max_7d": count_price_under_max_7d,
        }
