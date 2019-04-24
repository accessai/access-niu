import abc
from abc import ABCMeta


class Component(object):

    __metaclass__ = ABCMeta

    def __init__(self, comp_config):
        self.comp_config = comp_config
        self._is_enabled = (
            comp_config.get("active") if comp_config.get("active") is not None else True
        )

    @abc.abstractmethod
    def name(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def prepare(self, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def process(self, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def cleanup(self, **kwargs):
        raise NotImplementedError()

    @property
    def is_enabled(self):
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, value):
        self._is_enabled = value
