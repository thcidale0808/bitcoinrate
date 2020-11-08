from flask import jsonify, make_response


def error_handler(error):
    response = {
        "status": error.code,
        "message": error.description,
        "API Documentation": "link/to/docs",
    }
    return make_response(jsonify(response), error.code)
