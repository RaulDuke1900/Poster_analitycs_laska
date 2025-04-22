from dataclasses import dataclass
from environs import Env
from utils.storage import JsonStorage

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
    chat_ids: dict[str, int]         # <— добавили
    schedule: dict[str, dict]        # <— добавили
    poster_token: str
    poster_account: str

def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path or ".env")

    # 1) Читаем .env
    tg_bot = TgBot(
        bot_token=env("BOT_TOKEN"),
        admin_ids=list(map(int, env.list("ADMIN_IDS")))
    )
    db = DatabesConfig(
        database=env("DATABASE"),
        db_host=env("DB_HOST"),
        db_user=env("DB_USER"),
        db_password=env("DB_PASSWORD")
    )

    # 2) Секретные chat_id
    chat_ids = {
        "daily_shift": env.int("DAILY_SHIFT_CHAT_ID"),
        "weekly_sales": env.int("WEEKLY_SALES_CHAT_ID"),
        "visit_report": env.int("VISIT_REPORT_CHAT_ID"),
        "weekly_staff": env.int("WEEKLY_STAFF_CHAT_ID"),
        "monthly_reports": env.int("MONTHLY_REPORTS_CHAT_ID"),
    }

    # 3) Расписания из JSON
    storage = JsonStorage()
    schedule = storage.load_settings()

    # 5) Poster‑параметры из .env
    poster_token = env("POSTER_TOKEN")
    poster_account = env("POSTER_ACCOUNT")  

    return Config(
        tg_bot=tg_bot,
        db=db,
        chat_ids=chat_ids,
        schedule=schedule,
        poster_token=poster_token,
        poster_account=poster_account
   
    )

if __name__ == "__main__":
    cfg = load_config()
    print(cfg)
