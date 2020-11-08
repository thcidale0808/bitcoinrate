import datetime as dt
import factory
from sqlalchemy.orm.scoping import scoped_session
from sharedmodels import models


sdb_session = None


def set_session(session):
    global db_session
    db_session = session


def get_session():
    return db_session


class RateFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Rate
        sqlalchemy_session = scoped_session(get_session, scopefunc=get_session)

    id = factory.Sequence(lambda n: n)
    source_currency = 'BTC'
    target_currency = 'USD'
    value = 100
    currency_datetime = dt.datetime.now()
    last_update = dt.datetime.now()
