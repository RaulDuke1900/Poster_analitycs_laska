from pydantic import BaseModel, Field, validator
from constants import DECIMALS_IN_CURRENCY, SECONDS_IN_HOURS, SECONDS_IN_MINUTES
from config.config import load_config


class Counters(BaseModel):
    revenue: float = Field(default=0)
    transactions: int = Field(default=0)
    visitors: int = Field(default=0)
    average_receipt: float = Field(default=0)
    average_time: float = Field(default=0)


class AnalyticsBySpotModel(BaseModel):
    counters: Counters = Field(default_factory=Counters)
    daily_revenue: list[float] = Field(alias='data', default=[])
    hourly_revenue: list[float] = Field(alias='data_hourly',
                                        default=[0 for i in range(24)])
    weekday_revenue: list[float] = Field(alias='data_weekday',
                                         default=[0 for i in range(7)])

    @validator('counters', pre=True, allow_reuse=True)
    def convert_floats(cls, counters):
        for key in ['average_receipt', 'average_time', 'revenue']:
            if key in counters:
                counters[key] = round(float(counters[key]), 2)
        return counters

    @validator('daily_revenue', 'hourly_revenue', 'weekday_revenue',
               pre=True, allow_reuse=True)
    def convert_list_of_floats(cls, values):
        return [round(float(value), 2) for value in values]


class EmployeeStatisticModel(BaseModel):
    user_id: int = Field(default=None)
    name: str = Field(default=None)
    user_total_shifts: int = Field(alias='count_us', default=0)
    revenue: float = Field(default=0)
    clients: int = Field(default=0)
    average_check: float = Field(default=0)
    worked_hours_and_minutes: str = Field(alias='worked_time', default=0)
    worked_hours: float = Field(alias='worked_time', default=0)
    revenue_per_hour: float = Field(alias='worked_time')
    average_duration_per_shift: float = Field(alias='worked_time')

    @validator('user_total_shifts', pre=True, allow_reuse=True)
    def chek_user_shifts(cls, shifts):
        if shifts is None:
            return 0
        return shifts

    @validator('revenue', pre=True, allow_reuse=True)
    def convert_to_higher_currency_unit(cls, amount):
        return round(int(amount) / DECIMALS_IN_CURRENCY, 2)

    @validator('worked_hours_and_minutes', pre=True, allow_reuse=True)
    def convert_to_hours_and_minutes(cls, seconds):
        if seconds is None:
            seconds = 0
        hours = int(seconds) // SECONDS_IN_HOURS
        minutes = (int(seconds) % SECONDS_IN_HOURS) // SECONDS_IN_MINUTES
        return f'{hours} ч. {minutes} мин.'

    @validator('worked_hours', pre=True, allow_reuse=True)
    def convert_to_minutes(cls, seconds):
        if seconds is None:
            seconds = 0
        hours = int(seconds) / SECONDS_IN_HOURS
        return round(hours, 2)

    @validator('revenue_per_hour', pre=True, allow_reuse=True)
    def count_revenue_per_hour(cls, _, values: dict):
        revenue: float = values.get('revenue', 0)
        worked_hours: float = values.get('worked_hours', 1)
        if worked_hours is None or worked_hours == 0:
            return 0
        return round(revenue / worked_hours, 2)

    @validator('average_duration_per_shift', pre=True, allow_reuse=True)
    def count_average_duration_per_shift(cls, value, values: dict):
        worked_hours = values.get('worked_hours', 0)
        user_total_shifts = values.get('user_total_shifts', 1)
        if user_total_shifts == 0:
            return 0
        return round(worked_hours / user_total_shifts, 2)


class CashShiftsModel(BaseModel):
    amount_collection: float = Field(default=0)    # сумма инкассаций
    amount_debit: float = Field(default=0)         # сумма доходов
    amount_credit: float = Field(default=0)        # сумма расходов
    amount_sell_card: float = Field(default=0)     # сумма выручки картой
    amount_sell_cash: float = Field(default=0)     # сумма выручки наличными
    amount_start: float = Field(default=0)         # сумма в кассе на начало периода
    amount_end: float = Field(default=0)           # сумма в кассе на конец периода
    id: int = Field(alias='cash_shift_id', default=0)
    date_start: str = Field(default=0)
    date_end: str = Field(default=0)
    spot_id: int = Field(default=0)
    spot_adress: str = Field(default=0)
    spot_name: str = Field(default=0)
    user_id_start: int = Field(default=-1)
    user_id_end: int = Field(default=-1)

    @validator('amount_collection', 'amount_debit', 'amount_credit',
               'amount_start', 'amount_end', 'amount_sell_card',
               'amount_sell_cash', pre=True)
    def convert_to_higher_currency_unit(cls, value):
        return int(value) / DECIMALS_IN_CURRENCY

    @validator('user_id_start', 'user_id_end', pre=True)
    def check_user_id(cls, value):
        if value == '0':
            return -1
        return value


class CashShiftsTransactionsModel(BaseModel):
    comment: str
    delete: int
    amount: float = Field(alias='tr_amount')
    type: int

    @validator('amount', pre=True)
    def convert_to_higher_currency_unit(cls, value):
        return round(int(value) / DECIMALS_IN_CURRENCY, 2)


class ApplicationInfoModel(BaseModel):
    pass


if __name__ == '__main__':
    from user.user import User
    cfg = load_config()
    user = User(token=cfg.poster_token, account_number=cfg.poster_account)
