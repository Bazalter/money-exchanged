from typing import Annotated
from fastapi import FastAPI, Request, Path, HTTPException
from fastapi.responses import PlainTextResponse
from usd import Valutes
from schemas import Exchanger

app = FastAPI()


@app.post('/ex/{value}')
async def give_exchange(value: Annotated[int | float, Path(..., ge=0)], ex: Exchanger):
    if value < 0:
        raise HTTPException(status_code=400, detail="Value must be greater than or equal to 0")
    exchange = Valutes(value, ex.your_currency, ex.ex_currency)
    my_salary = round(exchange.calc_salary(), 2)
    my_salary_usd = round(my_salary * exchange.valutes[ex.ex_currency]["Value"] / exchange.valutes["USD"]["Value"], 2)
    if my_salary_usd <= 1000:
        return (f"Твоя зпка равна {my_salary} {ex.ex_currency} и это в баксах"
                f" {my_salary_usd}"
                f" очень мало, ты бич")
    elif my_salary_usd <= 2500:
        return f"Твоя зпка равна {my_salary} {ex.ex_currency} ты не так уж и слаб, но можешь больше"
    else:
        return f"Твоя зпка равна {my_salary} {ex.ex_currency} нам то не пизди, ты столько не зарабатываешь"


@app.get('/exchanger', response_class=PlainTextResponse)
async def give_currency():
    return Valutes.list_currency()
#
#
# @app.get('/exchange/{rub}/{usd}')
# async def give_pupa(rub: float, usd: float):
#     return {"puparub": rub, "pupausd": usd}
#
#
# @app.get("/rub-usd/{rub}")
# async def give_me_a_dollar(rub: float):
#     return f'Ваши {rub} рублей это {rub} доллара'
