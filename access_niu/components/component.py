import abc
from abc import ABCMeta
from collections import defaultdict

from keras.applications.mobilenet_v2 import MobileNetV2
from keras.applications.mobilenet import MobileNet
from keras.layers import Dense, Input, GlobalAveragePooling2D
from keras.models import Model
from keras.preprocessing import image

from access_niu import persist


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

    @abc.abstractmethod
    def execute(self, **kwargs):
        return NotImplementedError()

    def persist(self, **kwargs):
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
        return "mobilenet_v2"

    def _build_model(self, input_layer, pretrained_model, output_layer, misc):
        input_tensor = Input(
            shape=(
                input_layer.get("image_height"),
                input_layer.get("image_width"),
                input_layer.get("color_channels"),
            )
        )

        base_model = MobileNetV2(input_tensor=input_tensor, **pretrained_model)
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        op = Dense(**output_layer)(x)

        for layer in base_model.layers:
            layer.trainable = False

        model = Model(inputs=[input_tensor], outputs=[op])
        model.compile(
            optimizer=misc.get("optimizer"),
            loss=misc.get("loss"),
            metrics=misc.get("metrics"),
        )

        return model

    def execute(self, **kwargs):

        train_generator = kwargs.get("train_generator")
        n_samples = kwargs.get("n_train_samples")
        batch_size = kwargs.get("batch_size")
        epochs = kwargs.get("epochs")

        self.model.fit_generator(
            generator=train_generator,
            steps_per_epoch=n_samples // batch_size, #TODO: handle case when steps_per_epoch==0
            epochs=epochs
        )

    def persist(self, **kwargs):

        labels = kwargs.get("labels")
        persist.save_keras_model(kwargs.get("project").get("path"), self.model, labels)


class DataGeneratorComponent(Component):
    def __init__(self, **kwargs):
        super(DataGeneratorComponent, self).__init__(**kwargs)

    def prepare(self, **kwargs):
        gen = image.ImageDataGenerator(rescale=1.0 / 255)

        generator = gen.flow_from_directory(
            kwargs.get("data_dir"),
            target_size=(kwargs.get("image_height"), kwargs.get("image_width")),
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
