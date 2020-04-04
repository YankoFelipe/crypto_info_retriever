from os import getenv
from os.path import join, dirname
from dotenv import load_dotenv


class Config:
    @staticmethod
    def get():
        env = getenv("FLASK_ENV")
        if env == "test":
            return TestConfig
        elif env == "development":
            return DevConfig

        return ProductionConfig


class ProductionConfig:
    dotenv_path = join(dirname(__file__), ".env")
    load_dotenv(dotenv_path)

    CACHE_TYPE = getenv("CACHE_TYPE")
    DATABASE_URI = f"postgres+psycopg2://{getenv('DB_USER')}:{getenv('DB_PASS')}@{getenv('DB_URI')}:{getenv('DB_PORT')}"
    SQLALCHEMY_DATABASE_URI = f"{DATABASE_URI}/binance_{getenv('SYMBOL').lower()}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_BINDS = {}
    FLASK_DEBUG = False


class DevConfig(ProductionConfig):
    CACHE_TYPE = "null"
    FLASK_DEBUG = True


class TestConfig(ProductionConfig):
    CACHE_TYPE = "null"
