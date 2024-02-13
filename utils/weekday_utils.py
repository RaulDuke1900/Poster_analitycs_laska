import calendar
from datetime import datetime, timedelta


def count_weekdays(date_from, date_to):
    # Преобразуем строки с датами в объекты datetime
    date_from = datetime.strptime(date_from, '%Y-%m-%d')
    date_to = datetime.strptime(date_to, '%Y-%m-%d')

    # Создаем словарь для хранения количества дней каждого дня недели
    weekday_counts = {'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0,
                      'Friday': 0, 'Saturday': 0, 'Sunday': 0}

    # Считаем количество дней каждого дня недели
    current_date = date_from
    while current_date <= date_to:
        weekday_name = calendar.day_name[current_date.weekday()]
        weekday_counts[weekday_name] += 1
        current_date += timedelta(days=1)

    return {weekday: 1 if count == 0 else count
            for weekday, count in weekday_counts.items()}


if __name__ == '__main__':
    # Примеры использования функции
    result_custom = count_weekdays('2024-01-01', '2024-01-31')
    print(result_custom)
