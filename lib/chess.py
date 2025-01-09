from typing import Callable

from lib.castling import Castling
from lib.figure_type import Figure_type
from lib.move import Move
from lib.side import Side
from lib.figure import Figure
from lib.figure_fabric import FigureFabric
from lib.pawn import Pawn


start_position: list[list[Figure_type]] = [
    [Figure_type.w_rook, Figure_type.w_knight, Figure_type.w_bishop, Figure_type.w_queen,
     Figure_type.w_king, Figure_type.w_bishop, Figure_type.w_knight, Figure_type.w_rook],
    [Figure_type.w_pawn, Figure_type.w_pawn, Figure_type.w_pawn, Figure_type.w_pawn,
     Figure_type.w_pawn, Figure_type.w_pawn, Figure_type.w_pawn, Figure_type.w_pawn],

    [Figure_type.empty, Figure_type.empty, Figure_type.empty, Figure_type.empty,
     Figure_type.empty, Figure_type.empty, Figure_type.empty, Figure_type.empty],
    [Figure_type.empty, Figure_type.empty, Figure_type.empty, Figure_type.empty,
     Figure_type.empty, Figure_type.empty, Figure_type.empty, Figure_type.empty],
    [Figure_type.empty, Figure_type.empty, Figure_type.empty, Figure_type.empty,
     Figure_type.empty, Figure_type.empty, Figure_type.empty, Figure_type.empty],
    [Figure_type.empty, Figure_type.empty, Figure_type.empty, Figure_type.empty,
     Figure_type.empty, Figure_type.empty, Figure_type.empty, Figure_type.empty],

    [Figure_type.b_pawn, Figure_type.b_pawn, Figure_type.b_pawn, Figure_type.b_pawn,
     Figure_type.b_pawn, Figure_type.b_pawn, Figure_type.b_pawn, Figure_type.b_pawn],
    [Figure_type.b_rook, Figure_type.b_knight, Figure_type.b_bishop, Figure_type.b_queen,
     Figure_type.b_king, Figure_type.b_bishop, Figure_type.b_knight, Figure_type.b_rook],
]

# TODO: Добавить проверку на рокировку
# TODO: Добавить шах
# TODO: Добавить шах и мат


