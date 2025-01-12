from typing import Any, Dict
import pygame as pg
import os

from game.settings import *


class ResourcesService:
    def __init__(self):
        self.resources = {}
        self.load_resources()
        print(self.resources)

    def load_resources(self) -> None:
        """
        Обходит папку base_path и загружает изображения и звуки в словарь self.resources.
        """
        for root, _, files in os.walk(RESOURCES_PATH):
            relative_path = os.path.relpath(root, RESOURCES_PATH)
            path_parts = relative_path.split(
                os.sep) if relative_path != '.' else []

            current_dict = self.resources
            for part in path_parts:
                current_dict = current_dict.setdefault(part, {})

            for file in files:
                file_name, file_ext = os.path.splitext(file)
                file_ext = file_ext.lower()

                if file_ext in [".png", ".jpg", ".jpeg"]:
                    file_path = os.path.join(root, file)
                    current_dict[file_name] = pg.image.load(
                        file_path).convert_alpha()

                elif file_ext in [".wav", ".mp3", ".ogg"]:
                    file_path = os.path.join(root, file)
                    current_dict[file_name] = pg.mixer.Sound(file_path)

    def get_resource(self, name: str) -> Any:
        """
        Возвращает первый ресурс с указанным именем, найденный в дереве ресурсов.

        :param name: Имя ресурса.
        :return: Ресурс (например, Surface или Sound), если найден, иначе None.
        """
        resource = self._find_resource(self.resources, name)
        if resource is None:
            raise ValueError(f"Resource {name} not found")
        return resource

    def _find_resource(self, data: Dict[str, Any], name: str) -> Any:
        """
        Рекурсивно ищет ресурс по имени в дереве.

        :param data: Текущий узел дерева ресурсов.
        :param name: Имя ресурса для поиска.
        :return: Найденный ресурс или None.
        """
        for key, value in data.items():
            if key == name:  # Если имя совпадает, возвращаем ресурс
                return value
            if isinstance(value, dict):  # Если вложенный словарь, продолжаем поиск
                result = self._find_resource(value, name)
                if result is not None:
                    return result
        return None  # Если ресурс не найден
