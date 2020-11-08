from werkzeug.exceptions import NotFound
from api.bitcoinrate.error_handler import error_handler


def test_error_handler(app):

    not_found_error = NotFound()
    expected = {
        "API Documentation": "link/to/docs",
        "status": 404,
        "message": not_found_error.description,
    }

    json_response = error_handler(not_found_error).json

    assert json_response == expected
