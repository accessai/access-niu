
from keras.applications.mobilenet_v2 import MobileNetV2
from keras.layers import Dense, Input, GlobalAveragePooling2D
from keras.models import Model

from access_niu.components import Component


class MobilenetV2ModelComponent(Component):
    def __init__(self, **kwargs):
        super(MobilenetV2ModelComponent, self).__init__(**kwargs)
        self.input_shape = (224,224,3)

    def name(self):
        return "mobilenet_v2"

    def prepare(self, **kwargs):

        input_layer = kwargs.get('input_layer')
        model_layer = kwargs.get('model_layer')
        base_model = MobileNetV2(input_tensor = input_layer,
            **model_layer
        )

        for layer in base_model.layers:
            layer.trainable = False

        return {'model_layer': base_model}

    def build(self, **kwargs):
        model_layer = kwargs.get('model')
        output_layer = kwargs.get('output_layer')

        if not model_layer or not output_layer:
            return RuntimeError('Essential components missing.')

        x = model_layer.output
        x = GlobalAveragePooling2D()(x)
        op = output_layer(x)

        model = Model(inputs=[model_layer.layers[0]], outputs=[op])

        return {'model': model}

    # def _build_model(self, **kwargs):
    #
    #     input_layer = kwargs.get('input_layer', {})
    #     model_layer = kwargs.get('model')
    #     output_layer = kwargs.get('output_layer')
    #
    #     if not input_layer:
    #         input_layer = Input(shape=self.input_shape)
    #
    #     base_model = MobileNetV2(
    #         input_tensor=input_layer, **model_layer
    #     )
    #     x = base_model.output
    #     x = GlobalAveragePooling2D()(x)
    #     op = Dense(**output_layer)(x)
    #
    #     for layer in base_model.layers:
    #         layer.trainable = False
    #
    #     model = Model(inputs=[base_model], outputs=[op])
    #
    #     return model

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