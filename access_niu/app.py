from access_niu.infer import load_model, parse


class NIUApp(object):

    def __init__(self, config):
        self.config = config
        self.model_dir = config.get('model_dir')
        self.model = load_model(self.model_dir)

    def parse(self, data):
        return parse(self.model, data)

    def train(self):
        pass