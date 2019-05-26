CREATE TABLE IF NOT EXISTS fine.stocks (
  symbol VARCHAR(6) NOT NULL,
  name VARCHAR(50) NOT NULL,
  sector VARCHAR(50),
  industry VARCHAR(50),
  location VARCHAR(50),
  cik VARCHAR(50),
  source VARCHAR(50),
  daily_updated TIMESTAMP DEFAULT timestamp('1980-01-01'),
  intraday_updated TIMESTAMP DEFAULT timestamp('1980-01-01'),
  deleted TINYINT DEFAULT 0,
  PRIMARY KEY (symbol)
) ENGINE=INNODB;
