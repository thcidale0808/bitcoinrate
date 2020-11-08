from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import logging

from api.db import db
from api.bitcoinrate.views import api_blueprint
from api.bitcoinrate.error_handler import error_handler
from sharedmodels.db import get_connection_uri

logger = logging.getLogger("api.app")

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["SQLALCHEMY_DATABASE_URI"] = get_connection_uri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

app.register_blueprint(api_blueprint, url_prefix="/v1")

app.register_error_handler(404, error_handler)


@app.route("/", methods=["GET"])
@cross_origin()
def index():
    return jsonify({"ok": True})
