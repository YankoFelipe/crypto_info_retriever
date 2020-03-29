from application import create_app

app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0")

from application.retriever import Retriever
from application import db

db.create_all()

start_id = 35000000
end_id = 36000000
print('Retrieving trades from ' + str(start_id) + ' to ' + str(end_id))
Retriever.retrieve_trades(start_id, end_id)
print('Done')
