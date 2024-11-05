from datetime import date

from sqlalchemy.orm import Session
from .models import Exchanger, UserModel
from sql_app.models import DailyCounter as DailyCounterModel

def create_exchanger(db: Session, **kwargs) -> Exchanger:
    db_exchanger = Exchanger(**kwargs)

    db.add(db_exchanger)
    db.commit()
    db.refresh(db_exchanger)
    return db_exchanger


def update_counter(db: Session):
    today = date.today()
    counter = db.query(DailyCounterModel).filter(DailyCounterModel.count_date == today).first()

    if counter:
        counter.row_count += 1
    else:
        counter = DailyCounterModel(count_date=today, row_count=1)
        db.add(counter)
    db.commit()


def create_user(db: Session, **kwargs) -> UserModel:
    db_create_user = UserModel(**kwargs)

    db.add(db_create_user)
    db.commit()
    db.refresh(db_create_user)
    return db_create_user


def all_rows(db: Session):
    return db.query(Exchanger).all()

