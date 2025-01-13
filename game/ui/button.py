from game.services.resourse_service import ResourcesService
from game.services.service_locator import ServiceLocator
from game.ui.uielement import UiElement
from game.settings import *

from typing import Callable
import pygame as pg


class Button(UiElement):

    def __init__(self, x: int, y: int, width: int, height: int, image_name: str = None, text: str = "", action: Callable[[UiElement], None] = None, hover_image_name: str = None, sound_path: str = None, font: pg.font.Font = None, text_color: tuple[int, int, int] = BLACK, surface: pg.Surface = None):
        super().__init__(x, y, width, height, font, text, surface)
        self.text: str = text
        self.text_color: tuple[int, int, int] = text_color
        self.rect: pg.Rect = pg.Rect(self.x, self.y, self.width, self.height)

        self.resources_service: ResourcesService = ServiceLocator.get(
            ResourcesService)

        if image_name is None:
            image_name = DEFAULT_BTN_NAME
        if hover_image_name is None:
            hover_image_name = DEFAULT_BTN_HOVER_NAME

        self.image = self.resources_service.get_resource(image_name)
        self.image = pg.transform.scale(
            self.image, (self.width, self.height))

        self.hover_image = self.resources_service.get_resource(
            hover_image_name)
        self.hover_image: pg.Surface = pg.transform.scale(
            self.hover_image, (self.width, self.height))

        self.rect: pg.Rect = self.image.get_rect(top=self.y, left=self.x)
        self.sound = None
        if sound_path is not None:
            self.sound = pg.mixer.Sound(sound_path)

        self.on_btn_click_action: Callable[[UiElement], None] = action
        self.on_btn_hower_action: Callable[[UiElement], None] = None

        self.current_image: pg.Surface = self.image

        self.text_surface = self.font.render(text, True, BLACK)
        self.text_rect = self.text_surface.get_rect(
            center=(self.rect.centerx, self.rect.centery))

    def change_picture(self, pic: pg.Surface) -> None:
        self.image: pg.Surface = pic
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.current_image = self.image

    def change_hover_picture(self, pic: pg.Surface) -> None:
        self.hover_image: pg.Surface = pic
        self.hover_image = pg.transform.scale(
            self.hover_image, (self.width, self.height))

    def draw(self, surface: pg.Surface) -> None:
        super().draw(surface)
        surface.blit(self.current_image, self.rect)
        surface.blit(self.text_surface, self.text_rect)

    def on_hover(self, value: bool) -> None:
        self.current_image = self.hover_image if value else self.image
        if self.on_btn_hower_action is not None:
            self.on_btn_hower_action(self)

    def on_click(self) -> None:
        if self.on_btn_click_action is not None and self.is_hovered:
            self.on_btn_click_action(self)
