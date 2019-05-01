import argparse

from PIL import Image
import numpy as np
import yaml

from access_niu.infer import load_model, parse
from access_niu.train import Trainer


# def _create_parser():
#     parser = argparse.ArgumentParser(description='access-niu parser')
#     parser.add_argument('--template',
#                         type=str,
#                         required=True,
#                         help='Project template')
#
#     return parser.parse_args()


class NIUApp(object):
    def __init__(self, template):
        self.template = template
        self.model_dir = template.get("project").get("path")
        self.model, self.labels = load_model(self.model_dir)
        self.trainer = Trainer(template)

    def parse(self, data):
        img = np.expand_dims(np.array(Image.open(data)), axis=0)
        pred_arr = parse(self.model, img)
        max_idx = np.argmax(pred_arr)
        return {self.labels.get(max_idx): np.float(pred_arr[0][max_idx])}

    def train(self):
        pass


# if __name__ == '__main__':
#     args = _create_parser()
#
#     with open(args.get('template')) as f:
#         template = yaml.safe_load(f)
