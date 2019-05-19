from access_niu.infer import load_model, parse
from access_niu.utility import read_template


class Project(object):

    def __init__(self, project_path):
        self.template = read_template(project_path)
        self.model_dir = self.template.get("project").get("path")
        self.name = self.template.get('project').get('name')
        self.model, self.labels = None, None
        self.image_size = Project._get_image_dimensions(self.template)

    @staticmethod
    def _get_image_dimensions(template):
        input_layer = template.get("pipeline")[0].get("input_layer")
        return input_layer.get("image_width"), input_layer.get("image_height")

    def load(self):
        self.model, self.labels = load_model(self.model_dir)
        return True

    def unload(self):
        del self.model
        del self.labels
        self.model, self.labels = None, None

        return True

    def parse(self, data):
        return parse(self.model, data)