from game.entities.abstract.Entity import Entity
import pygame as pg


class IDrawable(Entity):
    def draw(self, surface: pg.Surface):
        pass
