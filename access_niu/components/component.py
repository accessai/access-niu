import abc
from abc import ABCMeta
from collections import defaultdict

from keras.applications.mobilenet_v2 import MobileNetV2
from keras.applications.mobilenet import MobileNet
from keras.layers import Dense, Input, GlobalAveragePooling2D
from keras.models import Model
from keras.preprocessing import image

from access_niu import persist
from access_niu.components import Component


class MobilenetV2ModelComponent(Component):
    def __init__(self, **kwargs):
        super(MobilenetV2ModelComponent, self).__init__(**kwargs)
        self.image_width = 224
        self.image_height = 224
        self.channels = 3
        self.model = self._build_model(**kwargs)

    def name(self):
        return "mobilenet_v2"

    def _build_model(self, **kwargs):

        input_layer = kwargs.get('input_layer', {})
        model_layer = kwargs.get('model')
        output_layer = kwargs.get('output_layer')

        input_shape = (input_layer.get('image_width', self.image_width),
                       input_layer.get('image_height', self.image_height),
                       input_layer.get('channels', self.channels))

        base_model = MobileNetV2(
            input_shape=input_shape, **model_layer
        )
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        op = Dense(**output_layer)(x)

        for layer in base_model.layers:
            layer.trainable = False

        model = Model(inputs=[base_model], outputs=[op])

        return model

    def _compile(self, model, train):
        return model.compile(
            optimizer=train.get("optimizer"),
            loss=train.get("loss"),
            metrics=train.get("metrics"),
        )

    def execute(self, **kwargs):

        train_generator = kwargs.get("train_generator")
        n_samples = kwargs.get("n_train_samples")
        batch_size = kwargs.get("batch_size")
        epochs = kwargs.get("epochs")

        steps = n_samples // batch_size or 1

        self.model.fit_generator(
            generator=train_generator,
            steps_per_epoch=steps,
            epochs=epochs,
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
        self.components['input_layer'] = Input
        self.components['output_layer'] = Dense
