from typing import Literal
from pydantic import BaseModel, SkipValidation


CurrencyType = Literal[
    "AUD", "AZN", "GBP", "AMD", "BYN", "BGN", "BRL", "HUF", "VND", "HKD", "GEL", "DKK", "AED",
    "USD", "EUR", "EGP", "INR", "IDR", "KZT", "CAD", "QAR", "KGS", "CNY", "MDL", "NZD", "NOK", "PLN", "RON", "XDR",
    "SGD", "TJS", "THB", "TRY", "TMT", "UZS", "UAH", "CZK", "SEK", "CHF", "RSD", "ZAR", "KRW", "JPY", "RUB"]


class Exchanger(BaseModel):
    # value: int | float
    your_currency: CurrencyType = "RUB"
    ex_currency: CurrencyType = "USD"

    class Config:
        arbitrary_types_allowed = True
