from keras.layers import Input

from access_niu.components import Component


class InputLayer(Component):
    def __init__(self, **kwargs):
        super(InputLayer, self).__init__(**kwargs)
        self.layer = Input(**kwargs)

    def name(self):
        return "input_layer"

    def prepare(self, **kwargs):
        return {self.name(): self.layer}

    def run(self, **kwargs):
        pass