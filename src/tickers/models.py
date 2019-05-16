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

    @classmethod
    def init_daily(self, stock, row):
        return self(self.DAILY, stock, row[0], row[1], row[2], row[3], row[4], row[5], row[6])

    def __str__(self):
        return "[{s} {d}] open: {o} close: {c} high: {h} low: {l} ".format(
            s=self.stock,
            d=self.date,
            o=self.open,
            c=self.close,
            h=self.high,
            l=self.low)

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

    def __init__(self, stock, tickers, period, function):
        self.stock = stock
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

    def empty(self):
        return len(self.ticker_results) == 0

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
            ret += "{s} - {p}d {f} ({cnt} events) ".format(s=self.stock, p=self.period, f=self.function, cnt=self.count)
            if not self.count: return ret

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
