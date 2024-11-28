from datetime import datetime, timezone, timedelta
from typing import Annotated
from fastapi import FastAPI, Path, HTTPException, Depends, Header, Request, status
from fastapi.responses import PlainTextResponse

import auth.auth
# from fastapi.security import OAuth2PasswordRequestForm

from usd import Valutes
from sqlalchemy.orm import Session
from sql_app.schemas import ExchangerCreate
from auth.schemas import UserInDB, TokenData, User, Token
from sql_app.crud import create_exchanger, update_counter, create_user
from sql_app.database import SessionLocal, engine, Base
from auth.crud import get_user, get_current_user, hash_password, verify_password, authenticate_user
# from auth.crud import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, create_access_token, get_current_active_user

app = FastAPI(docs_url="/docs", redoc_url="/redoc", openapi_url="/openapi.json")
app.include_router(auth.auth.router)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


dp_dependency = Annotated[Session, Depends(get_db)]


@app.post('/ex/{value}')
async def give_exchange(
    value: Annotated[float, Path(..., ge=0)],
    ex: ExchangerCreate,
    db: dp_dependency
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

    try:
        update_counter(
            db=db
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database commit error")

    return {"result": result, "db_exchanger": db_exchanger}


@app.get('/exchanger', response_class=PlainTextResponse)
async def give_currency():
    return Valutes.list_currency()


@app.get("/user-info")
async def read_items(info: Request, user_agent: Annotated[str | None, Header()] = None):
    url = str(info.url)
    ip = info.client.host
    return {"User-agent": user_agent,
            "url": url,
            "client_ip": ip
            }


@app.post('/register/', response_model=UserInDB)
async def register_new_user(
        user_data: User,
        db: dp_dependency
):
    existing_user = get_user(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = hash_password(user_data.password)

    new_user = create_user(
        db=db,
        username=user_data.username,
        password=user_data.password,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        email=user_data.email,
        disabled=user_data.disabled
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# @app.post("/token", response_model=None)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
#                                  db: Session = Depends(get_db)
#                                  ) -> Token:
#     user = authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return Token(access_token=access_token, token_type="bearer")


# # Открытый маршрут, доступен для всех
@app.get("/public")
async def read_public():
    return {"message": "This is a public route, available to everyone."}


# # Закрытый маршрут, доступен только авторизованным пользователям

# @app.get("/private")
# async def read_private(current_user: Annotated[UserInDB, Depends(get_current_user)]):
#     return {"message": f"Hello, {current_user.username}. This is a private route, only for authorized users."}
#
#
# @app.get("/users/me/", response_model=UserInDB)
# async def read_users_me(
#         current_user: Annotated[UserInDB, Depends(get_current_active_user)]
# ):
#     return current_user



# @app.get('/exchange/{rub}/{usd}')
# async def give_pupa(rub: float, usd: float):
#     return {"puparub": rub, "pupausd": usd}
#
#
# @app.get("/rub-usd/{rub}")
# async def give_me_a_dollar(rub: float):
#     return f'Ваши {rub} рублей это {rub} доллара'
