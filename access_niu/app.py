from PIL import Image
import numpy as np

from werkzeug.datastructures import FileStorage

from access_niu.infer import load_model, parse
from access_niu.train import Trainer


class NIUApp(object):
    def __init__(self, template):
        self.template = template
        self.model_dir = template.get("project").get("path")
        self.model, self.labels = load_model(self.model_dir)
        self.trainer = Trainer(template)
        # TODO: Load it at project level
        self.image_size = self._get_image_dimensions(template)

    def _get_image_dimensions(self, template):
        input_layer = template.get("pipeline")[0].get("input_layer")

        return input_layer.get("image_width"), input_layer.get("image_height")

    def parse(self, data: FileStorage) -> dict:
        """Handles the parse request.

        :param data: Image file to be parsed.
        :return: dic of the parsed response
        """
        img = Image.open(data).resize(self.image_size, Image.ANTIALIAS)
        img = np.expand_dims(np.array(img), axis=0)
        pred_arr = parse(self.model, img)
        max_idx = np.argmax(pred_arr)
        return {self.labels.get(max_idx): np.float(pred_arr[0][max_idx])}

    def train(self):
        pass
