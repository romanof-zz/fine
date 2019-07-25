from app import AppContext
import concurrent.futures

from stocks.symbols import US_SYMBOLS
from botocore.errorfactory import ClientError

app = AppContext()

def check_not_exists(symbol):
    try:
        content = app.s3.get(f"tickers/{symbol}/5m/2019-07-24.csv")
        return None if '.' in content else symbol
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

print(",".join(missing))
print(len(missing))
