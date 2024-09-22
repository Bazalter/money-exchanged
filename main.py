from typing import Annotated
from fastapi import FastAPI, Path, HTTPException, Depends
from fastapi.responses import PlainTextResponse
from datetime import date
from usd import Valutes
from sqlalchemy.orm import Session
from sql_app.models import DailyCounter as DailyCounterModel
from sql_app.schemas import ExchangerCreate
from sql_app.cryd import create_exchanger
from sql_app.database import SessionLocal, engine, Base

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)


@app.post('/ex/{value}')
async def give_exchange(
    value: Annotated[float, Path(..., ge=0)],
    ex: ExchangerCreate,
    db: Session = Depends(get_db)
):
    if value < 0:
        raise HTTPException(status_code=400, detail="Value must be greater than or equal to 0")

    exchange = Valutes(value, ex.your_currency, ex.ex_currency)
    my_salary = round(exchange.calc_salary(), 2)
    my_salary_usd = round(my_salary * exchange.valutes[ex.ex_currency]["Value"] / exchange.valutes["USD"]["Value"], 2)
    if my_salary_usd <= 1000:
        result = (f"Твоя зпка равна {my_salary} {ex.ex_currency} и это в баксах"
                f" {my_salary_usd}"
                f" очень мало, ты бич")
    elif my_salary_usd <= 2500:
        result = f"Твоя зпка равна {my_salary} {ex.ex_currency} ты не так уж и слаб, но можешь больше"
    else:
        result = f"Твоя зпка равна {my_salary} {ex.ex_currency} нам то не пизди, ты столько не зарабатываешь"
    try:
        db_exchanger = create_exchanger(
            db=db,
            value1=value,
            name_currency1=ex.your_currency,
            value2=my_salary,
            name_currency2=ex.ex_currency,
            value_usd=my_salary_usd
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating exchanger data")

    today = date.today()
    counter = db.query(DailyCounterModel).filter(DailyCounterModel.count_date == today).first()

    if counter:
        counter.row_count += 1
    else:
        counter = DailyCounterModel(count_date=today, row_count=1)
        db.add(counter)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database commit error")

    return {"result": result, "db_exchanger": db_exchanger}


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
