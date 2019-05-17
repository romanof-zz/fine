import datetime

class Ticker:
    DAILY = "daily"

    def __init__(self, type, stock, date, open, close, low, high, adj_close, volume):
        self.type = type
        self.stock = stock
        self.date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        self.open = float(open)
        self.close = float(close)
        self.low = float(low)
        self.high = float(high)
        self.adj_close = float(adj_close)
        self.volume = int(volume)

    def __str__(self):
        return "[{s} {d}] open: {o} close: {c} high: {h} low: {l} ".format(
            s=self.stock,
            d=self.date,
            o=self.open,
            c=self.close,
            h=self.high,
            l=self.low)

class TickerAnalysisStats:
    UP = "up"
    DOWN = "down"
    GROUPS = [UP, DOWN]

    def __init__(self):
        self.sum_percent_change = 0.0
        self.percent_change = 0.0
        self.count = 0
        self.chance = 0.0
        self.extreme = 0.0

class TickerAnalysisResult:
    RESULT_FRAMES = [1, 3, 7, 14, 30]

    def __init__(self, stock, tickers, period, function):
        self.stock = stock
        self.period = period
        self.function = function
        self.tickers = tickers
        self.count = 0
        self.ticker_results = {}
        self.stats = {}
        for i in self.RESULT_FRAMES:
            self.stats[i] = {}
            self.stats[i][TickerAnalysisStats.UP] = TickerAnalysisStats()
            self.stats[i][TickerAnalysisStats.DOWN] = TickerAnalysisStats()

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
            for idx in self.RESULT_FRAMES:
                tset = self.ticker_results[k]
                if len(tset) <= idx: continue

                percent_change = abs(tset[idx].adj_close - tset[0].adj_close) / tset[0].adj_close
                skey = TickerAnalysisStats.UP if tset[0].adj_close < tset[idx].adj_close else TickerAnalysisStats.DOWN

                self.stats[idx][skey].sum_percent_change += percent_change
                self.stats[idx][skey].count += 1
                if self.stats[idx][skey].extreme < percent_change:
                    self.stats[idx][skey].extreme = percent_change

        for idx in self.RESULT_FRAMES:
            for skey in TickerAnalysisStats.GROUPS:
                if self.stats[idx][skey].count:
                    self.stats[idx][skey].chance = self.stats[idx][skey].count / self.count
                    self.stats[idx][skey].percent_change = self.stats[idx][skey].sum_percent_change / self.stats[idx][skey].count

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

            for skey in TickerAnalysisStats.GROUPS:
                ret += " {key} avg: {avg:.2f}% with ({e} - {ep:.2f}%) events;".format(
                    key=skey,
                    avg=self.stats[offset][skey].percent_change * 100,
                      e=self.stats[offset][skey].count,
                     ep=self.stats[offset][skey].chance * 100)

        return ret
