from keras.layers import Dense, Input
from keras.models import Model
from keras.applications.mobilenet_v2 import MobileNetV2

def get_model():

    input_tensor = Input(shape=(224,224,3))
    base_model = MobileNetV2(input_shape=(224,224,3), include_top=False, weights='imagenet', input_tensor=input_tensor)
    op = Dense(2, activation='softmax')(base_model.output)

    for layer in base_model.layers:
        layer.trainable=False

    model = Model(inputs=[input_tensor], outputs=[op])


    model.summary()

    return model

