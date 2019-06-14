import yaml
import csv
import datetime
from stocks.models import Stock

stocks = []
with open("stocks.backup.csv", "r") as file:
    reader = csv.reader(file, delimiter=',')
    next(reader, None)  # skip the headers
    for row in reader:
        source = "favorites" if "favorites" in row[5] else "sp500"
        date1 = datetime.datetime(2010, 1, 1, 0, 0, 0)
        date2 = datetime.datetime(2010, 1, 1, 0, 0, 0)
        stocks.append(Stock(row[1], row[0], row[2], row[3], row[4], source, str(row[6]), date1, date2))

with open("all.yml", "w+") as file:
    file.write(yaml.dump(stocks))
