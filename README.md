# 🥑 Binance Client - Crypto info retriever 🥑
codename: `Skyward`

## Introduction

The present repository is the first of a 3 part project to create a crypto-currency trader bot.
This first part consist on gathering all the data needed to train the bot into stock trading.

## Accomplished tasks
- [x] Print anything periodically.
- [x] Connect to binance through the python-binance package.
- [x] Get the trade price instantaneously.
- [x] Get historical trades (ca. 20GB or 200M trades from Apr. 2018 to Apr. 2020).
- [x] Close sprint at UNIX(1590969600)
- [x] Get historical prices with a `dt` of 5 seconds.
- [x] Validate local table of historical prices.
- [x] Get maximum rise and fall for several sliding windows within the historical data.
- [x] Get instants when the price run over a several percentage compared with any moving average.
- [x] Get histograms for range [3, 3.1, 3.2, ..., 10] of rise and falls of price compare with moving average (30m, 25).
- [ ] Define new statistics for the price table.
- [x] Get historical Moving averages for any order and period.
- [ ] Define new market indicators to get.

## How to install

### Setup locale

Add this to your `~/.profile` file (or equivalent)

```bash
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
```

### Install Dependencies

```bash
brew install pipenv # required to install python dependencies
brew install postgres # required to compile psycopg2
brew cask install postgres # GUI for postgres
pipenv install
```

### Configure Postgres

```bash
psql -f setup_postgres
```

## How to run

### Add credentials

Add this in the `.env` file:

```python
API_KEY = 
SECRET_KEY = 
SYMBOL = BTCUSDT
DB_USER = test
DB_PASS = test
DB_URI = localhost
DB_PORT = 5432
FLASK_RUN_PORT = 5500
```

### Run

#### Prices
To get prices use:
```bash
pipenv run flask prices --source remote
```
the value of `--source` can be `local` or `remote`. The `local` option requires to have trades in the corresponding table and it may behave slower than the remote option.
If you already have prices it will continue from where it was left.

To check the prices table and get some metrics about it, use:
```bash
pipenv run flask check_prices_table
```

#### Moving averages
To generate a moving average use:
```bash
pipenv run flask moving_average --order <INT> --candle_duration <STR>
```
where order is the number of candle closes are being considered and candle duration can be one of the following
`['1m', '3m', '5m', '15m', '30m', '1h', '2h', '6h', '12h' '1d', '1w', '4w']`. Prices table with values is a prerequisite.

#### Deviations
To generate a deviations use:
```bash
pipenv run flask deviations --order <INT> --candle <STR> --start <FLOAT> --finish <FLOAT> --step <FLOAT>
```
where order and candle behave the same as the Moving average command, the percentages to use are `[start, start+step, ..., finish]`
Prices table and moving averages table are a prerequisite.

To analyse a single deviation type use:
```bash
pipenv run flask analyse_deviations --order <INT> --candle <STR> --percentage <FLOAT>
```
This will save a histogram in `png` format with some statistics of interest in the directory `<CURRENT_DIR>/<candle><order>` and the name `<HISTOGRAM_TYPE>_<percentage>.png`. Where the histogram type can will be monthly and weekly.

To get the histograms for all the saved deviations use:
```bash
pipenv run flask analyse_all_deviations
```

#### Trades (not in use)
To get trades use:
```bash
pipenv run flask trades --begin <INT> --end <INT>
```
Both parameters must be multiples of 1000. It is recommended to use 35000000 as the begin ID considering that it maps to 2018.04.12 (the time t_0 of this project).
