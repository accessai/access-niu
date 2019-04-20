
import yaml

from access_niu.classifiers import mobilenet_v2
from access_niu import data, persist

with open('sample/sample_config.yml') as f:
    config = yaml.safe_load(f)

model = mobilenet_v2.get_model()
model.compile(optimizer='adam',loss='categorical_crossentropy', metrics=['acc'])
train_generator = data.data_generator(config.get('data').get('train'),224,224)

model.fit_generator(generator=train_generator, steps_per_epoch=888/32 ,epochs=5)

persist.save_keras_model(model,config.get('project').get('path'))