import abc
from abc import ABCMeta


class Component(object):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        self._is_active = (
            kwargs.get("active") if kwargs.get("active") is not None else True
        )

    @abc.abstractmethod
    def name(self):
        raise NotImplementedError()

    def prepare(self, **kwargs):
        pass

    def build(self, **kwargs):
        pass

    @abc.abstractmethod
    def run(self, **kwargs):
        return NotImplementedError()

    def clean(self, **kwargs):
        pass

    def persist(self, **kwargs):
        pass

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        self._is_active = value
