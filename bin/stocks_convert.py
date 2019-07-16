import yaml
import csv
import datetime
from stocks.models import Stock

names = ["nasdaq", "nyse", "amex"]
stocks = {}

for source in names:
    with open("{}.csv".format(source), "r") as file:
        reader = csv.reader(file, delimiter=',')
        next(reader, None)  # skip the headers
        for row in reader:
            date1 = datetime.datetime(2010, 1, 1, 0, 0, 0)
            date2 = datetime.datetime(2010, 1, 1, 0, 0, 0)

            if row[0] not in stocks: stocks[row[0]] = Stock(row[0], row[1], row[5], row[6], source, date1, date2)

print(len(stocks))

with open("us.stocks.yml", "w+") as file:
    file.write(yaml.dump(stocks))
