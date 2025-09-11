"""ゲームの定数定義"""

# バージョン情報
VERSION = "1.01"

# 画面設定
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
TILE_SIZE = 40
FPS = 120  # フレームレートを上げる

# マップサイズ（画面固定なので画面サイズと同じ）
MAP_WIDTH = SCREEN_WIDTH   # マップの幅
MAP_HEIGHT = SCREEN_HEIGHT  # マップの高さ

# キャラクターサイズ
PLAYER_SIZE = 32
NPC_SIZE = 24  # 少し小さく
ENEMY_SIZE = 40

# ゲームプレイ設定
PLAYER_SPEED_VILLAGE = 4.5  # 村での速度（速い）- 120FPS用に調整
PLAYER_SPEED_FIELD = 2.25   # フィールドでの速度（遅い）- 120FPS用に調整
PLAYER_SPEED_BOSS = 3.0    # ボスエリアでの速度 - 120FPS用に調整
INTERACTION_DISTANCE = 50

# 色定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
LIGHT_GREEN = (144, 238, 144)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
DARK_RED = (139, 0, 0)
BROWN = (139, 69, 19)
LIGHT_BLUE = (173, 216, 230)
GRAY = (128, 128, 128)
DARK_GREEN = (0, 100, 0)
CYAN = (0, 255, 255)

# フォントパス
FONT_PATH = "C:/Windows/Fonts/meiryo.ttc"
FONT_SIZE = 20