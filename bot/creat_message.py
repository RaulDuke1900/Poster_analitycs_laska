from user.user import User
from api.models import AnalyticsBySpotModel, EmployeeStatisticModel, CashShiftsModel, CashShiftsTransactionsModel
import telebot
from utils import weekday_utils
from environs import Env
from constants import CASH_SHIFT_EXPENSE_ID, CASH_SHIFT_NOT_DELETED

env: Env = Env()
env.read_env()
token_bot = env('BOT_TOKEN_OLD')
bot = telebot.TeleBot(token=token_bot)


def creat_message_sales_by_main_categories(user: User, spot_id: str,
                                           date_from: str, date_to: str) -> str:
    sales_by_main_categories: dict = user.get_sales_by_main_category(spot_id, date_from, date_to)
    message_sales_by_main_categories: str = ''
    for category, revenue in sales_by_main_categories.items():
        message_sales_by_main_categories += f'{category} - {float(revenue):_.2f}\n'
    return message_sales_by_main_categories


def creat_messages_analitics_by_spot(user: User, date_from: str,
                                     date_to: str) -> str:

    for spot_id in user.spots.keys():
        analitics: AnalyticsBySpotModel = user.get_analitics_by_spot(spot_id,
                                                                     date_from,
                                                                     date_to)
        weekday_revenue = analitics.weekday_revenue
        hourly_revenue = analitics.hourly_revenue
        count_weekdays: dict = weekday_utils.count_weekdays(date_from, date_to)
        print(count_weekdays)
        message = f'<b>***{user.spots[spot_id]}***</b>\n'\
                  f'<b><i>з {date_from} по {date_to}</i></b>\n\n'\
                  f'Выручка - {analitics.counters.revenue:_.2f}\n'\
                  f'Кол-во чеков - {analitics.counters.transactions:_.0f}\n'\
                  f'Посетителей - {analitics.counters.visitors:_.0f}\n'\
                  f'Cредний чек - {analitics.counters.average_receipt:_.2f}\n\n'\
                  f'<b><i>Выручка по категориям</i></b>:\n'\
                  f'{creat_message_sales_by_main_categories(user, spot_id, date_from, date_to)}\n'\
                  f'<b><i>Средняя выручка по дням недели:</i></b>\n'\
                  f'Понедельник - '\
                  f'{round(weekday_revenue[1] / count_weekdays["Monday"], 2):_.2f}\n'\
                  f'Вторник - '\
                  f'{round(weekday_revenue[2] / count_weekdays["Tuesday"], 2):_.2f}\n'\
                  f'Среда - '\
                  f'{round(weekday_revenue[3] / count_weekdays["Wednesday"], 2):_.2f}\n'\
                  f'Четверг - '\
                  f'{round(weekday_revenue[4] / count_weekdays["Thursday"], 2):_.2f}\n'\
                  f'Пятница - '\
                  f'{round(weekday_revenue[5] / count_weekdays["Friday"], 2):_.2f}\n'\
                  f'Субота - '\
                  f'{round(weekday_revenue[6] / count_weekdays["Saturday"]):_.2f}\n'\
                  f'Воскресенье - '\
                  f'{round(weekday_revenue[0] / count_weekdays["Sunday"], 2):_.2f}\n\n'\
                  f'<b><i>Выручка по часам</i></b>:\n'\
                  f'C 00.00 до 08.00 - {sum(hourly_revenue[0:8]):_.2f}\n'\
                  f'C 08.00 до 12.00 - {sum(hourly_revenue[8:12]):_.2f}\n'\
                  f'C 10.00 до 11.00 - {sum(hourly_revenue[10:11]):_.2f}\n'\
                  f'C 11.00 до 12.00 - {sum(hourly_revenue[11:12]):_.2f}\n'\
                  f'C 12.00 до 16.00 - {sum(hourly_revenue[12:16]):_.2f}\n'\
                  f'C 16.00 до 20.00 - {sum(hourly_revenue[16:20]):_.2f}\n'\
                  f'C 19.00 до 20.00 - {sum(hourly_revenue[19:20]):_.2f}\n'\
                  f'C 20.00 до 00.00 - {sum(hourly_revenue[20:]):_.2f}\n'\
                  f'C 20.00 до 21.00 - {sum(hourly_revenue[20:21]):_.2f}\n\n'
        message = message.replace('_', ' ')
        bot.send_message(chat_id=user.tg_id, text=message, parse_mode="html")
        # bot.send_message(chat_id='502490414', text=message, parse_mode="html")
    return message


