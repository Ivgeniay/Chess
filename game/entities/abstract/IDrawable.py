# from abc import ABC, abstractmethod


class IDrawable(metaclass=type):
    def draw(self, surface):
        pass
