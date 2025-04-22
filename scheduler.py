import asyncio
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from config.config import load_config
from bot.telegram_interaction import (
    send_daily_shift_report,
    send_weekly_sales_report,
    send_visit_report,
    send_weekly_staff_report,
)

async def main():
    # 1) Загружаем конфигурацию
    cfg = load_config()

    # 2) Инициализируем бота
    bot = Bot(token=cfg.tg_bot.bot_token)

    # 3) Настраиваем APScheduler с нужным часовым поясом
    scheduler = AsyncIOScheduler(timezone="Europe/Kiev")

    # 4) Расписания по из cfg.schedule и cfg.chat_ids
    # Ежедневный отчёт по сменам
    h, m = map(int, cfg.schedule["daily_shift_report"]["time"].split(":"))
    scheduler.add_job(
        send_daily_shift_report,
        CronTrigger(hour=h, minute=m),
        args=[bot],
        name="daily_shift_report"
    )

    # Еженедельные отчёты (воскресенье)
    h, m = map(int, cfg.schedule["weekly_sales_report"]["time"].split(":"))
    scheduler.add_job(
        send_weekly_sales_report,
        CronTrigger(day_of_week="sun", hour=h, minute=m),
        args=[bot],
        name="weekly_sales_report"
    )
    scheduler.add_job(
        send_visit_report,
        CronTrigger(day_of_week="sun", hour=h, minute=m),
        args=[bot],
        name="visit_report"
    )

    # Еженедельный отчёт по сотрудникам (воскресенье)
    h, m = map(int, cfg.schedule["weekly_staff_report"]["time"].split(":"))
    scheduler.add_job(
        send_weekly_staff_report,
        CronTrigger(day_of_week="sun", hour=h, minute=m),
        args=[bot],
        name="weekly_staff_report"
    )

    # Отчёты 15-го числа
    h, m = map(int, cfg.schedule["monthly_reports"]["times"]["mid_month"].split(":"))
    for fn in (send_daily_shift_report, send_weekly_sales_report, send_visit_report, send_weekly_staff_report):
        scheduler.add_job(
            fn,
            CronTrigger(day="15", hour=h, minute=m),
            args=[bot],
            name=f"{fn.__name__}_mid_month"
        )

    # Отчёты в последний день месяца
    h, m = map(int, cfg.schedule["monthly_reports"]["times"]["end_month"].split(":"))
    for fn in (send_daily_shift_report, send_weekly_sales_report, send_visit_report, send_weekly_staff_report):
        scheduler.add_job(
            fn,
            CronTrigger(day="last", hour=h, minute=m),
            args=[bot],
            name=f"{fn.__name__}_end_month"
        )

    # 5) Запуск планировщика и вечный цикл
    scheduler.start()
    print("Scheduler started")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
