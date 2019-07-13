import sys
from .models import TickerAnalysisResult

class TickerAnalyzer:
    FUNCTIONS=["high", "low"]
    PERIODS= [7, 14, 30, 90, 180, 365, 365*3, 365*5]

    def __init__(self, tickers, logger, frame):
        self.logger = logger
        self.tickers = tickers
        self.frame = frame

    def high(self, tickers, start, period):
        max_high = 0
        end = start + period + 1
        if end >= len(tickers): return False
        ticker = tickers[start]

        for i in range(start + 1, end):
            if max_high < tickers[i].high:
                max_high = tickers[i].high

        self.logger.debug("== result max_high: {mh}, ticker: {t} ==".format(mh=max_high, t=ticker))
        return ticker.open < max_high and ticker.high > max_high

    def low(self, tickers, start, period):
        min_low = sys.maxsize
        end = start + period + 1
        if end >= len(tickers): return False
        ticker = tickers[start]

        for i in range(start + 1, end):
            if min_low > tickers[i].low:
                min_low = tickers[i].low

        self.logger.debug("== result min_low: {ml}, ticker: {t} ==".format(ml=min_low, t=ticker))
        return ticker.open > min_low and ticker.low < min_low

    def analyze(self, period, function):
        results = []
        periods = self.PERIODS if period is None else [period]
        functions = self.FUNCTIONS if function is None else [function]
        for stock in set(map(lambda t: t.stock, self.tickers)):
            tickers = sorted(filter(lambda t: t.stock == stock, self.tickers), key=lambda t: t.time, reverse=True)
            rtickers = list(reversed(tickers))
            results += [self.__analyze(tickers, rtickers, stock, p, f) for f in functions for p in periods]
        return list(filter(lambda r: not r.empty(), results))

    def __analyze(self, tickers, reverse, stock, period, function):
        result = TickerAnalysisResult(stock, self.frame, tickers[0], reverse, period, function)

        self.logger.debug("== analyze input: tickers={t}, period={p}, function={f}  ==".format(t=len(tickers), p=period, f=function))
        for idx, ticker in enumerate(tickers):
            extreme = getattr(self, function)(tickers, idx, int(period))
            if not extreme and idx == 0:
                self.logger.debug("== {s} {p} {f} - no hit on {d} ==".format(s=stock.symbol, p=period, f=function, d=ticker.time))
                break
            if extreme:
                self.logger.debug("== added ticker with index={i} ==".format(i=idx))
                result.add_ticker(idx)

        self.logger.debug("== result count={c} ==".format(c=result.count))
        if not result.empty(): self.logger.info(result)
        return result
