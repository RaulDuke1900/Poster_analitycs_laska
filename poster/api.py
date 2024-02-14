import requests
import logging
from dataclasses import dataclass
from typing import Dict, List, Tuple
from urllib.parse import urljoin
from decimal import Decimal
from datetime import datetime

from poster.models import AnalyticsBySpotModel, CashShiftsModel, CashShiftsTransactionsModel
from constants import DECIMALS_IN_CURRENCY, ID_MAIN_LEVEL_IN_MAIN_MENU, NOT_FOUND_EMPLOYEE, MAIN_MENU

logging.basicConfig(filename='app.log', level=logging.ERROR)


@dataclass
class Url:
    base_url: str = 'https://joinposter.com/api/'
    get_all_settings: str = urljoin(base_url, 'settings.getAllSettings')
    spots: str = urljoin(base_url, 'access.getSpots')
    menu_get_category: str = urljoin(base_url, 'menu.getCategory')
    get_categories: str = urljoin(base_url, 'menu.getCategories')
    get_categories_sales: str = urljoin(base_url, 'dash.getCategoriesSales')
    get_analytics: str = urljoin(base_url, 'dash.getAnalytics')
    get_employees: str = urljoin(base_url, 'access.getEmployees')
    get_cash_shifts: str = urljoin(base_url, 'finance.getCashShifts')
    get_cash_shift_transaction: str = urljoin(base_url,
                                              'finance.getCashShiftTransactions')
    application_get_info: str = urljoin(base_url, 'application.getInfo')


class ApiRequest:
    @staticmethod
    def get(url: str, params: Dict) -> requests.models.Response:
        response = requests.get(url=url, params=params)
        json_response = response.json()
        # pprint(json_response['response'])
        if 'response' in json_response:
            return json_response['response']
        else:
            message: str = f'\n{datetime.now()}\n'\
                           f'Poster status code: {response.status_code}\n'\
                           f'Poster text: {response.text}\n'\
                           f'call with params {params}\n'
            print(message)
            logging.error(message)

        return {}


class EmployeesManager:
    @staticmethod
    def get_employees(params) -> dict[int: str]:
        response: list[dict] = ApiRequest.get(Url.get_employees, params)
        employees: dict = {employee['user_id']: employee['name'] for employee in response}
        employees.update({NOT_FOUND_EMPLOYEE: 'Сотрудник не найден'})
        return employees


class CategoryManager:
    @staticmethod
    def find_parent_category(main_categories: dict,
                             params: dict,
                             category_id: str) -> Tuple[str, str]:
        if str(category_id) in MAIN_MENU.keys():
            return category_id, MAIN_MENU[f'{category_id}']
        params = params.copy()
        params.update({'category_id': category_id})
        response: Dict = ApiRequest.get(Url.menu_get_category, params)
        category_id: str = str(response.get('category_id'))
        category_name: str = response.get('category_name')
        parent_category: str = response.get('parent_category')
        if category_id not in main_categories.keys():
            category_id, category_name = (
                CategoryManager.find_parent_category(main_categories, params,
                                                     parent_category)
                )
        return category_id, category_name

    @staticmethod
    def get_main_categories(params: Dict) -> Dict:
        main_categories: Dict = {}
        main_categories.update(MAIN_MENU)
        response: List[Dict] = ApiRequest.get(Url.get_categories, params)
        # pprint(response)
        for category in response:
            if category['level'] == ID_MAIN_LEVEL_IN_MAIN_MENU:
                main_categories.update({category['category_id']:
                                        category['category_name']})
        return main_categories

    @staticmethod
    def built_category_mapping(params: dict,
                               main_categories: dict) -> Dict[str, str]:
        category_mapping = {}
        params: Dict = params.copy()
        response = ApiRequest.get(Url.get_categories, params)
        for category in response:
            category_id: str = category['category_id']
            category_name: str = category['category_name']
            category_level: str = category['level']
            parent_category: tuple = (
                CategoryManager.find_parent_category(main_categories,
                                                     params, category_id)
                )
            parent_category_id: str = parent_category[0]
            parent_category_name: str = parent_category[1]
            if category_level <= ID_MAIN_LEVEL_IN_MAIN_MENU:
                category_mapping[category_id] = (category_id, category_name)
            else:
                category_mapping[category_id] = (parent_category_id,
                                                 parent_category_name)

        return category_mapping


class SalesManager:
    @staticmethod
    def get_categories_sales(params: dict) -> list[dict]:
        return ApiRequest.get(url=Url.get_categories_sales,
                              params=params)

    @staticmethod
    def get_sales_by_main_category(category_mapping: dict, params: dict) -> dict:
        categories_sales: List[Dict] = (
            SalesManager.get_categories_sales(params)
            )
        sales = {}
        for category in categories_sales:
            if category['category_id'] not in category_mapping.keys():
                name_main_category = 'Главная категория не найдена'
            else:
                name_main_category = category_mapping[str(category['category_id'])][1]
            revenue = Decimal(category['revenue']) / DECIMALS_IN_CURRENCY
            sales[name_main_category] = sales.get(name_main_category, 0) + revenue

        return {key: float(value) for key, value in sales.items()}


class AnaliticsManager:
    @staticmethod
    def get_analytics_by_spot(params: dict) -> List[Dict]:
        params: dict = params.copy()
        params.update({'type': 'spots'})
        response: ApiRequest = ApiRequest.get(url=Url.get_analytics,
                                              params=params)
        analytics_by_spot = AnalyticsBySpotModel.parse_obj(response)
        return analytics_by_spot

    @staticmethod
    def get_analytics_by_employeers(params: dict, date_from: str,
                                    date_to: str) -> dict:
        params: dict = params.copy()
        params.update({'type': 'waiters', 'dateFrom': date_from,
                       'dateTo': date_to})
        response: list[dict] = ApiRequest.get(Url.get_analytics, params)
        return response


class CashShiftsManager():
    @staticmethod
    def get_cash_shifts(params: dict, date_from: str, date_to: str) -> list[CashShiftsModel]:
        params: dict = params.copy()
        params.update({'dateFrom': date_from, 'dateTo': date_to,
                       'timezone': 'client'})
        response: list[dict] = ApiRequest.get(Url.get_cash_shifts, params)
        cash_shifts: list[CashShiftsModel] = []
        for cash_shift in response:
            cash_shifts.append(CashShiftsModel.parse_obj(cash_shift))
        return cash_shifts

    @staticmethod
    def get_cash_shift_transactions(params: dict, shift_id: int) -> list[CashShiftsTransactionsModel]:
        params: dict = params.copy()
        params.update({'shift_id': shift_id})
        response: list[dict] = ApiRequest.get(Url.get_cash_shift_transaction, params)
        cash_shift_transactions: list[CashShiftsTransactionsModel] = []
        for transaction in response:
            cash_shift_transactions.append(CashShiftsTransactionsModel.parse_obj(transaction))
        return cash_shift_transactions
