from external_services import poster
from typing import Dict, List, Union
from pprint import pprint
import time

KOP_IN_GRN = 100


def get_sales_by_spot(user: poster.User, spot: str, date_from: str,
                      date_to: str) -> Dict[str, Union[float, str]]:
    """
    Возвращает выручку в разрезе главных категорий для заданного места
    продаж.

    :param user: Объект пользователя класса Poster.
    :param spot: Идентификатор места продаж.
    :param date_from: Дата начала периода.
    :param date_to: Дата окончания периода.
    :return: Словарь с выручкой по главным категориям товаров.
    """
    sales_by_category: list = user.get_categories_sales(spot=spot,
                                                        date_from=date_from,
                                                        date_to=date_to)

    return get_sales_by_main_category(user, spot, sales_by_category)


def get_sales_by_main_category(user: poster.User, spot: str,
                               sales_by_spots: list):
    sales_by_main_category: dict = dict(spot=user.spots[spot])
    for category in user.main_categories.values():
        sales_by_main_category[category] = dict(revenue=0, count=0)

    for category in sales_by_spots:

        revenue = int(category['revenue']) / KOP_IN_GRN
        count = float(category['count'])

        main_category_id = user.find_parent_category(category['category_id'])
        main_category_name = user.main_categories[str(main_category_id)]

        sales_by_main_category[main_category_name]['revenue'] =\
            sales_by_main_category.setdefault(main_category_name,
                                              dict(revenue=0, count=0))['revenue'] + revenue

        sales_by_main_category[main_category_name]['count'] =\
            sales_by_main_category.setdefault(main_category_name,
                                              dict(revenue=0, count=0))['count'] + count

    return sales_by_main_category


def sales_by_spots_by_main_categories(user: poster.User, date_from: str,
                                      date_to: str) -> List[Dict[str, Union[float, str]]]:
    now = time.time()
    sales_by_spots_by_main_categories: list = list()
    for spot in user.spots:
        sales = get_sales_by_spot(user, spot, date_from, date_to)
        sales_by_spots_by_main_categories.append(sales)
    print(f'get_user_spot work {time.time()-now}')
    return sales_by_spots_by_main_categories


def main(account: str, date_from: str, date_to: str):
    return sales_by_spots_by_main_categories(poster.User.users[account],
                                             date_from, date_to)


if __name__ == '__main__':
    pprint(main('laska', '2023-04-01', '2023-04-21'))
