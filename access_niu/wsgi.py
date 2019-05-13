import os
import argparse

from flask import Flask, request, jsonify
import yaml

from access_niu.app import NIUApp


def _create_parser():
    parser = argparse.ArgumentParser(description="access-niu parser")
    parser.add_argument(
        "--project", type=str, required=True, help="Path to trained model."
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        required=False,
        help="Network interface to bind",
    )
    parser.add_argument(
        "--port", type=int, default=8000, required=False, help="Network port"
    )

    return parser.parse_args()


flask_app = Flask(__name__)


@flask_app.route("/")
def status():
    return jsonify({"status": "OK"})


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

    with open(os.path.join(args.project, "template.yml")) as f:
        niu_app = NIUApp(yaml.safe_load(f))

    flask_app.run(host=args.host, port=args.port, debug=True)