class Chess:
    def __init__(self) -> None:
        self.fabric = FigureFabric(self)
        self.next_turn_handlers: list[Callable[[Chess], None]] = []
        self.initialize_bord()

    def initialize_bord(self) -> None:
        """
        Метод инициализации доски. Создаётся двумерный массив, содержащий фигуры в начальном положении. 
        Не должен вызываться напрямую
        """
        self.white_attack_cells: set[Move] = set()
        self.black_attack_cells: set[Move] = set()

        self.board: list[list[Figure]] = [[None for _ in range(
            len(start_position[0]))] for _ in range(len(start_position))]

        for i in range(len(start_position)):
            for j in range(len(start_position[i])):
                self.board[i][j] = self.fabric.create_figure(
                    start_position[i][j], Move(i, j))

        self.controll_side = Side.NONE
        self.controll_castling = Castling.Both
        self.controll_enpassant = "-"

        # NOTE: white side move
        self.move_number = 0
        # NOTE: black side move
        self.half_move_number = 0

    def register_next_turn_handler(self, handler: Callable[["Chess"], None]) -> None:
        """
        Регистрация обработчика события "следующий ход".
        """
        self.next_turn_handlers.append(handler)

    def get_figure_list(self):
        """
        Получение списка всех фигур на доске.
        """
        return [figure for row in self.board for figure in row if figure != None]

    def position_to_fen(self) -> str:
        """
        Вспомогательный метод для генерации FEN-строки. Преобразует текущую позицию на доске в строку, содержащую расположение фигур.
        """
        result = []
        for row in self.board:
            empty_count = 0
            row_fen = ""
            for cell in row:
                if cell == None:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        row_fen += str(empty_count)
                        empty_count = 0
                    row_fen += cell.figure_type.value
            if empty_count > 0:
                row_fen += str(empty_count)
            result.append(row_fen)

        result.reverse()
        result = "/".join(result)
        return result

    def get_fen(self) -> str:
        """
        Генерация FEN-строки для текущей позиции на доске.
        """
        # NOTE: Генерация первой части: расположение фигур
        board_fen = self.position_to_fen()

        # NOTE: Очередь хода
        side_fen = "w" if self.controll_side == Side.WHITE else "b"

        # NOTE: Права на рокировку
        castling_fen = ""
        if self.controll_castling == Castling.Both:
            castling_fen = "KQkq"
        elif self.controll_castling == Castling.WHITE:
            castling_fen = "KQ"
        elif self.controll_castling == Castling.BLACK:
            castling_fen = "kq"
        else:
            castling_fen = "-"

        # NOTE: Поле для взятия на проходе
        enpassant_fen = self.controll_enpassant

        # NOTE: Полусчётчик ходов (правило 50 ходов)
        halfmove_fen = str(self.half_move_number)

        # NOTE: Номер полного хода
        move_fen = str(self.move_number)

        # NOTE: Объединение всех частей
        return f"{board_fen} {side_fen} {castling_fen} {enpassant_fen} {halfmove_fen} {move_fen}"

    def move(self, moveFrom: Move, moveTo: Move) -> None:
        figureFrom = self.board[moveFrom.value[0]][moveFrom.value[1]]

        if figureFrom != None:
            figureFrom.move(moveTo)

    def nullify_on_passat(self, sender) -> None:
        """
        Отмена возможности взятия на проходе у всех пешек, кроме отправителя. Поскольку пешка, которая сделала ход на 2 клетки, 
        может быть взята на проходе только на следующем ходу.
        """
        for row in self.board:
            for figure in row:
                if figure != None and isinstance(figure, Pawn) and figure != sender:
                    figure.is_enpassant = False

    def next_turn(self) -> None:
        """
        Передача хода другой стороне и увеличение счётч. Пересчет возможных ходов для каждой стороны для выявления запрещенных зон для короля.
        """
        self.calculate_attack_positions()
        if self.controll_side == Side.WHITE:
            self.controll_side = Side.BLACK
            self.move_number += 1
        elif self.controll_side == Side.BLACK:
            self.controll_side = Side.WHITE
            self.half_move_number += 1
        else:
            self.controll_side = Side.WHITE

        for handler in self.next_turn_handlers:
            handler(self)

    def calculate_attack_positions(self) -> None:
        self.white_attack_cells.clear()
        self.black_attack_cells.clear()

        for row in self.board:
            for figure in row:
                if figure is not None:
                    if isinstance(figure, Pawn):
                        pawn_attack_cells = figure.pawn_attacks(figure)
                        if figure.side == Side.WHITE:
                            self.white_attack_cells.update(pawn_attack_cells)
                        else:
                            self.black_attack_cells.update(pawn_attack_cells)
                    else:
                        possible_moves = figure.get_possible_moves(
                            is_under_protection_figure=True)
                        if figure.side == Side.WHITE:
                            self.white_attack_cells.update(possible_moves)
                        else:
                            self.black_attack_cells.update(possible_moves)

    def get_horizontal_cells(self, move: Move) -> tuple[list[tuple[Move, "Figure"]], list[tuple[Move, "Figure"]]]:
        """
        Возвращает все клетки и их содержимое по горизонтали (влево и вправо) относительно указанного Move.

        :param move: Положение на доске (Move).
        :return: Кортеж из двух списков. Первый список - клетки слева, второй - клетки справа.
        """
        row, col = move.value
        left_cells = []
        right_cells = []

        # Проходим влево от текущей клетки
        for c in range(col - 1, -1, -1):
            move_key = Move((row, c))
            left_cells.append((move_key, self.board[row][c]))

        # Проходим вправо от текущей клетки
        for c in range(col + 1, 8):
            move_key = Move((row, c))
            right_cells.append((move_key, self.board[row][c]))

        return left_cells, right_cells

    def get_vertical_cells(self, move: Move) -> tuple[list[tuple[Move, "Figure"]], list[tuple[Move, "Figure"]]]:
        """
        Возвращает все клетки и их содержимое по вертикали (вверх и вниз) относительно указанного Move.

        :param move: Положение на доске (Move).
        :return: Кортеж из двух списков. Первый список - клетки ниже, второй - клетки выше.
        """
        row, col = move.value
        below_cells = []
        above_cells = []

        # Проходим вниз от текущей клетки
        for r in range(row - 1, -1, -1):
            move_key = Move((r, col))
            below_cells.append((move_key, self.board[r][col]))

        # Проходим вверх от текущей клетки
        for r in range(row + 1, 8):
            move_key = Move((r, col))
            above_cells.append((move_key, self.board[r][col]))

        return below_cells, above_cells

    def get_diagonal_cells(self, move: Move) -> tuple[list[tuple[Move, "Figure"]], list[tuple[Move, "Figure"]],
                                                      list[tuple[Move, "Figure"]], list[tuple[Move, "Figure"]]]:
        """
        Возвращает диагональные клетки относительно указанного положения.

        :param move: Положение на доске (Move).
        :return: Кортеж из четырёх списков: вверх-вправо, вверх-влево, вниз-вправо, вниз-влево.
        """
        row, col = move.value
        up_right = []
        up_left = []
        down_right = []
        down_left = []

        # NOTE: Диагональ вверх-вправо
        r, c = row + 1, col + 1
        while r < 8 and c < 8:
            move_key = Move((r, c))
            up_right.append((move_key, self.board[r][c]))
            r += 1
            c += 1

        # NOTE: Диагональ вверх-влево
        r, c = row + 1, col - 1
        while r < 8 and c >= 0:
            move_key = Move((r, c))
            up_left.append((move_key, self.board[r][c]))
            r += 1
            c -= 1

        # NOTE: Диагональ вниз-вправо
        r, c = row - 1, col + 1
        while r >= 0 and c < 8:
            move_key = Move((r, c))
            down_right.append((move_key, self.board[r][c]))
            r -= 1
            c += 1

        # NOTE: Диагональ вниз-влево
        r, c = row - 1, col - 1
        while r >= 0 and c >= 0:
            move_key = Move((r, c))
            down_left.append((move_key, self.board[r][c]))
            r -= 1
            c -= 1

        return up_right, up_left, down_right, down_left

    def get_knight_moves(self, move: Move) -> list[tuple[Move, "Figure"]]:
        """
        Возвращает возможные клетки для хода коня.

        :param move: Положение на доске (Move).
        :return: Список возможных клеток, куда может пойти конь.
        """
        row, col = move.value
        possible_moves = [
            (row - 2, col - 1), (row - 2, col + 1),
            (row - 1, col - 2), (row - 1, col + 2),
            (row + 1, col - 2), (row + 1, col + 2),
            (row + 2, col - 1), (row + 2, col + 1)
        ]

        valid_moves = []
        for r, c in possible_moves:
            if 0 <= r < 8 and 0 <= c < 8:  # Проверка на границы доски
                move_key = Move((r, c))
                valid_moves.append((move_key, self.board[r][c]))

        return valid_moves

    def is_cell_under_attack(self, move: Move, side: Side) -> bool:
        """
        Проверка находится ли клетка под атакой.
        """
        if side == Side.WHITE:
            return move in self.black_attack_cells
        else:
            return move in self.white_attack_cells

    def restart(self) -> None:
        """
        Метод перезапуска шахматной партии. Уничтожение всех фигур на доске и инициализация новой доски.
        """

        for figure_row in self.board:
            for figure in figure_row:
                if figure is not None:
                    figure.destroy()

        self.initialize_bord()
        self.next_turn()
        pass
