from re import S
from typing import Literal
from game.services.service_locator import ServiceLocator
from game.ui.surface.surface_manager import SurfaceManager
from game.ui.uielement import UiElement
from game.services.input import Input
from game.settings import *

import pygame as pg


class Layout():

    def __init__(self, x: int, y: int, width: int, height: int, content: list[UiElement] = None, surface: pg.Surface = None, fill_color: tuple[int, int, int] = BLACK) -> None:
        if surface is None:
            self._surface = pg.Surface((width, height))
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.input: Input = ServiceLocator.get(Input)
        self.is_hovered: bool = False
        self.rect: pg.Rect = pg.Rect(self.x, self.y, self.width, self.height)

        self.surface_manager: SurfaceManager = ServiceLocator.get(
            SurfaceManager)

        self.input.mouse_pos_register(self.on_mouse_pos_change)
        self.input.mouse_left_down_register(self, self.on_click)

        # self.content: list[UiElement] = [] if content is None else content
        self.content: set[UiElement] = set(
        ) if content is None else set(content)
        self.is_open = False
        self.fill_color: tuple[int, int, int] = fill_color
        self.is_adjust_content = True

    @property
    def surface(self) -> pg.Surface:
        return self._surface

    def draw(self, surface: pg.Surface) -> None:
        if not self.is_open:
            return
        self._surface.fill(self.fill_color)
        for element in self.content:
            element.draw(self._surface)

        surface.blit(self._surface, (self.x, self.y))

    def add_element(self, element: UiElement) -> None:
        self.content.add(element)
        if self.is_adjust_content:
            self.center_adjust_content()

    def open(self) -> None:
        if not self.is_open:
            self.surface_manager.add_surface(
                self._surface, self.rect, layout=self, is_main=False)
        self.is_open = True

    def close(self) -> None:
        if self.is_open:
            self.surface_manager.remove_surface(self._surface)
        self.is_open = False

    def right_top_adjust_content(self) -> None:
        """
        Подстраивает размеры и позиции всех элементов в content так,
        чтобы они помещались в границы Layout.
        """
        if not self.content:
            return

        total_width = sum(element.width for element in self.content)
        total_height = sum(element.height for element in self.content)

        width_scale = min(
            1, self.width / total_width) if total_width > 0 else 1
        height_scale = min(
            1, self.height / total_height) if total_height > 0 else 1

        current_x = 0
        current_y = 0

        for element in self.content:
            element.width = int(element.width * width_scale)
            element.height = int(element.height * height_scale)

            element.rect.width = element.width
            element.rect.height = element.height
            element.rect.x = current_x
            element.rect.y = current_y

            current_x += element.width

            if current_x > self.width:
                current_x = 0
                current_y += element.height

            if current_y + element.height > self.height:
                break

    def center_adjust_content(self) -> None:
        """
        Центрирует все элементы внутри Layout.
        Все элементы будут размещены в центре Layout.
        """
        if not self.content:
            return

        # Суммарная ширина и высота всех элементов
        total_width = sum(element.width for element in self.content)
        total_height = sum(element.height for element in self.content)

        # Коэффициенты масштабирования, если нужно уместить все элементы в пределах Layout
        width_scale: float | Literal[1] = min(
            1, self.width / total_width) if total_width > 0 else 1
        height_scale: float | Literal[1] = min(
            1, self.height / total_height) if total_height > 0 else 1

        # Пропорционально изменяем размеры элементов
        for element in self.content:
            element.width = int(element.width * width_scale)
            element.height = int(element.height * height_scale)

            # Обновляем размеры rect
            element.rect.width = element.width
            element.rect.height = element.height

        # Вычисляем начальную координату для размещения элементов в центре
        current_x: float | int = (self.width - total_width * width_scale) // 2
        current_y: float | int = (
            self.height - total_height * height_scale) // 2

        for element in self.content:
            # Обновляем позицию каждого элемента, чтобы они располагались по центру
            element.rect.x = current_x
            element.rect.y = current_y

            # Обновляем координаты для следующего элемента
            current_x += element.width

            # Если элементы выходят за пределы ширины Layout, переносим на новую строку
            if current_x > self.width:
                current_x = (self.width - total_width * width_scale) // 2
                current_y += element.height

    def on_hover(self, is_hovered: bool) -> None:
        pass

    def on_click(self) -> None:
        pass

    def on_mouse_pos_change(self, global_mouse_pos: tuple[int, int]) -> None:
        top_surface: pg.Surface | None = self.surface_manager.get_top_surface_at(
            *global_mouse_pos)
        if top_surface:
            local_mouse_pos: tuple[int, int] | None = self.surface_manager.get_relative_mouse_pos(
                top_surface["surface"], global_mouse_pos)
            # print(local_mouse_pos)
            if local_mouse_pos:
                rect: pg.Rect = top_surface["rect"]
                is_collided: bool = self.rect.collidepoint(local_mouse_pos)
                if is_collided != self.is_hovered:
                    self.is_hovered = is_collided
                    self.on_hover(self.is_hovered)
