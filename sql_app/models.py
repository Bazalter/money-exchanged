from .database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Date, Integer, Boolean
from datetime import date, datetime


class Exchanger(Base):
    __tablename__ = "exchanger"

    id: Mapped[int] = mapped_column(primary_key=True)
    value1: Mapped[float] = mapped_column(Float)
    name_currency1: Mapped[str] = mapped_column(String)
    value2: Mapped[float] = mapped_column(Float)
    name_currency2: Mapped[str] = mapped_column(String)
    value_usd: Mapped[float] = mapped_column(Float)


class DailyCounter(Base):
    __tablename__ = "daily_counter"

    count_date: Mapped[date] = mapped_column(Date, primary_key=True, default=datetime.today())
    row_count: Mapped[int] = mapped_column(Integer, default=0)


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    full_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, unique=True)
    role: Mapped[str] = mapped_column(String, server_default="user")
    disabled: Mapped[bool] = mapped_column(Boolean)
