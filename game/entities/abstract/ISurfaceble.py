from abc import ABC, abstractmethod


class ISurfaceble:
    def __init__(self):
        pass

    @property
    @abstractmethod
    def surface(self):
        pass
