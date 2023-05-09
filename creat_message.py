import sales
from datetime import datetime
import time


def creat_messages_sales(account: str, date_from: str,
                         date_to: str) -> list[str]:
    now = time.time()
    realization = sales.main(account, date_from, date_to)
    alignment_revenue = max(list(map(len, realization[0].keys())))
    list_message = []


    for spot in realization:

        message = 'Точка продажу'
        message = f'{message.ljust(alignment_revenue)} {spot["spot"]}\n'
        message = f'{message}Продажі з {date_from} по {date_to}\n\n'
        for key, value in sorted(spot.items()):

            if key != 'spot':
                revenue = f'{value["revenue"]:_}'
                message = f'{message}{key}{" " * (alignment_revenue - len(key))} {revenue } грн.'
                message = f'{message} {" " * (15)} {str(value["count"])} од. \n'

        total_sum = sum([i['revenue'] for i in spot.values() if type(i) != str])
        total_count = sum([i['count'] for i in spot.values() if type(i) != str])
        message += f'\nВсього{" " * (alignment_revenue - 6)} {total_sum:_} грн.'
        message += f' {" " * (15)} {total_count} од.'
        list_message.append(message)

        message = ''

    message = f'{realization}'
    print(f'creat_messages_sales WORK {time.time()-now}')
    return list_message


def creat_message_cash_shifts():
    pass


def creat_message_analitics():
    pass


def creat_message():
    pass


if __name__ == '__main__':
    messages = creat_messages_sales('laska', '2023-05-08', '2023-05-08')
    for mes in messages:
        print(mes)
        print()
