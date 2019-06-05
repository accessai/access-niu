import os

import yaml


def ensure_directory(path):
    os.makedirs(path, exist_ok=True)


def read_template(project_path):
    with open(os.path.join(project_path, "template.yml")) as f:
        template = yaml.safe_load(f)

    return template


def parse_shape(shape):
    shape = shape.replace(")", "").replace("(", "")
    return tuple([int(e) for e in shape.split(",")])
