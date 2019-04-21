import os
from keras.models import model_from_json
from keras.models import Model


def load_model(model_dir: str) -> Model:
    """Loads model from json and h5py file

    :param model_dir: Path to json model file
    :return: Keras model file
    """

    with open(os.path.join(model_dir,'model.json')) as f:
        model = model_from_json(f.read())

    weights_file = os.path.join(model_dir, 'model_weights.h5')
    model.load_weights(weights_file)

    return model


def parse(model, data):

    return model.predict(data, verbose=0)
