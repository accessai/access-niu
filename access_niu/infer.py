import os

from keras.models import model_from_json
from keras.models import Model
import yaml


def load_model(model_dir: str) -> [Model, dict]:
    """Loads model from json and h5py file

    :param model_dir: Path to json model file
    :return: Keras model file
    """

    with open(os.path.join(model_dir, "model.json")) as f:
        model = model_from_json(f.read())

    weights_file = os.path.join(model_dir, "model_weights.h5")
    model.load_weights(weights_file)

    # look at: https://github.com/keras-team/keras/issues/6462
    model._make_predict_function()

    with open(os.path.join(model_dir, "labels.yml")) as f:
        labels = yaml.safe_load(f)

    return model, labels


def parse(model, data):
    pred = model.predict(data, verbose=0)
    return pred
