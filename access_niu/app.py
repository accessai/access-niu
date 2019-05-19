import os
import logging
from typing import Dict

from PIL import Image
import numpy as np

from werkzeug.datastructures import FileStorage

from access_niu.train import Trainer
from access_niu.project import Project

logger = logging.getLogger(__name__)


class NIUApp(object):
    def __init__(self, projects_dir):
        self.projects_dir = projects_dir
        self.projects = NIUApp._get_project_list(projects_dir)

    @staticmethod
    def _get_project_list(projects_dir: str) -> Dict[str, Project]:

        project_names = os.listdir(projects_dir)

        projects = {}
        for name in project_names:
            project_path = os.path.join(projects_dir, name)
            projects[name] = NIUApp._read_project(project_path)

        return projects

    @staticmethod
    def _read_project(project_path):
        return Project(project_path)

    def _append_to_projects(self, project_name, project):
        self.projects[project_name] = project

    def parse(self, project_name: str, data: FileStorage) -> dict:
        """Handles the parse request.

        :param project_name: Name of the project.
        :param data: Image file to be parsed.
        :return: dic of the parsed response
        """

        project = self.projects.get(project_name)

        img = Image.open(data).resize(project.image_size, Image.ANTIALIAS)
        img = np.expand_dims(np.array(img), axis=0)
        pred_arr = project.parse(img)
        max_idx = np.argmax(pred_arr)
        return {project.labels.get(max_idx): np.float(pred_arr[0][max_idx])}

    def train(self, template):
        # TODO: make it asynchronous, return train id
        trainer = Trainer(template)
        project_name, saved_path = trainer.start_construction()\
            .train() \
            .persist()

        self._append_to_projects(project_name, NIUApp._read_project(saved_path))

        logger.info("Training completed. Model saved at {}".format(saved_path))
        return {'success': saved_path}

    def load(self, project_name):
        self.projects.get(project_name).load()

        return {'success': project_name}

    def unload(self, project_name):
        self.projects.get(project_name).unload()

        return {'success': project_name}