def creat_messages_analitics_by_employeers(user: User, date_from: str,
                                           date_to: str) -> str:
    analytics: list[EmployeeStatisticModel] = user.get_analytics_by_employeers(date_from,
                                                                               date_to)
    message: str = f'<b>Аналитика по сотрудникам за период\n'\
                   f'c {date_from} по {date_to}</b>\n\n'
    for employee in analytics:
        employee_statistic = (EmployeeStatisticModel(**employee))
        message = f'{message}'\
                  f'<b><i>{employee_statistic.name}</i></b>\n'\
                  f'Выручка - {employee_statistic.revenue:_.2f}\n'\
                  f'Средняя выручка в час - {employee_statistic.revenue_per_hour:_.2f}\n'\
                  f'Средний чек - {employee_statistic.average_check:_.2f}\n'\
                  f'Кол-во клиентов - {employee_statistic.clients:_.0f}\n'\
                  f'Отработано смен - {employee_statistic.user_total_shifts:_.0f}\n'\
                  f'Отработано {employee_statistic.worked_hours_and_minutes}\n'\
                  f'Средняя длительность смены - ' \
                  f'{employee_statistic.average_duration_per_shift} ч. \n\n'

    message = message.replace('_', ' ')
    bot.send_message(chat_id=user.tg_id, text=message, parse_mode="html")
    return message


def creat_message_cash_shift(user: User, date_from, date_to):
    cash_shifts: list[CashShiftsModel] = user.get_cash_shifts(date_from,
                                                              date_to)
    all_messages: list[str] = []
    for cash_shift in cash_shifts:
        amount_sell = cash_shift.amount_sell_cash + cash_shift.amount_sell_card
        message_sales_by_main_categories: str = creat_message_sales_by_main_categories(user, cash_shift.spot_id,
                                                                                       date_from, date_to)
        message_cash_shift_expenses: str = ''
        cash_shift_expenses: list[CashShiftsTransactionsModel] = user.get_cash_shift_transactions(user.params,
                                                                                                  cash_shift.id)
        for transaction in cash_shift_expenses:
            if transaction.type == CASH_SHIFT_EXPENSE_ID and transaction.delete == CASH_SHIFT_NOT_DELETED:
                message_cash_shift_expenses += f'{transaction.amount:_.2f} - {transaction.comment}\n'

        message: str = f'<i>{cash_shift.date_start}</i>\n'\
                       f'<b>{cash_shift.spot_name}</b>\n'\
                       f'<b><i>{cash_shift.spot_adress}</i></b>\n\n'\
                       f'<b>Продажи по категориям:</b>\n'\
                       f'{message_sales_by_main_categories}\n'\
                       f'<b>Всего - {amount_sell:_.2f}</b>\n'\
                       f'Выручка наличные - {cash_shift.amount_sell_cash:_.2f}\n'\
                       f'Выручка карта - {cash_shift.amount_sell_card:_.2f}\n\n'\
                       f'<u>Смена открыта {cash_shift.date_start}</u>\n'\
                       f'<i>{user.get_employees()[cash_shift.user_id_start]}</i>\n'\
                       f'<b>Сумма в кассе - {cash_shift.amount_start:_.2f}</b>\n\n'\
                       f'Затраты всего - {cash_shift.amount_credit:_.2f}\n'\
                       f'из них:\n'\
                       f'{message_cash_shift_expenses}\n\n'\
                       f'Прочие поступления - {cash_shift.amount_debit}\n'\
                       f'Инкассация - {cash_shift.amount_collection}\n\n'\
                       f'<u>Смена закрыта {cash_shift.date_end}</u>\n'\
                       f'<i>{user.get_employees()[cash_shift.user_id_end]}</i>\n'\
                       f'<b>Сумма в кассе - {cash_shift.amount_end:_.2f}</b>\n'

        message = message.replace('_', ' ')
        all_messages.append(message)

    for message in all_messages:
        bot.send_message(chat_id=user.tg_id, text=message, parse_mode="html")
    return all_messages


if __name__ == '__main__':
    date_from = '2024-02-01'
    date_to = '2024-02-12'
    laska: User = User.load_from_file('laska.pkl')
    # creat_messages_analitics_by_employeers(laska, date_from, date_to)
    creat_messages_analitics_by_spot(laska, date_from, date_to)
    # creat_message_cash_shift(laska, '2024-02-11', '2024-02-11')
    print(laska.tg_id)
