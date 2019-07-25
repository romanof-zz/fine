class Stock:
    def __init__(self, symbol, name, sector, industry, source):
        self.symbol = symbol
        self.name = name
        self.sector = sector
        self.industry = industry
        self.source = source

class Ticker:
    class Type:
        ONE_DAY  = '1d'
        ONE_HOUR = '1h'
        FIVE_MIN = '5m'
        ONE_MIN  = '1m'
        OPTIONS = "opts"

    TYPES = [Type.ONE_DAY, Type.ONE_HOUR, Type.FIVE_MIN, Type.ONE_MIN, Type.OPTIONS]

    def __init__(self, type, symbol, time, open, close, low, high, volume):
        self.type = type
        self.symbol = symbol
        self.time = time
        self.open = float(open)
        self.close = float(close)
        self.low = float(low)
        self.high = float(high)
        self.volume = int(volume)

    def __str__(self):
        return "[{s}@{t}] open: {o} close: {c} high: {h} low: {l}, vol: {v}".format(
            s=self.symbol,
            t=self.time,
            o=self.open,
            c=self.close,
            h=self.high,
            l=self.low,
            v=self.volume)

class TickerAnalysisStats:
    class Type:
        UP = "up"
        DOWN = "down"

    TYPES = [Type.UP, Type.DOWN]

    def __init__(self, ticker_result, result_frame, type):
        self.ticker_result = ticker_result
        self.result_frame = result_frame
        self.type = type
        self.sum_percent_change = 0.0
        self.percent_change = 0.0
        self.count = 0
        self.chance = 0.0
        self.extreme = 0.0

    def record_percent_change(self, percent_change):
        self.sum_percent_change += percent_change
        self.count += 1
        if self.extreme < percent_change: self.extreme = percent_change

    def update_counts(self):
        self.chance = self.count / self.ticker_result.count
        if self.count: self.percent_change = self.sum_percent_change / self.count

class TickerAnalysisResult:
    RESULT_FRAMES = [5, 10, 20]

    def __init__(self, symbol, frame, current, tickers, period, function):
        self.symbol = symbol
        self.frames = [frame] if frame else self.RESULT_FRAMES
        self.current = current
        self.period = period
        self.function = function
        self.tickers = tickers
        self.count = 0
        self.ticker_results = {}
        self.stats = {}
        for i in self.frames:
            self.stats[i] = {}
            self.stats[i][TickerAnalysisStats.Type.UP] = TickerAnalysisStats(self, i, TickerAnalysisStats.Type.UP)
            self.stats[i][TickerAnalysisStats.Type.DOWN] = TickerAnalysisStats(self, i, TickerAnalysisStats.Type.DOWN)

    def add_ticker(self, offset):
        self.ticker_results[self.count] = []
        for idx in range(offset, offset + 21):
            try:
                self.ticker_results[self.count].append(self.tickers[idx])
            except IndexError:
                break
        self.count += 1

    def empty(self):
        return len(self.ticker_results) == 0

    def calculate_stats(self):
        for k in self.ticker_results:
            for frame in self.frames:
                tset = self.ticker_results[k]
                if len(tset) <= frame: continue

                percent_change = abs(tset[frame].close - tset[0].close) / tset[0].close
                type = TickerAnalysisStats.Type.UP if tset[0].close < tset[frame].close else TickerAnalysisStats.Type.DOWN
                self.stats[frame][type].record_percent_change(percent_change)

        [self.stats[frame][type].update_counts() for type in TickerAnalysisStats.TYPES for frame in self.frames]

    def __str__(self):
        self.calculate_stats()

        ret = "\n{s} on {d} - {p}d {f} ({cnt} events) ".format(
            s=self.symbol,
            d=self.current.time,
            p=self.period,
            f=self.function,
            cnt=self.count)

        if not self.count: return ret
        for offset in self.frames:
            ret += "\n[{o}d]: ".format(o=offset)
            ret += "max: {max:.2f}%; min: -{min:.2f}%;".format(
                max=self.stats[offset][TickerAnalysisStats.Type.UP].extreme * 100,
                min=self.stats[offset][TickerAnalysisStats.Type.DOWN].extreme * 100)

            for skey in TickerAnalysisStats.TYPES:
                ret += " {key} avg: {avg:.2f}% with ({e} - {ep:.2f}%) events;".format(
                    key=skey,
                    avg=self.stats[offset][skey].percent_change * 100,
                      e=self.stats[offset][skey].count,
                     ep=self.stats[offset][skey].chance * 100)

        return ret
