import os

import yaml

from access_niu.utility import ensure_directory


def save_keras_model(path, model, labels):

    ensure_directory(path)

    with open(os.path.join(path, "model.json"), "w") as f:
        f.write(model.to_json())

    model.save(os.path.join(path, "model_weights.h5"))
    _save_labels(path, labels)


def _save_labels(path, labels):

    with open(os.path.join(path, "labels.yml"), "w") as f:
        yaml.safe_dump(labels, f)
