from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

from sharedmodels.models import Rate


class RateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Rate
        include_relationships = False
        include_fk = True

    id = fields.Integer(as_string=True)

    source_currency = fields.String()

    target_currency = fields.String()

    value = fields.Decimal(as_string=True)

    currency_datetime = fields.DateTime()
