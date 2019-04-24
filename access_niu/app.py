import json

from PIL import Image
import numpy as np

from access_niu.infer import load_model, parse


class NIUApp(object):

    def __init__(self, config):
        self.config = config
        self.model_dir = config.get('project').get('path')
        self.model, self.labels = load_model(self.model_dir)

    def parse(self, data):
        img = np.expand_dims(np.array(Image.open(data)), axis=0)
        pred_arr = parse(self.model, img)
        max_idx = np.argmax(pred_arr)
        return {self.labels.get(max_idx) : np.float(pred_arr[0][max_idx])}

    def train(self):
        pass