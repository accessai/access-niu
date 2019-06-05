from keras.layers import Dense

from access_niu.components import Component


class OutputLayer(Component):
    def __init__(self, **kwargs):
        super(OutputLayer, self).__init__(**kwargs)
        self.comp_kwargs = kwargs

    def name(self):
        return "output_layer"

    def build(self, **kwargs):
        layer = Dense(**self.comp_kwargs)
        return {self.name(): layer}

    def run(self, **kwargs):
        pass
