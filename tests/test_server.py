from access_niu.wsgi import flask_app


def test_flask():

    test_client = flask_app.test_client()

    context = flask_app.app_context()
    context.push()

    resp  = test_client.get('/')

    assert resp.status_code == 200
    assert resp.json == {"status": "OK"}

    context.pop()