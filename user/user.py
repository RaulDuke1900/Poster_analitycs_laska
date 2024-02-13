import pickle

from api.poster import Url, ApiRequest, SalesManager
from api.poster import CategoryManager, EmployeesManager, AnaliticsManager, CashShiftsManager
from api.models import CashShiftsModel, CashShiftsTransactionsModel
from typing import Dict, List

# from pprint import pprint


class User:
    def __init__(self, token: str, account_number: str) -> None:
        self.token: str = token
        self.account_number: str = account_number
        self.tg_chats_id: list = []
        self.tg_id: str = '-875092911'  # 'Гагагаududud'
        self.params: dict[str, str] = {'token': self.token}
        self.spots: dict[str, str] = self.get_spots()
        self.main_categories: dict[str, str] = (
            self.get_main_categories()
        )
        self.category_mapping: dict[str, tuple(str, str)] = (
            self.built_category_mapping()
            )

    def get_settings(self) -> Dict:
        return ApiRequest.get(url=Url.get_all_settings, params=self.params)

    def get_spots(self) -> Dict:
        response = ApiRequest.get(url=Url.spots, params=self.params)
        return {spot['spot_id']: spot['spot_adress'] for spot in response}

    def get_main_categories(self) -> Dict:
        return CategoryManager.get_main_categories(self.params)

    def built_category_mapping(self) -> Dict[int, str]:

        self.main_categories: dict[str, str] = (
            self.get_main_categories()
        )

        category_mapping = \
            CategoryManager.built_category_mapping(self.params,
                                                   self.main_categories)
        self.category_mapping = category_mapping
        self.save_object_to_file(f'{self.account_number}.pkl')

        return category_mapping

    def save_object_to_file(self, filename: str) -> None:
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load_from_file(cls, filename: str):
        with open(filename, 'rb') as file:
            user = pickle.load(file)
        return user

    def get_sales_by_main_category(self, spot: str, date_from: str,
                                   date_to: str) -> List[Dict]:
        self.params = self.params.copy()
        self.params.update({'spot_id': spot, 'dateFrom': date_from,
                            'dateTo': date_to})
        return SalesManager.get_sales_by_main_category(self.category_mapping,
                                                       self.params)

    def get_analitics_by_spot(self, spot_id: str, date_from: str,
                              date_to: str) -> dict[str, str]:
        params_copy: dict = self.params.copy()
        params_copy.update({'id': spot_id,
                            'dateFrom': date_from,
                            'dateTo': date_to})
        return AnaliticsManager.get_analytics_by_spot(params_copy)

    def get_analytics_by_employeers(self, date_from, date_to) -> dict:
        return AnaliticsManager.get_analytics_by_employeers(self.params,
                                                            date_from,
                                                            date_to)

    def get_employees(self) -> list[dict]:
        return EmployeesManager.get_employees(self.params)

    def get_cash_shifts(self, date_from: str, date_to: str) -> list[CashShiftsModel]:
        return CashShiftsManager.get_cash_shifts(self.params,
                                                 date_from,
                                                 date_to)

    def get_cash_shift_transactions(self, params: dict, shift_id: int) -> list[CashShiftsTransactionsModel]:
        return CashShiftsManager.get_cash_shift_transactions(params, shift_id)


if __name__ == '__main__':
    # from environs import Env
    # env = Env()
    # env.read_env()
    # laska = User(token=env('POSTER_TOKEN'), account_number='laska')
    # laska.save_object_to_file(f'{laska.account_number}.pkl')
    laska: User = User.load_from_file('laska.pkl')
    print(laska.tg_id)
    # pprint(laska.get_cash_shift_transactions(laska.params, 2993))
