import datetime

class TickerAnalyzer:

    def __init__(self, tickers):
        tickers.sort(key=lambda t: t.date)
        self.tickers = tickers

    def max(self, date, period_in_days, field):
        start_date = date - datetime.timedelta(days=period_in_days)
        if self.tickers[0].date > start_date: raise ValueError("invalid period")
        period_list = list(filter(lambda ticker: ticker.date >= start_date and ticker.date < date, self.tickers))
        return max(period_list, key=lambda ticker: getattr(ticker, field))

    def min(self, date, period_in_days, field):
        start_date = date - datetime.timedelta(days=period_in_days)
        if self.tickers[0].date > start_date: raise ValueError("invalid period")
        period_list = list(filter(lambda ticker: ticker.date >= start_date and ticker.date < date, self.tickers))
        return min(period_list, key=lambda ticker: getattr(ticker, field))

    def analyze(self, field, period, function):
        count = 0
        count_rebound_1d = 0
        count_rebound_3d = 0
        count_rebound_7d = 0

        for idx, ticker in enumerate(self.tickers):
            try:
                func_ticker = getattr(self, function)(ticker.date, int(period), field)
                result = getattr(func_ticker, field)

                if function == "max" and getattr(ticker, field) > result:
                    count += 1
                    if getattr(self.tickers[idx+1], field) < result: count_rebound_1d += 1
                    if getattr(self.tickers[idx+3], field) < result: count_rebound_3d += 1
                    if getattr(self.tickers[idx+7], field) < result: count_rebound_7d += 1
                if function == "min" and getattr(ticker, field) < result:
                    count += 1
                    if getattr(self.tickers[idx+1], field) > result: count_rebound_1d += 1
                    if getattr(self.tickers[idx+3], field) > result: count_rebound_3d += 1
                    if getattr(self.tickers[idx+7], field) > result: count_rebound_7d += 1
            except (IndexError, ValueError):
                next

        return {
            "count": count,
            "count_rebound_1d": count_rebound_1d,
            "count_rebound_3d": count_rebound_3d,
            "count_rebound_7d": count_rebound_7d,
        }
