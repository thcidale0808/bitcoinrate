from flask import Blueprint, jsonify, abort, request
from api.db import db
from sharedmodels.models import Rate
from sharedmodels.schemas import RateSchema


api_blueprint = Blueprint("api", __name__)


@api_blueprint.route(
    "/bitcoinrate/latest", methods=["GET"]
)
def get_latest_rate():
    """
    Endpoint to obtain all Product records
    SQLAlchemy Object response from the query is converted to JSON by a Marshmallow Schema
    :return: JSON representation of the Product Record
    :raises: 404 If no Rate is found
    """
    rate_record = Rate.query_latest_rate(session=db.session)

    if not rate_record:
        abort(
            404,
            description=f"No Rates found",
        )

    response_schema = RateSchema(many=False)
    output = response_schema.dump(rate_record)

    return jsonify(output)


@api_blueprint.route(
    "/bitcoinrate", methods=["GET"]
)
def get_rates_by_date():
    """
    Endpoint to obtain exchange rates for a date range
    SQLAlchemy Object response from the query is converted to JSON by a Marshmallow Schema
    :return: JSON representation of the Rate Record
    :raises: 404 If no Rate found
    """
    start_date = request.args.get('start_date', None)
    end_date = request.args.get('end_date', None)

    if not start_date or not end_date:
        abort(400, 'Missing mandatory parameters: start_date and/or end_date')

    rate_records = Rate.query_rate_by_date(session=db.session, start_date=start_date, end_date=end_date)

    if not rate_records:
        abort(
            404,
            description=f"No Rates found",
        )

    response_schema = RateSchema(many=True)
    output = response_schema.dump(rate_records)

    return jsonify(output)
