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
            smbl = row[0].strip()
            if smbl.find('^') != -1 or smbl.find('.') != -1 or smbl.find('~') != -1 or smbl.find('$') != -1:
                continue
            if smbl not in stocks.keys():
                stocks[smbl] = Stock(smbl, row[1], row[5], row[6], source)
            else:
                stocks[smbl].source += ",{}".format(source)

print(stocks.keys())
print(len(stocks.keys()))

stocks = list(stocks.values())
with open("us.stocks.yml", "w+") as file:
    file.write(yaml.dump(stocks))
