from user.user import User
from poster.models import (
    AnalyticsBySpotModel,
    EmployeeStatisticModel,
    CashShiftsModel,
    CashShiftsTransactionsModel
)
from utils import weekday_utils
from constants import CASH_SHIFT_EXPENSE_ID, CASH_SHIFT_NOT_DELETED

def creat_message_sales_by_main_categories(
    user: User,
    spot_id: str,
    date_from: str,
    date_to: str
) -> str:
    sales = user.get_sales_by_main_category(spot_id, date_from, date_to)
    out = ""
    for category, revenue in sales.items():
        out += f"{category} - {float(revenue):_.2f}\n"
    return out

def creat_messages_analytics_by_spot(
    user: User,
    date_from: str,
    date_to: str
) -> list[str]:
    messages: list[str] = []
    for spot_id, spot_name in user.spots.items():
        analytics: AnalyticsBySpotModel = user.get_analitics_by_spot(spot_id, date_from, date_to)
        weekday_revenue = analytics.weekday_revenue
        hourly_revenue = analytics.hourly_revenue
        counts = weekday_utils.count_weekdays(date_from, date_to)

        text = (
            f"<b>***{spot_name}***</b>\n"
            f"<b><i>с {date_from} по {date_to}</i></b>\n\n"
            f"Выручка - {analytics.counters.revenue:_.2f}\n"
            f"Кол-во чеков - {analytics.counters.transactions:.0f}\n"
            f"Посетителей - {analytics.counters.visitors:.0f}\n"
            f"Средний чек - {analytics.counters.average_receipt:_.2f}\n\n"
            f"<b><i>Выручка по категориям</i></b>:\n"
            f"{creat_message_sales_by_main_categories(user, spot_id, date_from, date_to)}\n"
            f"<b><i>Средняя выручка по дням недели:</i></b>\n"
            f"Понедельник - {round(weekday_revenue[1]/counts['Monday'],2):_.2f}\n"
            f"Вторник - {round(weekday_revenue[2]/counts['Tuesday'],2):_.2f}\n"
            f"Среда - {round(weekday_revenue[3]/counts['Wednesday'],2):_.2f}\n"
            f"Четверг - {round(weekday_revenue[4]/counts['Thursday'],2):_.2f}\n"
            f"Пятница - {round(weekday_revenue[5]/counts['Friday'],2):_.2f}\n"
            f"Субота - {round(weekday_revenue[6]/counts['Saturday'],2):_.2f}\n"
            f"Воскресенье - {round(weekday_revenue[0]/counts['Sunday'],2):_.2f}\n\n"
            f"<b><i>Выручка по часам</i></b>:\n"
            f"C 00–08 - {sum(hourly_revenue[0:8]):_.2f}\n"
            f"C 08–12 - {sum(hourly_revenue[8:12]):_.2f}\n"
            f"C 12–16 - {sum(hourly_revenue[12:16]):_.2f}\n"
            f"C 16–20 - {sum(hourly_revenue[16:20]):_.2f}\n"
            f"C 20–00 - {sum(hourly_revenue[20:]):_.2f}\n"
        )
        messages.append(text.replace("_", " "))
    return messages

def creat_messages_analytics_by_employees(
    user: User,
    date_from: str,
    date_to: str
) -> list[str]:
    analytics = user.get_analytics_by_employeers(date_from, date_to)
    messages: list[str] = []
    header = f"<b>Аналитика по сотрудникам за период</b>\n<i>{date_from} – {date_to}</i>\n\n"
    for emp in analytics:
        stat = EmployeeStatisticModel(**emp)
        text = (
            header +
            f"<b><i>{stat.name}</i></b>\n"
            f"Выручка - {stat.revenue:_.2f}\n"
            f"Средняя выручка в час - {stat.revenue_per_hour:_.2f}\n"
            f"Средний чек - {stat.average_check:_.2f}\n"
            f"Кол-во клиентов - {stat.clients:.0f}\n"
            f"Смен - {stat.user_total_shifts:.0f}\n"
            f"Часов - {stat.worked_hours_and_minutes}\n"
            f"Средняя длительность смены - {stat.average_duration_per_shift} ч.\n"
        )
        messages.append(text.replace("_", " "))
    return messages

def creat_message_cash_shift(
    user: User,
    date_from: str,
    date_to: str
) -> list[str]:
    shifts = user.get_cash_shifts(date_from, date_to)
    messages: list[str] = []
    for shift in shifts:
        total = shift.amount_sell_cash + shift.amount_sell_card
        sales_text = creat_message_sales_by_main_categories(user, shift.spot_id, date_from, date_to)

        expenses = ""
        txs = user.get_cash_shift_transactions(user.params, shift.id)
        for tx in txs:
            if tx.type == CASH_SHIFT_EXPENSE_ID and tx.delete == CASH_SHIFT_NOT_DELETED:
                expenses += f"{tx.amount:_.2f} - {tx.comment}\n"

        text = (
            f"<i>{shift.date_start}</i>\n"
            f"<b>{shift.spot_name}</b>\n"
            f"<b><i>{shift.spot_adress}</i></b>\n\n"
            f"<b>Продажи по категориям:</b>\n{sales_text}\n"
            f"<b>Всего - {total:_.2f}</b>\n"
            f"Наличные - {shift.amount_sell_cash:.2f}\n"
            f"Карта - {shift.amount_sell_card:.2f}\n\n"
            f"<u>Открыта {shift.date_start}</u>\n"
            f"<i>{user.get_employees()[shift.user_id_start]}</i>\n"
            f"<b>В кассе - {shift.amount_start:.2f}</b>\n\n"
            f"Затраты - {shift.amount_credit:.2f}\n"
            f"{expenses}\n"
            f"Прочие - {shift.amount_debit}\n"
            f"Инкассация - {shift.amount_collection}\n\n"
            f"<u>Закрыта {shift.date_end}</u>\n"
            f"<i>{user.get_employees()[shift.user_id_end]}</i>\n"
            f"<b>В кассе - {shift.amount_end:.2f}</b>\n"
        )
        messages.append(text.replace("_", " "))
    return messages
