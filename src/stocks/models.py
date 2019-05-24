class Stock:
    def __init__(self, symbol, name, sector, industry, location, source, cik, daily_updated, intraday_updated):
        self.symbol = symbol
        self.name = name
        self.sector = sector
        self.industry = industry
        self.location = location
        self.source = source
        self.cik = cik
        self.daily_updated = daily_updated
        self.intraday_updated = intraday_updated

class Ticker:
    DAILY = "daily"
    INTRADAY = "5min"

    def __init__(self, type, stock, time, open, close, low, high, adj_close, volume):
        self.type = type
        self.stock = stock
        self.time = time
        self.open = float(open)
        self.close = float(close)
        self.low = float(low)
        self.high = float(high)
        self.adj_close = float(adj_close)
        self.volume = int(volume)

    def __str__(self):
        return "[{s}@{t}] open: {o} close: {c} high: {h} low: {l}, vol: {v}".format(
            s=self.stock,
            t=self.time,
            o=self.open,
            c=self.close,
            h=self.high,
            l=self.low,
            v=self.volume)

    def to_csv(self):
        return "{},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{}".format(self.time.strftime('%Y-%m-%d %H:%M:%S'),
           self.open, self.close, self.low, self.high, self.adj_close, self.volume)

class TickerAnalysisStats:
    UP = "up"
    DOWN = "down"
    TYPES = [UP, DOWN]

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
    RESULT_FRAMES = [1, 3, 7, 14, 30]
    MIN_CONSIDERRED = 0.01

    def __init__(self, stock, current, tickers, period, function):
        self.stock = stock
        self.current = current
        self.period = period
        self.function = function
        self.tickers = tickers
        self.count = 0
        self.ticker_results = {}
        self.stats = {}
        for i in self.RESULT_FRAMES:
            self.stats[i] = {}
            self.stats[i][TickerAnalysisStats.UP] = TickerAnalysisStats(self, i, TickerAnalysisStats.UP)
            self.stats[i][TickerAnalysisStats.DOWN] = TickerAnalysisStats(self, i, TickerAnalysisStats.DOWN)

    def add_ticker(self, offset):
        self.ticker_results[self.count] = []
        for idx in range(offset, offset + 31):
            try:
                self.ticker_results[self.count].append(self.tickers[idx])
            except IndexError:
                break
        self.count += 1

    def empty(self):
        return len(self.ticker_results) == 0

    def calculate_stats(self):
        for k in self.ticker_results:
            for frame in self.RESULT_FRAMES:
                tset = self.ticker_results[k]
                if len(tset) <= frame: continue

                percent_change = abs(tset[frame].adj_close - tset[0].adj_close) / tset[0].adj_close
                type = TickerAnalysisStats.UP if tset[0].adj_close < tset[frame].adj_close else TickerAnalysisStats.DOWN
                self.stats[frame][type].record_percent_change(percent_change)

        [self.stats[frame][type].update_counts() for type in TickerAnalysisStats.TYPES for frame in self.RESULT_FRAMES]

    def to_stats_above_chance_value(self, chance_value):
        stats = []
        for frame in self.RESULT_FRAMES:
            for type in TickerAnalysisStats.TYPES:
                if (self.stats[frame][type].chance >= chance_value and
                   self.stats[frame][type].percent_change >= self.MIN_CONSIDERRED):
                    stats.append(self.stats[frame][type])
        return stats

    def __str__(self):
        self.calculate_stats()

        ret = ""
        for offset in self.RESULT_FRAMES:
            ret += "\n{s} - {p}d {f} ({cnt} events) ".format(s=self.stock, p=self.period, f=self.function, cnt=self.count)
            if not self.count: return ret

            ret += "[{o}d]: ".format(o=offset)
            ret += "max: {max:.2f}%; min: -{min:.2f}%;".format(
                max=self.stats[offset][TickerAnalysisStats.UP].extreme * 100,
                min=self.stats[offset][TickerAnalysisStats.DOWN].extreme * 100)

            for skey in TickerAnalysisStats.TYPES:
                ret += " {key} avg: {avg:.2f}% with ({e} - {ep:.2f}%) events;".format(
                    key=skey,
                    avg=self.stats[offset][skey].percent_change * 100,
                      e=self.stats[offset][skey].count,
                     ep=self.stats[offset][skey].chance * 100)

        return ret
