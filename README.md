# 🥑 Binance Client 🥑

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

#### Trades
To get trades use:
```bash
pipenv run flask trades --begin <INT> --end <INT>
```
Both parameters must be multiples of 1000. It is recommended to use 35000000 as the begin ID considering that it maps to 2018.04.12 (the time t_0 of this project).

#### Prices
To get prices use:
```bash
pipenv run flask prices --source <STRING>
```
where the source can be `local` or `remote`. The `local` option requires to have trades in the corresponding table.
If you already have prices it will continue from where it was left.

To check the prices table and get some metrics about it, use:
```bash
pipenv run flask check_prices_table
```
