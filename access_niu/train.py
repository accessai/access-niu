import yaml

from access_niu.classifiers import mobilenet_v2
from access_niu import data, persist

with open("sample/sample_config.yml") as f:
    config = yaml.safe_load(f)


class Trainer(object):

    def __init__(self, template):
        self.template = template

    def construct_model(self):
        pass


model = mobilenet_v2.get_model()
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["acc"])
train_generator, labels, n_samples = data.data_generator(
    config.get("data").get("train"), 224, 224
)

model.fit_generator(generator=train_generator, steps_per_epoch=n_samples / 32, epochs=5)

persist.save_keras_model(config.get("project").get("path"), model, labels)
