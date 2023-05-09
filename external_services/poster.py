import requests
from pprint import pprint
from dataclasses import dataclass
import time


@dataclass
class Url:
    url: str = 'https://joinposter.com/api/'
    spots: str = url + 'access.getSpots'
    menu_get_category: str = url + 'menu.getCategory'
    get_categories: str = url + 'menu.getCategories'
    get_categories_sales: str = url + 'dash.getCategoriesSales'
    get_analitics: str = url + 'dash.getAnalytics'


class PosterAPI():
    spots: dict
    main_categories: dict
    params: dict = {'format': 'json'}

    def __get_response(self, url: str, params: dict):
        now = time.time()
        response: dict = requests.get(url=url,
                                      params=params).json()
        print('__get_response work', time.time()-now)
        return self.__check_response(response)

    def __check_response(self, response):
        if 'response' in response:
            return response['response']
        else:
            return response['response']

    def get_spots(self) -> dict:
        now = time.time()

        response: dict = self.__get_response(Url.spots, self.params)
        spots = dict()

        for spot in response:
            if spot['spot_id'] not in spots:
                spots.update({spot['spot_id']: spot['spot_adress']})
        print(f'get_spots work {time.time()-now}')
        return spots

    def get_main_category(self) -> dict:
        now = time.time()
        main_categories: dict = {'0': 'Головний екран'}
        main_category_level: str = '1'
        category_hidden: str = '1'

        response = self.__get_response(Url.get_categories, self.params)

        for category in response:
            if (category['level'] == main_category_level
                    and category['category_hidden'] != category_hidden
                    and category['category_name'] not in main_categories):
                main_categories.update({category['category_id']:
                                        category['category_name']})
        print(f'get_main_category work {time.time()-now}')
        return main_categories

    def find_parent_category(self, category_id: int) -> int:
        now = time.time()
        params = self.params.copy()
        params.update({'category_id': str(category_id)})

        if str(category_id) not in self.main_categories.keys():
            response = self.__get_response(Url.menu_get_category, params)
            category_id = self.find_parent_category(response['parent_category'])
        print(f'find_parent_category work {time.time()-now}')
        return category_id

    def get_categories_sales(self, spot: str,
                             date_from: str, date_to: str) -> list[dict]:
        now = time.time()
        params: dict = self.params.copy()
        params.update({'dateFrom': date_from,
                       'dateTo': date_to,
                       'spot_id': spot})
        response = requests.get(url=Url.get_categories_sales,
                                params=params).json()['response']
        print(f'get_categories_sales work {time.time()-now}')
        return response

    def get_cash_expense(self):
        pass

    def get_analitics(self, date_from: str, date_to: str):
        now = time.time()
        '''
        Возвращает список словарей, которые содержат информацию
        по точкам продаж:
        Адрес точки продаж, Средний чек, Кол-во чеков
        '''
        params: dict = self.params.copy()
        params.update({'type': 'spots', 'dateFrom': date_from,
                       'dateTo': date_to})
        analitics = []
        for spot_id in self.spots:
            params.update({'id': spot_id})

            response: dict = requests.get(url=Url.get_analitics,
                                          params=params).json()['response']

            analitics_by_spot: dict = dict()
            analitics_by_spot.update({f'***{self.spots[spot_id]}***':
                                      f'з {date_from} по {date_to}```',
                                      'Кіл-ть чеків - ':
                                      f'{response["counters"]["transactions"]}',
                                      'Cередній чек - ':
                                      f'{round(float(response["counters"]["average_receipt"]), 2)}'})

            analitics.append(analitics_by_spot)
        print(f'get_analitics work {time.time()-now}')
        return analitics


class User(PosterAPI):
    users: dict = dict({str: object})

    def __init__(self, token, account) -> None:
        self.account: str = account
        self.token: str = token
        self.params: dict = {'token': self.token}
        self.spots: dict = self.get_spots()
        self.main_categories: dict = self.get_main_category()
        self.chats_id: list[str] = []
        User.users.update({self.account: self})


laska = User(token='570849:9460992ae868397046950392537d69ed',
             account='laska')


if __name__ == '__main__':
    pprint(laska.account)
    pprint(laska.spots)
    pprint(laska.params)
    pprint(laska.main_categories)

    pprint(laska.get_analitics('2023-04-22', '2023-04-22'))
