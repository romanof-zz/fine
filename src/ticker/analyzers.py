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
        self.hi_extreme = 0.0
        self.lo_extreme = 0.0

class TickerAnalysisResult:
    RESULT_FRAMES = [1, 3, 7, 14, 30]

    def __init__(self, tickers, period, function):
        self.period = period
        self.function = function
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
                if len(tset) <= idx: continue

                percent_change = abs(tset[idx].adj_close - tset[0].adj_close) / tset[0].adj_close
                if tset[0].adj_close < tset[idx].adj_close:
                    self.stats[idx].sum_hi_percent_change += percent_change
                    self.stats[idx].hi_count += 1
                    if self.stats[idx].hi_extreme < percent_change: self.stats[idx].hi_extreme = percent_change
                else:
                    self.stats[idx].sum_lo_percent_change += percent_change
                    self.stats[idx].lo_count += 1
                    if self.stats[idx].lo_extreme < percent_change: self.stats[idx].lo_extreme = percent_change

        for idx in self.RESULT_FRAMES:
            if self.stats[idx].lo_count:
                self.stats[idx].lo_percent_change = self.stats[idx].sum_lo_percent_change / self.stats[idx].lo_count
            if self.stats[idx].hi_count:
                self.stats[idx].hi_percent_change = self.stats[idx].sum_hi_percent_change / self.stats[idx].hi_count


    def __str__(self):
        self.calculate_stats()

        ret = ""
        for offset in self.RESULT_FRAMES:
            ret += "{p}d {f} ({cnt} events) ".format(p=self.period, f=self.function, cnt=self.count)
            ret += "[{o}d]: ".format(o=offset)
            ret += "max: {max:.2f}%; min: -{min:.2f}%; ".format(
                max=self.stats[offset].hi_extreme * 100,
                min=self.stats[offset].lo_extreme * 100)
            ret += "up avg: {avg:.2f}% with ({e} - {ep:.2f}%) events; ".format(
                avg=self.stats[offset].hi_percent_change * 100,
                e=self.stats[offset].hi_count,
                ep=self.stats[offset].hi_count / self.count * 100)
            ret += "down avg: {avg:.2f}% with ({e} - {ep:.2f}%) events;\n".format(
                avg=self.stats[offset].lo_percent_change * 100,
                e=self.stats[offset].lo_count,
                ep=self.stats[offset].lo_count / self.count * 100)

        return ret

class TickerAnalyzer:
    AVAILABLE_FUNCTIONS=["high", "low"]
    AVAILABLE_PERIODS=[30,90,180,365,730]

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
        periods = self.AVAILABLE_PERIODS if period is None else [period]
        functions = self.AVAILABLE_FUNCTIONS if function is None else [function]
        return [self.__analyze(p, f) for f in functions for p in periods]

    def __analyze(self, period, function):
        result = TickerAnalysisResult(self.tickers, period, function)
        for idx, ticker in enumerate(self.tickers):
            try:
                if getattr(self, function)(ticker, int(period)): result.add_ticker(idx)
            except (ValueError):
                next
        return result
