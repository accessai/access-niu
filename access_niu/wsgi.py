import os
import argparse

from flask import Flask, request, jsonify
import yaml

from access_niu.app import NIUApp


def _create_parser():
    parser = argparse.ArgumentParser(description="access-niu parser")
    parser.add_argument("--project", type=str, required=True, help="Path to trained model.")

    return parser.parse_args()


flask_app = Flask(__name__)

@flask_app.route("/")
def status():
    return {"status": "OK"}


@flask_app.route("/parse", methods=["POST"])
def parse():
    # model = request.form["model"]
    data = request.files["data"]
    resp = niu_app.parse(data)
    return jsonify(resp)


@flask_app.route("/train", methods=["POST"])
def train():
    pass


if __name__ == "__main__":
    args = _create_parser()

    with open(os.path.join(args.project, 'template.yml')) as f:
        niu_app = NIUApp(yaml.safe_load(f))

    flask_app.run(host="localhost", port=8000, debug=True)

