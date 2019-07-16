import yaml
import csv
import datetime
from stocks.models import Stock

names = ["nasdaq", "nyse", "amex"]
stock_keys = set()
stocks = []

for source in names:
    with open("{}.csv".format(source), "r") as file:
        reader = csv.reader(file, delimiter=',')
        next(reader, None)  # skip the headers
        for row in reader:
            if row[0] not in stock_keys:
                stock_keys.add(row[0])
                stocks.append(Stock(row[0], row[1], row[5], row[6], source))

print(stock_keys)

with open("us.stocks.yml", "w+") as file:
    file.write(yaml.dump(stocks))
