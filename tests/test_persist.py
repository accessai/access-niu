
def test_persist():
    from access_niu.persist import save_keras_model
    from keras.models import Model
    from keras.layers import Input, Dense

    ip = Input(shape=(1,1))
    op = Dense(1)(ip)

    model = Model(inputs=[ip], outputs=[op])
    result = save_keras_model('/tmp',model, {0:'A', 1:'B'})

    assert result is True
