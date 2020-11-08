from flask import url_for

from api.app import index


def test_index(client):
    resp = client.get(url_for("index"))

    assert resp.json == {"ok": True}
