from game.input import Input
from game.ui.uielement import UiElement
from game.settings import *

from typing import Callable
import pygame as pg


class Button(UiElement):

    def __init__(self, x: int, y: int, width: int, height: int, input: Input, image_path: str = None, text: str = "", action: Callable[[UiElement], None] = None, hover_image_path: str = None, sound_path: str = None, font: pg.font.Font = None, text_color: tuple[int, int, int] = BLACK):
        super().__init__(x, y, width, height, input, font, text)
        self.text: str = text
        self.text_color: tuple[int, int, int] = text_color

        self.image = None
        if image_path is None:
            image_path = DEFAULT_BTN_PATH
        if image_path.endswith('.png'):
            self.image = pg.image.load(image_path).convert_alpha()
            self.image = pg.transform.scale(
                self.image, (self.width, self.height))
        else:
            self.image = pg.image.load(image_path)
            self.image = pg.transform.scale(
                self.image, (self.width, self.height))

        self.hover_image = None
        if hover_image_path is None:
            hover_image_path = DEFAULT_BTN_HOVER_PATH
        if hover_image_path is not None and hover_image_path.endswith('.png'):
            self.hover_image = pg.image.load(hover_image_path).convert_alpha()
            self.hover_image = pg.transform.scale(
                self.hover_image, (self.width, self.height))
        elif hover_image_path is not None:
            self.hover_image = pg.image.load(hover_image_path)
            self.hover_image = pg.transform.scale(
                self.hover_image, (self.width, self.height))

        self.rect: pg.Rect = self.image.get_rect(top=self.y, left=self.x)
        self.sound = None
        if sound_path is not None:
            self.sound = pg.mixer.Sound(sound_path)

        self.on_btn_click_action: Callable[[UiElement], None] = action
        self.on_btn_hower_action: Callable[[UiElement], None] = None

        self.current_image = self.image

        self.text_surface = self.font.render(text, True, BLACK)
        self.text_rect = self.text_surface.get_rect(
            center=(self.rect.centerx, self.rect.centery))

    def draw(self, surface):
        surface.blit(self.current_image, self.rect)
        surface.blit(self.text_surface, self.text_rect)

    def on_hover(self, value: bool):
        self.current_image = self.hover_image if value else self.image

    def on_click(self):
        if self.on_btn_click_action is not None and self.is_hovered:
            self.on_btn_click_action(self)
