from app import AppContext

from stocks.symbols import US_SYMBOLS
from botocore.errorfactory import ClientError

app = AppContext()

missing = []
for symbol in US_SYMBOLS:
    try:
        app.s3.get(f"tickers/{symbol}/1h/2019-07-24.csv")
    except ClientError:
        missing.append(symbol)

print(missing)
print(len(missing))
