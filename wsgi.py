from application import create_app

app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0")

from application.modules.historical_price_generator import HistoricalPriceGenerator

from application.modules.retriever import Retriever
from application import db

db.create_all()
print('Historical price generation begin!')
HistoricalPriceGenerator().fill_table(is_resuming=True)
print('Historical price generation end!')

start_id = 241000000
end_id = 245000000
print('Retrieving trades from ' + str(start_id) + ' to ' + str(end_id))
Retriever.retrieve_trades(start_id, end_id)
print('Done. Expected size = ' + str(end_id-35000000))
