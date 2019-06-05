from collections import defaultdict

from keras.applications.mobilenet import MobileNet
from keras.preprocessing import image

from access_niu.components import Component
from access_niu.components.input_layers import InputLayer
from access_niu.components.output_layers import OutputLayer
from access_niu.components.mobilenet_v2 import MobilenetV2ModelComponent


class DataGeneratorComponent(Component):
    def __init__(self, **kwargs):
        super(DataGeneratorComponent, self).__init__(**kwargs)

    def prepare(self, **kwargs):
        gen = image.ImageDataGenerator(rescale=1.0 / 255)

        generator = gen.flow_from_directory(
            kwargs.get("data_dir"),
            target_size=kwargs.get("image_shape")[:-1],
            batch_size=kwargs.get("batch_size"),
            shuffle=True,
        )

        labels = {v: k for k, v in generator.class_indices.items()}

        return {
            kwargs.get("generator_name"): generator,
            "labels": labels,
            kwargs.get("num_sample_name"): generator.n,
        }

    def execute(self, **kwargs):
        pass


class ComponentManager(object):
    def __init__(self):
        self.components = defaultdict(Component)
        self._load_components()

    def get(self, name):
        return self.components.get(name)

    def _load_components(self):
        self.components["mobilenet"] = MobileNet
        self.components["mobilenet_v2"] = MobilenetV2ModelComponent
        self.components["data_generator"] = DataGeneratorComponent
        self.components["input_layer"] = InputLayer
        self.components["output_layer"] = OutputLayer
