import os
from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')))


DATABASE = {
    'database': os.environ.get('POSTGRES_DB', 'default_db_name'),
    'user': os.environ.get('POSTGRES_USER', 'default_user'),
    'password': os.environ.get('POSTGRES_PASSWORD', 'default_password'),
    'host': os.environ.get('POSTGRES_HOST', 'default_host'),
    'port': os.environ.get('POSTGRES_PORT', 'default_port'),
}
