from flask import Flask, request, jsonify, make_response
import yaml

from access_niu.app import NIUApp

flask_app = Flask(__name__)

with open('sample/sample_config.yml') as f:
    niu_app = NIUApp(yaml.safe_load(f))


@flask_app.route("/")
def status():
    return {'status': 'OK'}


@flask_app.route("/parse", methods=['POST'])
def parse():
    model = request.form['model']
    data = request.form['data']
    niu_app.parse(data)


@flask_app.route("/train", methods=['POST'])
def train():
    pass