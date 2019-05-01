from copy import deepcopy
import argparse
import yaml

from access_niu.components.classifiers import mobilenet_v2
from access_niu import data, persist
from access_niu.pipeline import build_pipeline

from access_niu.pipeline import build_pipeline


def _create_parser():
    parser = argparse.ArgumentParser(description='access-niu parser')
    parser.add_argument('--template',
                        type=str,
                        required=True,
                        help='Project template')

    return parser.parse_args()


# with open("sample/sample_template.yml") as f:
#     config = yaml.safe_load(f)


class Trainer(object):

    def __init__(self, template):
        self.template = template
        self.pipeline = []

    def start_construction(self):
        self.pipeline = build_pipeline(template)

    def train(self):

        kwargs = self.template

        for component in self.pipeline:
            result = component.execute(**kwargs)
            if result is not None:
                kwargs.update(result)

    def persist(self):
        kwargs = self.template
        for component in self.pipeline:
            component.persist(**kwargs)


# model = mobilenet_v2.get_model()
# model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["acc"])
# train_generator, labels, n_samples = data.data_generator(
#     config.get("data").get("train"), 224, 224
# )
#
# model.fit_generator(generator=train_generator, steps_per_epoch=n_samples / 32, epochs=5)
#
# persist.save_keras_model(config.get("project").get("path"), model, labels)


if __name__ == '__main__':
    args = _create_parser()

    with open(args.template) as f:
        template = yaml.safe_load(f)

    trainer = Trainer(template)
    trainer.start_construction()
    trainer.train()
    trainer.persist()