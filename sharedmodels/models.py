import logging

from datetime import datetime
from sqlalchemy.schema import Sequence
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Numeric,
    and_,
    desc
)
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)

Base = declarative_base()


class Rate(Base):
    __tablename__ = "rate"
    __table_args__ = {
        "comment": "Represents an exchange rate"
    }

    id = Column(Integer, Sequence('rate_id_seq', start=1, increment=1), primary_key=True, nullable=False, comment="Rate ID")

    source_currency = Column(String, nullable=False, comment="Source currency code")

    target_currency = Column(String, nullable=False, comment="Target currency code")

    value = Column(
        Numeric,
        nullable=False,
        comment="Rate value",
    )

    currency_datetime = Column(
        DateTime,
        nullable=False,
        comment="Exchange rate date time",
    )

    last_update = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment="Last date an update",
    )

    def __repr__(self):
        return f"<Rate(Source='{self.source_currency}', Target='{self.target_currency}, Value={self.value}')>"

    @classmethod
    def create(cls, session, source_currency, target_currency, **attrs):
        """
        Creates a new rate
        it if already existing.

        :param session: SQLAlchemy session
        :param attrs: Key Value pairs of Product Fields and Values
        :return: Created/updated Product object
        """

        rate = cls(source_currency=source_currency, target_currency=target_currency)

        for attribute, value in attrs.items():
            setattr(rate, attribute, value)

        session.add(rate)

        return rate

    @classmethod
    def query_latest_rate(
            cls, session
    ):
        """
        Return the lastes exchange rate
        :param session: SQLAlchemy Session
        :return: SQLAlchemy Product Object
        """
        response = (
            session.query(cls)
                .order_by(desc('currency_datetime')).first()
        )
        return response

    @classmethod
    def query_rate_by_date(
            cls, session, start_date, end_date
    ):
        """
        :param session: SQLAlchemy Session
        :return: SQLAlchemy Product Object
        """
        response = (
            session.query(cls).filter(and_(cls.currency_datetime <= end_date, cls.currency_datetime>=start_date))
                .all()
        )
        return response