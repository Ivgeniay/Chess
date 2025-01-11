# NOTE: GENERAL
RELEASE = False

# NOTE: screen settings
WIDTH = 800
HEIGHT = 800
APP_TITLE = "Chess"
FPS = 60

# NOTE: board settings
BOARD_WIDTH = 600
BOARD_HEIGHT = 600
SQUARE_SIZE = BOARD_WIDTH // 8
SQUARE_SCALE = 1
BOARD_OFFSET = (100, 150)

BLACK_PAW_LINK = "resources/sprites/black_pawn.png"
BLACK_ROOK_LINK = "resources/sprites/black_rook.png"
BLACK_KNIGHT_LINK = "resources/sprites/black_knight.png"
BLACK_BISHOP_LINK = "resources/sprites/black_bishop.png"
BLACK_QUEEN_LINK = "resources/sprites/black_queen.png"
BLACK_KING_LINK = "resources/sprites/black_king.png"
WHITE_PAW_LINK = "resources/sprites/white_pawn.png"
WHITE_ROOK_LINK = "resources/sprites/white_rook.png"
WHITE_KNIGHT_LINK = "resources/sprites/white_knight.png"
WHITE_BISHOP_LINK = "resources/sprites/white_bishop.png"
WHITE_QUEEN_LINK = "resources/sprites/white_queen.png"
WHITE_KING_LINK = "resources/sprites/white_king.png"

DRAGGABLE_OFFSET = (-SQUARE_SIZE//4, -SQUARE_SIZE//4)
WINDOW_TITLE = "Chess"

# NOTE: ui settings
UPPER_UI_HEIGHT = BOARD_OFFSET[1]
UPPER_UI_WIDTH = WIDTH

BTN_WIDTH = 100
BTN_HEIGHT = 50
BTN_FONT_SIZE = 36
BTN_POSITION = (UPPER_UI_WIDTH/2 - BTN_WIDTH/2,
                UPPER_UI_HEIGHT/2 - BTN_HEIGHT/1)

SCORE_WIDTH = 200
SCORE_HEIGHT = 50

DEFAULT_BTN_PATH = "game/resources/btns/Btn_Rectangle00_n_Gray.png"
DEFAULT_BTN_HOVER_PATH = "game/resources/btns/Btn_Rectangle00_n_Blue.png"


# NOTE: colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLACK_SOFT = (50, 50, 50)
BROWN = (139, 69, 19)
SILVER = (192, 192, 192)
YELLOW = (255, 255, 0)
RED = (180, 0, 0)
GREEN = (0, 180, 0)
