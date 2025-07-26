from functools import wraps

from sqlalchemy.orm import Session


def transactional(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        db: Session | None = None

        for attr_value in self.__dict__.values():
            if hasattr(attr_value, "_db") and isinstance(
                getattr(attr_value, "_db"), Session
            ):
                db = getattr(attr_value, "_db")
                break

        if db is None:
            raise RuntimeError("No database session found in any repository.")

        try:
            result = func(self, *args, **kwargs)
            db.commit()
            return result
        except Exception as ex:
            db.rollback()
            raise ex

    return wrapper
