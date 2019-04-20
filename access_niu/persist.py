import os


def save_keras_model(model, path):

    with open(os.path.join(path, 'model.json'), 'w') as f:
        f.write(model.to_json())

    model.save(os.path.join(path, 'model_weights.h5'))