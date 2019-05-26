from keras.layers import Input

from access_niu.components import Component
from access_niu.utility import parse_shape


class InputLayer(Component):
    def __init__(self, **kwargs):
        super(InputLayer, self).__init__(**kwargs)
        kwargs['shape'] = parse_shape(kwargs.get('shape'))
        self.layer = Input(**kwargs)

    def name(self):
        return "input_layer"

    def prepare(self, **kwargs):
        return {self.name(): self.layer}

    def run(self, **kwargs):
        pass