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
@click.option('--source')
def prices(source):
    from application.commands.prices import PricesCommand
    return PricesCommand(source).do()


@app.cli.command('check_prices_table')
def check_price_table():
    from application.commands.check_prices_table import CheckPricesTableCommand
    return CheckPricesTableCommand().do()


@app.cli.command('moving_average')
@click.option('--order')
@click.option('--candle_duration')
def moving_average(order, candle_duration):
    from application.commands.moving_average import MovingAverageCommand
    return MovingAverageCommand(order, candle_duration).do()


@app.cli.command('deviations')
@click.option('--order')
@click.option('--candle')
@click.option('--start')
@click.option('--finish')
@click.option('--step')
def deviations(order, candle, start, finish, step):
    from application.commands.deviations import DeviationsCommand
    return DeviationsCommand(order, candle, start, finish, step).do()


@app.cli.command('analyse_deviations')
@click.option('--order')
@click.option('--candle')
@click.option('--percentage')
def deviations(order, candle, percentage):
    from application.commands.analyse_deviations import AnalyseDeviationsCommand
    return AnalyseDeviationsCommand(order, candle, percentage).do()


@app.cli.command('analyse_all_deviations')
def deviations():
    from application.commands.analyse_all_deviations import AnalyseAllDeviationsCommand
    return AnalyseAllDeviationsCommand().do()
