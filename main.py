from fastapi import FastAPI
from usd import valutes

app = FastAPI()


@app.get('/exchanger')
async def give_money(rub: float, usd: float = 0):
    return {'rub': rub, 'usd': usd}


@app.get('/exchange/{rub}/{usd}')
async def give_pupa(rub: float, usd: float):
    return {"puparub": rub, "pupausd": usd}

@app.get("/rub-usd/{rub}")
async def give_me_a_dollar(rub: float):
    return f'Ваши {rub} рублей это {rub/valutes} доллара'
