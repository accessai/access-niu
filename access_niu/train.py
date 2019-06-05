import os
import argparse
import yaml
from copy import deepcopy

from access_niu.pipeline import build_pipeline


def _create_parser():
    parser = argparse.ArgumentParser(description="access-niu parser")
    parser.add_argument("--template", type=str, required=True, help="Project template")

    return parser.parse_args()


class Trainer(object):
    """Trainer class
    """

    def __init__(self, template):
        self.orig_template = deepcopy(template)
        self.template = template
        self.pipeline = []

    def start_construction(self):
        """Builds the pipeline from given template.
        """
        self.pipeline = build_pipeline(self.template)

        return self

    def train(self):
        """Trains the model using the constructed pipeline.
        """

        kwargs = self.template

        for component in self.pipeline:
            result = component.run(**kwargs)
            if result is not None and type(result) == dict:
                kwargs.update(result)

        return self

    def persist(self):
        """ Saves the trained model.
        """

        kwargs = self.template
        for component in self.pipeline:
            component.persist(**kwargs)

        with open(
            os.path.join(kwargs.get("project").get("path"), "template.yml"), "w"
        ) as f:
            yaml.safe_dump(self.orig_template, f)

        return kwargs.get("project").get("name"), kwargs.get("project").get("path")


if __name__ == "__main__":
    args = _create_parser()

    with open(args.template) as f:
        template = yaml.safe_load(f)

    trainer = Trainer(template)
    trainer.start_construction()
    trainer.train()
    trainer.persist()
