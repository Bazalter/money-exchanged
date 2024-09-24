from sqlalchemy.orm import Session
from .models import Exchanger


def create_exchanger(db: Session, value1: float,name_currency1: str,
                    value2: float, name_currency2: str,
                    value_usd: float) -> Exchanger:
    db_exchanger = Exchanger(
        value1=value1,
        name_currency1=name_currency1,
        value2=value2,
        name_currency2=name_currency2,
        value_usd=value_usd
    )
    db.add(db_exchanger)
    db.commit()
    db.refresh(db_exchanger)
    return db_exchanger
