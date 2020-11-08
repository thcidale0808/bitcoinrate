from api.bitcoinrate import views
from api.bitcoinrate.views import db
from sharedmodels import models, schemas
from tests import factories
from unittest.mock import patch
import pytest
from werkzeug.exceptions import NotFound


@patch.object(models.Rate, "query_latest_rate")
def test_get_rate_calls_abort(mock_query_method):
    mock_query_method.return_value = []

    with pytest.raises(NotFound):
        views.get_latest_rate()


@patch.object(models.Rate, "query_latest_rate")
def test_get_rate_calls_query(mock_query_method, app, db_session):

    rate_factory = factories.RateFactory()
    mock_query_method.return_value = [rate_factory]

    views.get_latest_rate()

    mock_query_method.assert_called_once_with(session=db.session)


@patch.object(models.Rate, "query_latest_rate")
@patch.object(schemas.RateSchema, "dump")
@patch("api.bitcoinrate.views.jsonify")
def test_get_serialised_rate_value(mock_jsonify, mock_dump, mock_query_response):

    views.get_latest_rate()
    mock_dump.assert_called_once_with(mock_query_response.return_value)


@patch("api.bitcoinrate.views.request")
@patch.object(models.Rate, "query_rate_by_date")
def test_get_rate_by_date_calls_abort(mock_query_method, mock_request):
    mock_query_method.return_value = []
    mock_request.args.get.return_value = '20201105'
    with pytest.raises(NotFound):
        views.get_rates_by_date()


@patch("api.bitcoinrate.views.request")
@patch.object(models.Rate, "query_rate_by_date")
def test_get_rate_by_date_calls_query(mock_query_method, mock_request, app, db_session):
    mock_request.args.get.return_value = '20201105'
    rate_factory = factories.RateFactory()
    mock_query_method.return_value = [rate_factory]

    views.get_rates_by_date()

    mock_query_method.assert_called_once_with(session=db.session, start_date='20201105', end_date='20201105')


@patch("api.bitcoinrate.views.request")
@patch.object(models.Rate, "query_rate_by_date")
@patch.object(schemas.RateSchema, "dump")
@patch("api.bitcoinrate.views.jsonify")
def test_get_serialised_rate_by_date_value(mock_jsonify, mock_dump, mock_query_response, mock_request):
    mock_request.args.get.return_value = '20201105'
    views.get_rates_by_date()
    mock_dump.assert_called_once_with(mock_query_response.return_value)
