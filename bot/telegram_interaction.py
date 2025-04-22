from aiogram import Bot
from datetime import date, timedelta
from config.config import load_config
from user.user import User
from bot.creat_message import (
    creat_message_cash_shift,
    creat_messages_analitics_by_spot,
    creat_messages_analitics_by_employeers,
)

# Загружаем единый cfg — токены, chat_ids и расписание
cfg = load_config()

async def send_daily_shift_report(bot: Bot):
    """Ежедневный отчёт по кассовым сменам за текущий день."""
    today = date.today().isoformat()
    cfg = load_config()
    user = User(token=cfg.poster_token, account_number=cfg.poster_account)
    messages = creat_message_cash_shift(user, today, today)
    for msg in messages:
        await bot.send_message(
            chat_id=cfg.chat_ids["daily_shift"],
            text=msg,
            parse_mode="html"
        )

async def send_weekly_sales_report(bot: Bot):
    """Еженедельный отчёт по продажам (понедельник–воскресенье)."""
    today = date.today()
    start = (today - timedelta(days=today.weekday())).isoformat()
    end = today.isoformat()
    cfg = load_config()
    user = User(token=cfg.poster_token, account_number=cfg.poster_account)
    text = creat_messages_analitics_by_spot(user, start, end)
    await bot.send_message(
        chat_id=cfg.chat_ids["weekly_sales"],
        text=text,
        parse_mode="html"
    )

async def send_visit_report(bot: Bot):
    """Еженедельный отчёт по посетителям (понедельник–воскресенье)."""
    today = date.today()
    start = (today - timedelta(days=today.weekday())).isoformat()
    end = today.isoformat()
    cfg = load_config()
    user = User(token=cfg.poster_token, account_number=cfg.poster_account)
    # Если у вас есть отдельная функция для отчёта по посетителям, замените ниже:
    text = creat_messages_analitics_by_spot(user, start, end)
    await bot.send_message(
        chat_id=cfg.chat_ids["visit_report"],
        text=text,
        parse_mode="html"
    )

async def send_weekly_staff_report(bot: Bot):
    """Еженедельный отчёт по сотрудникам (понедельник–воскресенье)."""
    today = date.today()
    start = (today - timedelta(days=today.weekday())).isoformat()
    end = today.isoformat()
    cfg = load_config()
    user = User(token=cfg.poster_token, account_number=cfg.poster_account)
    text = creat_messages_analitics_by_employeers(user, start, end)
    await bot.send_message(
        chat_id=cfg.chat_ids["weekly_staff"],
        text=text,
        parse_mode="html"
    )
