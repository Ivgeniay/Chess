from lib.figure_type import Figure_type
from lib.move import Move
from lib.side import Side


class MoveModel:

    def __init__(self, figure_type: Figure_type, move_from: Move, move_to: Move, side: Side) -> None:
        self.figure_type: Figure_type = figure_type
        self.move_from: Move | None = move_from
        self.move_to: Move = move_to
        self.side: Side = side
