from typing import Callable

from lib.figure_fabric import FigureFabric
from lib.castlingType import CastlingType
from lib.figure_type import Figure_type
from lib.castling import Castling
from lib.figure import Figure
from lib.bishop import Bishop
from lib.knight import Knight
from lib.queen import Queen
from lib.move import Move
from lib.side import Side
from lib.pawn import Pawn
from lib.king import King
from lib.rook import Rook


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

# TODO: Добавить взятие на проходе
# TODO: Добавить превращение пешки
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

        self.controll_side: Side = Side.NONE
        self.controll_castling: Castling = Castling.Both
        self.controll_enpassant = "-"

        # NOTE: white side move
        self.move_number = 0
        # NOTE: black side move
        self.half_move_number = 0
        self.calculate_attack_positions()

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

    def from_fen(self, fen: str) -> None:
        """
        Парсит FEN-строку и обновляет состояние доски.
        """

        parts = fen.split()
        if len(parts) != 6:
            raise ValueError("Неверный формат FEN-строки")

        board_fen, side_fen, castling_fen, enpassant_fen, halfmove_fen, move_fen = parts

        self.destroy_all_figures()

        # 1. Расстановка фигур на доске
        self.board = [[None for _ in range(8)] for _ in range(8)]
        rows = board_fen.split("/")
        if len(rows) != 8:
            raise ValueError("Некорректное количество строк в FEN-строке.")

        for row_idx, row in enumerate(reversed(rows)):
            col_idx = 0
            for char in row:
                if char.isdigit():  # Пустые клетки
                    col_idx += int(char)
                else:  # Фигура
                    position = Move(row_idx, col_idx)
                    figure = self.fabric.create_figure(
                        Figure_type(char), position)
                    self.board[row_idx][col_idx] = figure
                    col_idx += 1

        # 2. Очередь хода
        self.controll_side = Side.WHITE if side_fen == "w" else Side.BLACK

        # 3. Права на рокировку
        if castling_fen == "-":
            self.controll_castling = Castling.None_
        else:
            self.controll_castling = Castling.Both
            if "K" not in castling_fen or "Q" not in castling_fen:
                self.controll_castling = Castling.WHITE if "K" in castling_fen or "Q" in castling_fen else Castling.None_
            if "k" not in castling_fen or "q" not in castling_fen:
                if self.controll_castling == Castling.WHITE:
                    self.controll_castling = Castling.None_
                else:
                    self.controll_castling = Castling.BLACK

        # 4. Поле взятия на проходе
        self.controll_enpassant = enpassant_fen

        # 5. Полусчётчик ходов (правило 50 ходов)
        self.half_move_number = int(halfmove_fen)

        # 6. Номер полного хода
        self.move_number = int(move_fen)

        self.is_next_turn_on_start = False

        # Пересчитать атакующие клетки
        self.calculate_attack_positions()

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

    def move_figure(self, figure: Figure, move_to: Move) -> None:
        other = self.board[move_to.value[0]][move_to.value[1]]

        # NOTE: обработка взятия на проходе
        if isinstance(figure, Pawn) and other == None and figure.position.value[1] != move_to.value[1]:
            self.eating_an_passant(figure, move_to)

        # NOTE: обработки ракировки
        elif isinstance(figure, King) and isinstance(other, Rook) and figure.side == other.side:
            delta = abs(move_to.value[1] - figure.position.value[1])
            match figure.side:
                case Side.WHITE:
                    self.castling(CastlingType.W_SHORT) if delta == 3 else self.castling(
                        CastlingType.W_LONG)
                case Side.BLACK:
                    self.castling(CastlingType.B_SHORT) if delta == 3 else self.castling(
                        CastlingType.B_LONG)
        else:
            old_position: Move = figure.position
            if other != None:
                self.eating_figure(
                    figure, other)
            else:
                self.board[move_to.value[0]][move_to.value[1]] = figure
                self.board[old_position.value[0]][old_position.value[1]] = None
                figure.set_new_position(move_to)

        self.nullify_on_passant(figure)
        figure.last_action()
        self.next_turn()

        print(move_to.value)

    def castling(self, castling_type: CastlingType) -> None:
        """
        Метод для рокировки. Перемещает короля и ладью на соответствующие клетки. Метод безопасен только в том случае, если соблюдаются условия рокировки
        """
        match castling_type:
            case CastlingType.W_SHORT:
                rook = self.board[0][7]
                king = self.board[0][4]
                self.board[0][5] = rook
                self.board[0][6] = king
                self.board[0][4] = None
                self.board[0][7] = None
                rook.set_new_position(Move(0, 5))
                king.set_new_position(Move(0, 6))
            case CastlingType.W_LONG:
                rook = self.board[0][0]
                king = self.board[0][4]
                self.board[0][0] = None
                self.board[0][4] = None
                self.board[0][3] = rook
                self.board[0][2] = king
                rook.set_new_position(Move(0, 3))
                king.set_new_position(Move(0, 2))
            case CastlingType.B_SHORT:
                rook = self.board[7][7]
                king = self.board[7][4]
                self.board[7][7] = None
                self.board[7][4] = None
                self.board[7][5] = rook
                self.board[7][6] = king
                rook.set_new_position(Move(7, 5))
                king.set_new_position(Move(7, 6))
            case CastlingType.B_LONG:
                rook = self.board[7][0]
                king = self.board[7][4]
                self.board[7][0] = None
                self.board[7][4] = None
                self.board[7][3] = rook
                self.board[7][2] = king
                rook.set_new_position(Move(7, 3))
                king.set_new_position(Move(7, 2))

    def eating_figure(self, eating_figures: Figure, eaten_figure: Figure) -> None:
        """
        Метод для съедания фигуры. Перемещает фигуру на указанную клетку и уничтожает фигуру, которая находилась на этой клетке.
        """
        self.board[eating_figures.position.value[0]
                   ][eating_figures.position.value[1]] = None
        self.board[eaten_figure.position.value[0]
                   ][eaten_figure.position.value[1]] = eating_figures
        eating_figures.set_new_position(eaten_figure.position)
        eaten_figure.destroy()

    def eating_an_passant(self, figure: Figure, move_to: Move) -> None:
        """
        Вспомогательный метод вызываем при обработке перемещения пешки. Не рекомендуется вызывать
        """

        other_figure: Figure = None
        other_position: Move = None
        self_old_position = figure.position
        if figure.side == Side.WHITE:
            other_position = Move(move_to.value[0] - 1, move_to.value[1])
            # other_figure = self.board[move_to.value[0] - 1][move_to.value[1]]
        if figure.side == Side.BLACK:
            other_position = Move(move_to.value[0] + 1, move_to.value[1])
            # other_figure = self.board[move_to.value[0] + 1][move_to.value[1]]

        other_figure = self.board[other_position.value[0]
                                  ][other_position.value[1]]
        self.board[other_position.value[0]][other_position.value[1]] = None
        other_figure.destroy()

        self.board[move_to.value[0]][move_to.value[1]] = figure
        self.board[self_old_position.value[0]
                   ][self_old_position.value[1]] = None
        figure.set_new_position(move_to)

    def switch_pawn(self, figure: Pawn, figure_type: Figure_type) -> None:
        """
        Метод для превращения пешки в другую фигуру.
        """
        new_figure = self.fabric.create_figure(
            figure_type, figure.position)
        figure.destroy()
        self.board[figure.position.value[0]
                   ][figure.position.value[1]] = new_figure

    def nullify_on_passant(self, sender) -> None:
        """
        Отмена возможности взятия на проходе у всех пешек, кроме отправителя. Поскольку пешка, которая сделала ход на 2 клетки, может быть взята на проходе на следующем ходу.
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
        self.inscrease_score_and_get_next_turn()
        self.call_next_turn_event()

        print(self.get_fen())

    def call_next_turn_event(self):
        """
        Метод вызова события "следующий ход" для подписчиков события.
        """
        for handler in self.next_turn_handlers:
            handler(self)

    def inscrease_score_and_get_next_turn(self):
        """
        Передача хода другой стороне и увеличение счётчиков ходов.
        """
        if self.controll_side == Side.WHITE:
            self.controll_side = Side.BLACK
            self.move_number += 1
        elif self.controll_side == Side.BLACK:
            self.controll_side = Side.WHITE
            self.half_move_number += 1
        else:
            self.controll_side = Side.WHITE

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

    def is_cell_under_attack(self, move: Move, side: Side) -> bool:
        """
        Проверка находится ли клетка под атакой.
        """
        if side == Side.WHITE:
            return move in self.black_attack_cells
        else:
            return move in self.white_attack_cells

    def destroy_all_figures(self) -> None:
        """
        Уничтожение всех фигур на доске.
        """
        for row in self.board:
            for figure in row:
                if figure is not None:
                    figure.destroy()

    def restart(self) -> None:
        """
        Метод перезапуска шахматной партии. Уничтожение всех фигур на доске и инициализация новой доски.
        """

        self.destroy_all_figures()
        self.initialize_bord()
        self.next_turn()
        pass

    def start(self, is_call_next_turn=True) -> None:
        """
        Начало игры. Первый ход белых.

        :param is_call_next_turn: Вызвать ли событие "следующий ход" (по умолчанию True). В случае, если False, событие не будет вызвано, но подпичсики события будут всеравно уведомлены.
        """
        if is_call_next_turn:
            self.next_turn()
        else:
            self.call_next_turn_event()

    def get_figure_possible_moves(self, figure: Figure, is_under_protection_figure: bool = False) -> list[Move]:
        match figure:
            case King():
                return self.get_king_possible_moves(figure, is_under_protection_figure)
            case Queen():
                return self.get_queen_possible_moves(figure, is_under_protection_figure)
            case Rook():
                return self.get_rook_possible_moves(figure, is_under_protection_figure)
            case Bishop():
                return self.get_bishop_possible_moves(figure, is_under_protection_figure)
            case Knight():
                return self.get_knight_possible_moves(figure, is_under_protection_figure)
            case Pawn():
                return self.get_pawn_possible_moves(figure, is_under_protection_figure)

    def get_king_possible_moves(self, figure: Figure, is_under_protection_figure: bool = False) -> list[Move]:
        possible_moves = []
        row, col = figure.position.value
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                other_figure = self.board[r][c]
                move_key = Move((r, c))

                # NOTE: Клетка свободна или занята фигурой противника
                if other_figure is None or other_figure.side != figure.side:
                    possible_moves.append(move_key)

        # Добавление проверки на рокировку
        if is_under_protection_figure == False and figure.side == Side.WHITE and self.controll_castling in (Castling.WHITE, Castling.Both):
            # Короткая рокировка белых
            if len(figure.positions) == 1 and self.board[0][7] and isinstance(self.board[0][7], Rook):
                rook = self.board[0][7]
                if len(rook.positions) == 1 and all(self.board[0][c] is None for c in (5, 6)):
                    # Проверяем, что клетки e1, f1, g1 не под атакой
                    if not any(cell in self.black_attack_cells for cell in (Move((0, 4)), Move((0, 5)), Move((0, 6)))):
                        # possible_moves.append(Move((7, 6)))
                        possible_moves.append(Move((0, 7)))

            # Длинная рокировка белых
            if len(figure.positions) == 1 and self.board[0][0] and isinstance(self.board[0][0], Rook):
                rook = self.board[0][0]
                if len(rook.positions) == 1 and all(self.board[0][c] is None for c in (1, 2, 3)):
                    # Проверяем, что клетки e1, d1, c1 не под атакой
                    if not any(cell in self.black_attack_cells for cell in (Move((0, 4)), Move((0, 3)), Move((0, 2)))):
                        # possible_moves.append(Move((7, 2)))
                        possible_moves.append(Move((0, 0)))

        if not is_under_protection_figure and figure.side == Side.BLACK and self.controll_castling in (Castling.BLACK, Castling.Both):
            # Короткая рокировка черных
            if len(figure.positions) == 1 and self.board[7][7] and isinstance(self.board[7][7], Rook):
                rook = self.board[7][7]
                if len(rook.positions) == 1 and all(self.board[7][c] is None for c in (5, 6)):
                    # Проверяем, что клетки e8, f8, g8 не под атакой
                    if not any(cell in self.white_attack_cells for cell in (Move((7, 4)), Move((7, 5)), Move((7, 6)))):
                        # possible_moves.append(Move((0, 6)))
                        possible_moves.append(Move((7, 7)))

            # Длинная рокировка черных
            if len(figure.positions) == 1 and self.board[7][0] and isinstance(self.board[7][0], Rook):
                rook = self.board[7][0]
                if len(rook.positions) == 1 and all(self.board[7][c] is None for c in (1, 2, 3)):
                    # Проверяем, что клетки e8, d8, c8 не под атакой
                    if not any(cell in self.white_attack_cells for cell in (Move((7, 4)), Move((7, 3)), Move((7, 2)))):
                        # possible_moves.append(Move((0, 2)))
                        possible_moves.append(Move((7, 0)))

        return possible_moves

    def get_queen_possible_moves(self, figure: Figure, is_under_protection_figure: bool = False) -> list[Move]:
        possible_moves = []
        row, col = figure.position.value
        self.traverse_direction(figure,
                                1, 0, row, col, possible_moves, is_under_protection_figure)
        self.traverse_direction(figure, -1, 0, row, col,
                                possible_moves, is_under_protection_figure)
        self.traverse_direction(figure,
                                0, 1, row, col, possible_moves, is_under_protection_figure)
        self.traverse_direction(figure,
                                0, -1, row, col, possible_moves, is_under_protection_figure)
        self.traverse_direction(figure,
                                1, 1, row, col, possible_moves, is_under_protection_figure)
        self.traverse_direction(figure,
                                1, -1, row, col, possible_moves, is_under_protection_figure)
        self.traverse_direction(figure, -1, 1, row, col,
                                possible_moves, is_under_protection_figure)
        self.traverse_direction(figure, -1, -1, row, col,
                                possible_moves, is_under_protection_figure)

        return possible_moves

    def get_rook_possible_moves(self, figure: Figure, is_under_protection_figure: bool = False) -> list[Move]:
        possible_moves = []
        row, col = figure.position.value
        # NOTE: Обход вертикали и горизонтали
        self.traverse_direction(figure,
                                1, 0, row, col, possible_moves, is_under_protection_figure)
        self.traverse_direction(figure, -1, 0, row, col,
                                possible_moves, is_under_protection_figure)
        self.traverse_direction(figure,
                                0, 1, row, col, possible_moves, is_under_protection_figure)
        self.traverse_direction(figure,
                                0, -1, row, col, possible_moves, is_under_protection_figure)

        return possible_moves

    def get_bishop_possible_moves(self, figure: Figure, is_under_protection_figure: bool = False) -> list[Move]:
        possible_moves = []
        row, col = figure.position.value

        # ТNOTE: Обход диагоналей
        self.traverse_direction(figure,
                                1, 1, row, col, possible_moves, is_under_protection_figure)
        self.traverse_direction(figure,
                                1, -1, row, col, possible_moves, is_under_protection_figure)
        self.traverse_direction(figure, -1, 1, row, col,
                                possible_moves, is_under_protection_figure)
        self.traverse_direction(figure, -1, -1, row, col,
                                possible_moves, is_under_protection_figure)

        return possible_moves

    def traverse_direction(self, figure: Figure, dr: int, dc: int, row: int, col: int, possible_moves: list, is_under_protection_figure: bool = False) -> None:
        """
        Вспомогательный метод для обхода клеток в указанном направлении.

        :param dr: Смещение по вертикали.
        :param dc: Смещение по горизонтали.
        :param row: Начальная строка.
        :param col: Начальный столбец.
        :param possible_moves: Список возможных ходов.
        :param with_guard_figure: Флаг, указывающий на необходимость добавления клеток с фигурами того же цвета для включения в список, как 'под защитой фигуры'.
        """
        from lib.king import King
        r, c = row + dr, col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            other_figure = self.board[r][c]
            move_key = Move((r, c))

            # NOTE: Клетка пустая
            if other_figure is None:
                possible_moves.append(move_key)
            elif isinstance(other_figure, King) and other_figure.side != figure.side:
                # NOTE: Если фигура противника - король, добавляем клетку и продолжаем обход
                possible_moves.append(move_key)
            else:
                # NOTE: Если фигура того же цвета
                if other_figure.side == figure.side:
                    # NOTE: Если фигура находится под защитой, добавляем клетку и прерываем обход
                    if is_under_protection_figure:
                        possible_moves.append(move_key)
                    break
                # NOTE: Если фигура противника, добавляем клетку и прерываем обход
                possible_moves.append(move_key)
                break

            r += dr
            c += dc

    def get_knight_possible_moves(self, figure: Figure, is_under_protection_figure: bool = False) -> list[Move]:
        possible_moves = []
        row, col = figure.position.value

        # Все возможные смещения для хода коня
        knight_moves = [
            (-2, -1), (-2, 1),  # Верхние ходы
            (-1, -2), (-1, 2),  # Ходы слева и справа
            (1, -2), (1, 2),    # Ходы снизу слева и справа
            (2, -1), (2, 1)     # Нижние ходы
        ]

        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc

            # Проверяем, что клетка находится в пределах доски
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                move = Move((new_row, new_col))
                cell = self.board[new_row][new_col]

                # Если клетка пуста или занята фигурой противника, добавляем ход
                if cell is None or cell.side != figure.side:
                    possible_moves.append(move)
                elif is_under_protection_figure:
                    possible_moves.append(move)

        return possible_moves

    def get_pawn_possible_moves(self, figure: Figure, is_under_protection_figure: bool = False) -> list[Move]:
        possible_moves = []
        row, col = figure.position.value
        if isinstance(figure, Pawn):
            figure: Pawn = figure
        else:
            raise ValueError("Figure is not pawn")

        # NOTE: Определяем направление движения в зависимости от стороны
        direction = 1 if figure.side == Side.WHITE else -1

        # NOTE: Ход на одну клетку вперёд
        new_row = row + direction
        # NOTE:Клетка должна быть пустой
        if 0 <= new_row < 8 and self.board[new_row][col] is None:
            possible_moves.append(Move((new_row, col)))

            # NOTE: Ход на две клетки вперёд со стартовой позиции
            if figure.can_enpassant and ((figure.side == Side.WHITE and row == 1) or (figure.side == Side.BLACK and row == 6)):
                two_step_row = row + 2 * direction
                # Проверяем, что обе клетки свободны
                if self.board[two_step_row][col] is None:
                    possible_moves.append(Move((two_step_row, col)))

        # NOTE: Диагональные ходы (возможны только при атаке)
        for dc in (-1, 1):  # Влево и вправо по диагонали
            diag_row, diag_col = row + direction, col + dc
            if 0 <= diag_row < 8 and 0 <= diag_col < 8:
                cell = self.board[diag_row][diag_col]
                # NOTE: Если есть фигура противника
                if cell is not None and cell.side != figure.side:
                    possible_moves.append(Move((diag_row, diag_col)))
                # NOTE: Если есть фигура игрока и нужно вернуть данные о фигурах под защитой
                elif is_under_protection_figure:
                    possible_moves.append(Move((diag_row, diag_col)))

            # NOTE: Взятие на проходе
            enpassant_row = row
            enpassant_col = col + dc
            if 0 <= enpassant_col < 8:
                # Находим фигуру, которую можно взять на проходе
                enpassant_figure = self.board[enpassant_row][enpassant_col]
                if (
                    isinstance(enpassant_figure, Pawn)
                    and enpassant_figure.side != figure.side
                    and enpassant_figure.is_enpassant
                    # Клетка позади должна быть свободной
                    and self.board[diag_row][diag_col] is None
                ):
                    possible_moves.append(Move((diag_row, diag_col)))

        return possible_moves
