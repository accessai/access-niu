from keras.preprocessing import utils, image


def data_generator(path, img_ht, img_wt, batch_size=32):

    gen = image.ImageDataGenerator(rescale=1.0 / 255)

    generator = gen.flow_from_directory(
        path, target_size=(img_ht, img_wt), batch_size=batch_size, shuffle=True
    )

    return generator
