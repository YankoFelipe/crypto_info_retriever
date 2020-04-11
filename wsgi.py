from application import create_app
import click

app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0")

from application import db

db.create_all()


@app.cli.command('trades')
@click.option('--begin')
@click.option('--end')
def trades(begin, end):
    from application.commands.trades import TradesCommand
    return TradesCommand(begin, end).do()


@app.cli.command('prices')
def prices():
    from application.commands.prices import PricesCommand
    return PricesCommand().do()
