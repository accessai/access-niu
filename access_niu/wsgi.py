import json

from flask import Flask, request, jsonify

flask_app = Flask(__name__)
niu_app = None


@flask_app.route("/")
def status():
    return jsonify({"status": "OK"})


@flask_app.route("/parse", methods=["OPTIONS", "POST"])
def parse():
    img = request.files["data"]
    project_name = request.form.get("project_name")
    resp = niu_app.parse(project_name, img)
    return jsonify(resp)


@flask_app.route("/train", methods=["OPTIONS", "POST"])
def train():

    # data = json.loads(request.data)
    # template = data.get('template')
    # resp = niu_app.train(template)
    #
    # return jsonify(resp)
    return jsonify({"message": "Train method not implemented yet."}), 501


@flask_app.route("/load", methods=["OPTIONS", "POST"])
def load():
    data = json.loads(request.data)
    project_name = data.get("project_name")
    resp = niu_app.load(project_name)

    return jsonify(resp)


@flask_app.route("/unload", methods=["OPTIONS", "POST"])
def unload():
    data = json.loads(request.data)
    project_name = data.get("project_name")
    resp = niu_app.unload(project_name)

    return jsonify(resp)
