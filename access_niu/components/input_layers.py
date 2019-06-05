from keras.layers import Input

from access_niu.components import Component
from access_niu.utility import parse_shape


class InputLayer(Component):
    def __init__(self, **kwargs):
        super(InputLayer, self).__init__(**kwargs)
        self.comp_kwargs = kwargs
        self.comp_kwargs["shape"] = parse_shape(kwargs.get("shape"))

    def name(self):
        return "input_layer"

    def build(self, **kwargs):
        layer = Input(**self.comp_kwargs)
        return {self.name(): layer}

    def run(self, **kwargs):
        pass
