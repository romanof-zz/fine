import datetime

class TickerAnalysisResult:
    def __init__(self, tickers):
        self.tickers = tickers
        self.count = 0
        self.frames = [1, 3, 7, 14, 30]
        self.stats = {}
        for i in self.frames:
            self.stats[i] = TickerAnalysisStats()

    def __str__(self):
        ret = "total event count: {cnt}\n".format(cnt=self.count)
        for offset in self.frames:
            ret += "changes after {o} days:\n".format(o=offset)
            ret += "  higher: avg price change: {hpp:.2f}%; with events: {he} ({hep:.2f}%)\n".format(
                hpp=self.stats[offset].sum_hi_percent_change / self.stats[offset].hi_count * 100,
                he=self.stats[offset].hi_count,
                hep=self.stats[offset].hi_count / self.count * 100)
            ret += "  lower: avg price change: {lpp:.2f}%; with events: {le} ({lep:.2f}%)\n".format(
                lpp=self.stats[offset].sum_lo_percent_change / self.stats[offset].lo_count * 100,
                le=self.stats[offset].lo_count,
                lep=self.stats[offset].lo_count / self.count * 100)

        return ret

class TickerAnalysisStats:
    def __init__(self):
        self.sum_lo_percent_change = 0.0
        self.sum_hi_percent_change = 0.0
        self.lo_count = 0
        self.hi_count = 0

class TickerAnalyzer:
    def __init__(self, tickers):
        tickers.sort(key=lambda t: t.date)
        self.tickers = tickers
        self.result = TickerAnalysisResult(tickers)

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
        for idx, ticker in enumerate(self.tickers):
            try:
                func_ticker = getattr(self, function)(ticker.date, int(period), field)
                result = getattr(func_ticker, field)

                if ((function == "max" and getattr(ticker, field) > result) or
                    (function == "min" and getattr(ticker, field) < result)):

                    self.result.count += 1
                    for offset in self.result.frames:
                        change = (getattr(self.tickers[idx+offset], field) - result)
                        if getattr(self.tickers[idx+offset], field) >= result:
                            self.result.stats[offset].sum_hi_percent_change += change/result
                            self.result.stats[offset].hi_count += 1
                        else:
                            self.result.stats[offset].sum_lo_percent_change += change/result
                            self.result.stats[offset].lo_count += 1

            except (IndexError, ValueError):
                next
