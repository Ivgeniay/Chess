import pygame as pg


class SurfaceManager:

    def __init__(self) -> None:
        self.surfaces = []  # Список поверхностей с их z-индексами
        self.main_surface = None

    def add_surface(self, surface: pg.Surface, rect: pg.Rect, z_index: int = None, layout=None, is_main: bool = False) -> None:
        """
        Добавление поверхности с z-индексом
        """
        if is_main:
            self.main_surface: pg.Surface = surface

        if z_index is None:
            z_index = max((s["z_index"]
                          for s in self.surfaces), default=-1) + 1
        self.surfaces.append(
            {"surface": surface, "rect": rect, "z_index": z_index, "layout": layout, "is_main": is_main})

        if is_main:
            self.set_surface_z_index(surface, 0)

        self.normalize_z_indexes()
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

    def set_surface_z_index(self, surface: pg.Surface, z_index: int) -> None:
        """
        Устанавливает z-индекс для поверхности.
        """
        for s in self.surfaces:
            if s["surface"] == surface:
                s["z_index"] = z_index
                self.normalize_z_indexes()
                self._sort_surfaces()

                for d in self.surfaces:
                    if d["z_index"] >= z_index and d != s:
                        d["z_index"] += 1
                return

        raise ValueError("Surface not found")

    def get_relative_mouse_pos(self, surface: pg.Surface, global_mouse_pos: tuple[int, int]) -> tuple[int, int] | None:
        """
        Возвращает координаты мыши относительно поверхности, если мышь над ней.
        """
        for s in self.surfaces:
            if s["surface"] == surface:
                rect = s["rect"]
                if rect.collidepoint(global_mouse_pos):
                    local_x = global_mouse_pos[0] - rect.x
                    local_y = global_mouse_pos[1] - rect.y
                    return local_x, local_y
        return None

    def draw_surfaces(self) -> None:
        """
        Отрисовывает все поверхности на экране в порядке их z-index.
        """
        for s in sorted(self.surfaces, key=lambda s: s["z_index"], reverse=False):
            layout = s["layout"]
            if layout != None:
                layout.draw(self.main_surface)
                continue

    def raise_surface_on_click(self, x: int, y: int) -> None:
        """
        Поднимает поверхность, на которую было кликнуто, выше всех остальных,
        изменяя z_index так, чтобы кликнутый был самым высоким,
        а остальные поверхности сдвигались вниз, сохраняя порядок.
        """
        clicked_surface = self.get_top_surface_at(x, y)
        if clicked_surface["is_main"]:
            return
        if clicked_surface:
            # Получаем текущий z_index кликнутой поверхности
            clicked_z_index = clicked_surface["z_index"]

            # Сдвигаем z_index всех поверхностей ниже кликнутой
            for s in self.surfaces:
                if s["z_index"] > clicked_z_index:
                    s["z_index"] -= 1

            # Устанавливаем самый высокий z_index для кликнутой поверхности
            clicked_surface["z_index"] = max(
                s["z_index"] for s in self.surfaces) + 1

            # Пересортировка поверхностей по z_index
            self._sort_surfaces()

    def normalize_z_indexes(self) -> None:
        """
        Нормализует z-индексы: начинает с 0 и идет по возрастанию до len(surfaces) - 1.
        """
        self.surfaces.sort(key=lambda s: s["z_index"])  # Сортируем по z_index
        for i, s in enumerate(self.surfaces):
            s["z_index"] = i  # Переназначаем индексы по порядку

    def _sort_surfaces(self) -> None:
        """Сортирует поверхности по z-индексу (от большего к меньшему)."""
        self.surfaces.sort(key=lambda s: s["z_index"], reverse=True)
