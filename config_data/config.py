from dataclasses import dataclass
from environs import Env


@dataclass
class DatabesConfig:
    database: str
    db_host: str
    db_user: str
    db_password: str


@dataclass
class TgBot:
    bot_token: str
    admin_ids: list[int]


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabesConfig


def load_config(path: str | None) -> Config:

    env: Env = Env()
    env.read_env()

    return Config(tg_bot=TgBot(bot_token=env('BOT_TOKEN'),
                               admin_ids=list(map(int,
                                                  env.list('ADMIN_IDS')))),
                  db=DatabesConfig(database=env('DATABASE'),
                                   db_host=env('DB_HOST'),
                                   db_user=env('DB_USER'),
                                   db_password=('DB_PASSWORD')))


if __name__ == '__main__':
    load_config('.env')
