from keras.applications.mobilenet_v2 import MobileNetV2
from keras.layers import Dense, Input, GlobalAveragePooling2D
from keras.models import Model

from access_niu.components import Component
from access_niu import persist


class MobilenetV2ModelComponent(Component):
    def __init__(self, **kwargs):
        super(MobilenetV2ModelComponent, self).__init__(**kwargs)
        self.input_shape = (224, 224, 3)
        self.comp_kwargs = kwargs

    def name(self):
        return "mobilenet_v2"

    def build(self, **kwargs):

        input_layer = kwargs.get("input_layer")
        output_layer = kwargs.get("output_layer")

        if output_layer is None:
            return RuntimeError("Essential components missing.")

        if input_layer is None:
            input_layer = Input(shape=self.input_shape)

        base_model = MobileNetV2(input_tensor=input_layer, **self.comp_kwargs)

        for layer in base_model.layers:
            layer.trainable = False

        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        op = output_layer(x)

        model = Model(inputs=[input_layer], outputs=[op])

        return {"model": model}

    def _compile(self, model, train):
        return model.compile(
            optimizer=train.get("optimizer"),
            loss=train.get("loss"),
            metrics=train.get("metrics"),
        )

    def run(self, **kwargs):

        train = kwargs.get("train", {})

        train_generator = kwargs.get("train_generator")
        n_samples = kwargs.get("n_train_samples")
        batch_size = train.get("batch_size", 1)
        epochs = train.get("epochs")

        steps = n_samples // batch_size or 1

        model = kwargs.get("model")

        model.compile(
            optimizer=train.get("optimizer"),
            loss=train.get("loss"),
            metrics=train.get("metrics"),
        )

        model.fit_generator(
            generator=train_generator, steps_per_epoch=steps, epochs=epochs
        )

    def persist(self, **kwargs):

        labels = kwargs.get("labels")
        persist.save_keras_model(
            kwargs.get("project").get("path"), kwargs.get("model"), labels
        )
