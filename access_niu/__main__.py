import argparse

from access_niu import wsgi
from access_niu.wsgi import flask_app
from access_niu.app import NIUApp
from access_niu import utility


def _create_parser():
    parser = argparse.ArgumentParser(description="access-niu parser")
    parser.add_argument(
        "--projects", type=str, required=False, default='./projects', help="Path to trained models directory."
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


def main():

    args = _create_parser()

    utility.ensure_directory(args.projects)

    wsgi.niu_app = NIUApp(args.projects)
    flask_app.run(host=args.host, port=args.port, debug=True)


if __name__ == "__main__":
    main()
