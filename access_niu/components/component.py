import abc
from abc import ABCMeta
from collections import defaultdict

from keras.applications.mobilenet_v2 import MobileNetV2
from keras.applications.mobilenet import MobileNet
from keras.layers import Dense, Input, GlobalAveragePooling2D
from keras.models import Model


class Component(object):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        self._is_active = (
            kwargs.get("active") if kwargs.get("active") is not None else True
        )

    @abc.abstractmethod
    def name(self):
        raise NotImplementedError()

    def prepare(self, **kwargs):
        pass

    def process(self, **kwargs):
        pass

    def cleanup(self, **kwargs):
        pass

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        self._is_active = value


class MobilenetV2ModelComponent(Component):

    def __init__(self, **kwargs):
        super(MobilenetV2ModelComponent, self).__init__(**kwargs)
        self.model = self._build_model(**kwargs)

    def name(self):
        return 'mobilenet_v2'

    def _build_model(self, input_layer, pretrained_model, output_layer):
        input_tensor = Input(shape=(input_layer.get('image_height'),
                                    input_layer.get('image_width'),
                                    input_layer.get('color_channels')))

        base_model = MobileNetV2(
            input_tensor=input_tensor,
            **pretrained_model
        )
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        op = Dense(**output_layer)(x)

        for layer in base_model.layers:
            layer.trainable = False

        model = Model(inputs=[input_tensor], outputs=[op])

        return model


class ComponentManager(object):

    def __init__(self):
        self.components = defaultdict(Component)
        self._load_components()

    def get(self, name):
        return self.components.get(name)

    def _load_components(self):
        self.components['mobilenet'] = MobileNet
        self.components['mobilenet_v2'] = MobilenetV2ModelComponent
