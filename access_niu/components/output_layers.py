from keras.layers import Dense

from access_niu.components import Component


class OutputLayer(Component):
    def __init__(self, **kwargs):
        super(OutputLayer, self).__init__(**kwargs)
        self.layer = Dense(**kwargs)

    def name(self):
        return "output_layer"

    def prepare(self, **kwargs):
        return {self.name(): self.layer}

    def run(self, **kwargs):
        pass