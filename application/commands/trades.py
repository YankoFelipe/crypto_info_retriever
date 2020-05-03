from application.modules.data_checker import DataChecker
from application.modules.trades_retriever import Retriever


class TradesCommand:
    epoch_id = 35000000

    def __init__(self, begin: str, end: str):
        self.check_inputs(begin, end)
        self.begin = begin
        self.begin_id = int(begin)
        self.end = end
        self.end_id = int(end)

    def do(self):
        if not DataChecker.has_trades():
            print("It looks like it's your first time running this command.")
            print("It is recommended to use 'begin = " + str(self.epoch_id) + "'.")
            print("Which maps to 2018.04.12, the time 0 for the interest of this project")
            print("And 'end = " + str(self.epoch_id + 1000000) + "', to get a significant amount of data.")
            input("If you are sure of your begin/end values. Then press Enter to continue...")
        print("Retrieving trades from ID " + self.begin + " to " + self.end)
        Retriever.retrieve_trades(self.begin_id, self.end_id)
        print("Done")
        print("Expected size = " + str(self.end_id - self.epoch_id))
        print("'If you want to get more trades, repeat the command using 'begin = " + self.end + "' ")

    @classmethod
    def check_inputs(cls, begin: str, end: str):
        if not begin or not end:
            print('Must provide the parameters "--begin" and "--end"')
            exit(0)

        begin_id, end_id = int(begin), int(end)
        if not isinstance(begin_id, int) or not isinstance(end_id, int):
            print('Both begin and end must be numbers')
            exit(0)
        if end_id <= begin_id:
            print('End must be bigger than begin')
            exit(0)
        if begin_id % 1000 > 0 or end_id % 1000 > 0:
            print('Both begin and end must be multiple of 1000')
            exit(0)
