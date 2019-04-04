import sys
import datetime

class TickerAnalysisStats:
    def __init__(self):
        self.sum_lo_percent_change = 0.0
        self.sum_hi_percent_change = 0.0
        self.lo_percent_change = 0.0
        self.hi_percent_change = 0.0
        self.lo_count = 0
        self.hi_count = 0
        self.hi_max = 0.0
        self.hi_min = sys.maxsize
        self.lo_max = 0.0
        self.lo_min = sys.maxsize

class TickerAnalysisResult:
    RESULT_FRAMES = [1, 3, 7, 14, 30]

    def __init__(self, tickers):
        self.tickers = tickers
        self.count = 0
        self.ticker_results = {}
        self.stats = {}
        for i in self.RESULT_FRAMES:
            self.stats[i] = TickerAnalysisStats()

    def add_ticker(self, offset):
        self.ticker_results[self.count] = []
        for idx in range(offset, offset + 31):
            try:
                self.ticker_results[self.count].append(self.tickers[idx])
            except IndexError:
                break
        self.count += 1

    def calculate_stats(self):
        for k in self.ticker_results:
            for idx in self.RESULT_FRAMES:
                tset = self.ticker_results[k]
                percent_change = abs(tset[idx].adj_close - tset[0].adj_close) / tset[0].adj_close
                if tset[0].adj_close < tset[idx].adj_close:
                    self.stats[idx].sum_hi_percent_change += percent_change
                    self.stats[idx].hi_count += 1
                    if self.stats[idx].hi_max < percent_change: self.stats[idx].hi_max = percent_change
                    if self.stats[idx].hi_min > percent_change: self.stats[idx].hi_min = percent_change
                else:
                    self.stats[idx].sum_lo_percent_change += percent_change
                    self.stats[idx].lo_count += 1
                    if self.stats[idx].lo_max < percent_change: self.stats[idx].lo_max = percent_change
                    if self.stats[idx].lo_min > percent_change: self.stats[idx].lo_min = percent_change

        for idx in self.RESULT_FRAMES:
            if self.stats[idx].lo_count:
                self.stats[idx].lo_percent_change = self.stats[idx].sum_lo_percent_change / self.stats[idx].lo_count
            if self.stats[idx].hi_count:
                self.stats[idx].hi_percent_change = self.stats[idx].sum_hi_percent_change / self.stats[idx].hi_count


    def __str__(self):
        self.calculate_stats()

        ret = "total event count: {cnt}\n".format(cnt=self.count)
        for offset in self.RESULT_FRAMES:
            ret += "changes after {o} days:\n".format(o=offset)
            ret += "  higher changes: avg: {havg:.2f}%; max: {hmax:.2f}%; min: {hmin:.2f}%; with events: {he} ({hep:.2f}%)\n".format(
                havg=self.stats[offset].hi_percent_change * 100,
                hmax=self.stats[offset].hi_max * 100,
                hmin=self.stats[offset].hi_min * 100,
                he=self.stats[offset].hi_count,
                hep=self.stats[offset].hi_count / self.count * 100)
            ret += "  lower changes: avg: -{lavg:.2f}%; max: -{lmax:.2f}%; min: -{lmin:.2f}%; with events: {le} ({lep:.2f}%)\n".format(
                lavg=self.stats[offset].lo_percent_change * 100,
                lmax=self.stats[offset].lo_max * 100,
                lmin=self.stats[offset].lo_min * 100,
                le=self.stats[offset].lo_count,
                lep=self.stats[offset].lo_count / self.count * 100)

        return ret

class TickerAnalyzer:
    def __init__(self, tickers):
        tickers.sort(key=lambda t: t.date)
        self.tickers = tickers

    def high(self, ticker, period):
        start_date = ticker.date - datetime.timedelta(days=period)
        if self.tickers[0].date > start_date: raise ValueError("invalid period")

        max_high = 0
        for t in self.tickers:
            if t.date >= start_date and t.date < ticker.date and max_high < t.high:
                max_high = t.high

        return ticker.open < max_high and ticker.high > max_high

    def low(self, ticker, period):
        start_date = ticker.date - datetime.timedelta(days=period)
        if self.tickers[0].date > start_date: raise ValueError("invalid period")

        min_low = sys.maxsize
        for t in self.tickers:
            if t.date >= start_date and t.date < ticker.date and min_low > t.low:
                min_low = t.low

        return ticker.open > min_low and ticker.low < min_low

    def analyze(self, period, function):
        result = TickerAnalysisResult(self.tickers)
        for idx, ticker in enumerate(self.tickers):
            try:
                if getattr(self, function)(ticker, int(period)): result.add_ticker(idx)
            except (ValueError):
                next
        return result
