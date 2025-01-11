import pygame as pg


class SurfaceManager:
    def __init__(self):
        self.surfaces = []  # Список поверхностей с их z-индексами

    def add_surface(self, surface: pg.Surface, rect: pg.Rect, z_index: int = None) -> None:
        """
        Добавление поверхности с z-индексом
        """

        if z_index is None:
            z_index = max((s["z_index"]
                          for s in self.surfaces), default=-1) + 1
        self.surfaces.append(
            {"surface": surface, "rect": rect, "z_index": z_index})

        self._sort_surfaces()

    def remove_surface(self, surface: pg.Surface) -> None:
        """
        Удаление поверхности
        """
        for s in self.surfaces:
            if s["surface"] == surface:
                self.surfaces.remove(s)
                break
        self._sort_surfaces()

    def get_top_surface_at(self, x, y) -> pg.Surface | None:
        """
        Проверка, какая поверхность сверху в точке (x, y)
        """
        for s in self.surfaces:
            if s["rect"].collidepoint(x, y):
                return s
        return None

    def increment_z_index(self, surface: pg.Surface) -> None:
        """Инкрементирует z_index указанной поверхности."""
        for s in self.surfaces:
            if s["surface"] == surface:
                s["z_index"] += 1
                break
        self._sort_surfaces()

    def decrement_z_index(self, surface: pg.Surface) -> None:
        """Декрементирует z_index указанной поверхности."""
        for s in self.surfaces:
            if s["surface"] == surface:
                s["z_index"] -= 1
                break
        self._sort_surfaces()

    def set_z_index(self, surface: pg.Surface, z_index: int) -> None:
        """Устанавливает конкретный z_index для указанной поверхности."""
        for s in self.surfaces:
            if s["surface"] == surface:
                s["z_index"] = z_index
                break
        self._sort_surfaces()

    def _sort_surfaces(self) -> None:
        """Сортирует поверхности по z-индексу (от большего к меньшему)."""
        self.surfaces.sort(key=lambda s: s["z_index"], reverse=True)
