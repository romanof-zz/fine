from app import AppContext
import concurrent.futures

from stocks.symbols import US_SYMBOLS
from botocore.errorfactory import ClientError

app = AppContext()

def check_not_exists(symbol):
    try:
        type = '5m'
        date = '2019-07-22'
        content = app.s3.get(f"tickers/{symbol}/{type}/{date}.csv")
        return None if date in content else symbol
    except ClientError:
        return symbol

missing = []
counter = 0
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(check_not_exists, symbol) for symbol in US_SYMBOLS]
    for future in concurrent.futures.as_completed(futures):
        counter+=1
        print(counter)
        res = future.result()
        if res: missing.append(res)

print(missing)
print(len(missing))
