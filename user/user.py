import pickle
from typing import Dict, List
from pydantic import BaseModel, validator

from poster.api import Url, PosterRequest, SalesManager
from poster.api import CategoryManager, EmployeesManager, AnaliticsManager, CashShiftsManager
from poster.models import CashShiftsModel, CashShiftsTransactionsModel
from bot.static_message import hourly_period_revenue_exeption

class HourlyRevenuePeriod(BaseModel):
    start_first: int = 0
    end_first: int = 8
    start_second: int = 8
    end_second: int = 12
    start_third: int = 12
    end_third: int = 16
    start_fourth: int = 16
    end_fourth: int = 24

    @validator("start_first", "end_first", "start_second", "end_second", 
               "start_third", "end_third", "start_fourth", "end_fourth")
    def check_range(cls, value):
        if value < 0 or value > 24:
            raise ValueError(f"Переделать на отправку сообщения {hourly_period_revenue_exeption}")
        return value


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
        self.category_mapping: dict[str, tuple[str, str]] = (
            self.built_category_mapping()
            )
        self.hourly_revenue_period: BaseModel = HourlyRevenuePeriod()

    def get_settings(self) -> Dict:
        return PosterRequest.get(url=Url.get_all_settings, params=self.params)

    def get_spots(self) -> Dict:
        response = PosterRequest.get(url=Url.spots, params=self.params)
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

    def get_application_info(self, params: dict) -> dict:
        return PosterRequest.get(Url.application_get_info, params)


if __name__ == '__main__':
    from environs import Env
    env = Env()
    env.read_env()
    laska = User(token=env('POSTER_TOKEN'), account_number='laska')
    laska.save_object_to_file(f'{laska.account_number}.pkl')
    laska: User = User.load_from_file('laska.pkl')
    print(laska.tg_id, laska.account_number)
    # pprint(laska.get_cash_shift_transactions(laska.params, 2993))
