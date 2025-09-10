"""マップシステムの定義"""
import pygame
from constants import *
from npc import NPC
from enemy import Enemy

class Map:
    def __init__(self, map_id):
        self.map_id = map_id
        self.tiles = []
        self.obstacles = []
        self.npcs = []
        self.enemies = []
        self.create_map()
    
    def create_map(self):
        if self.map_id == 0:  # 村のマップ
            # 地形タイルの作成
            self.tiles = [
                # 道
                {'x': 400, 'y': 0, 'w': 400, 'h': SCREEN_HEIGHT, 'color': BROWN, 'type': 'road'},
                # 草地
                {'x': 0, 'y': 0, 'w': 400, 'h': SCREEN_HEIGHT, 'color': LIGHT_GREEN, 'type': 'grass'},
                {'x': 800, 'y': 0, 'w': 400, 'h': SCREEN_HEIGHT, 'color': LIGHT_GREEN, 'type': 'grass'},
                # 広場
                {'x': 500, 'y': 300, 'w': 200, 'h': 200, 'color': GRAY, 'type': 'plaza'},
            ]
            
            # 障害物（家、木など）
            self.obstacles = [
                pygame.Rect(100, 100, 120, 120),  # 家1
                pygame.Rect(900, 150, 120, 120),  # 家2
                pygame.Rect(150, 400, 120, 120),  # 家3
                pygame.Rect(50, 600, 40, 60),     # 木1
                pygame.Rect(200, 650, 40, 60),    # 木2
                pygame.Rect(950, 500, 40, 60),    # 木3
                pygame.Rect(1050, 600, 40, 60),   # 木4
            ]
            
            # NPCs
            self.npcs = [
                NPC(600, 350, "村長", "ようこそ、我が村へ！北へ行くと森があるぞ。"),
                NPC(300, 200, "商人", "いい品物がありますよ〜", 
                    "assets/sprites/portraits/woman_npc.png"),
                NPC(850, 400, "戦士", "モンスターには気をつけろ！", 
                    None, "assets/sprites/characters/npcs/warrior.png", 
                    is_sprite_sheet=True, frame_width=64, frame_height=64),
                NPC(200, 300, "子供", "お兄ちゃん、どこから来たの？",
                    "assets/sprites/portraits/child.png")
            ]
            
        elif self.map_id == 1:  # 森のマップ
            # 地形タイルの作成
            self.tiles = [
                # 森の背景
                {'x': 0, 'y': 0, 'w': SCREEN_WIDTH, 'h': SCREEN_HEIGHT, 'color': DARK_GREEN, 'type': 'forest'},
                # 小道
                {'x': 500, 'y': 0, 'w': 200, 'h': SCREEN_HEIGHT, 'color': BROWN, 'type': 'path'},
            ]
            
            # 障害物（たくさんの木）
            self.obstacles = []
            # 木をランダムっぽく配置
            tree_positions = [
                (100, 100), (200, 150), (150, 250), (300, 300),
                (50, 400), (250, 450), (100, 550), (350, 600),
                (800, 100), (900, 200), (850, 350), (950, 450),
                (1050, 300), (1100, 500), (1000, 650)
            ]
            for x, y in tree_positions:
                self.obstacles.append(pygame.Rect(x, y, 60, 80))
            
            # NPCs
            self.npcs = [
                NPC(600, 200, "魔法使い", "この森には強いモンスターがいる...",
                    "assets/sprites/portraits/wizard.png"),
                NPC(550, 500, "旅人", "道に迷ってしまった...")
            ]
            
            # 敵
            self.enemies = [
                Enemy(800, 300),
                Enemy(400, 400),
                Enemy(900, 600)
            ]
    
    def draw_tiles(self, screen):
        for tile in self.tiles:
            pygame.draw.rect(screen, tile['color'], 
                           (tile['x'], tile['y'], tile['w'], tile['h']))
    
    def draw_obstacles(self, screen):
        for obstacle in self.obstacles:
            if self.map_id == 0:  # 村
                if obstacle.width > 100:  # 家
                    pygame.draw.rect(screen, BROWN, obstacle)
                    # 屋根
                    pygame.draw.polygon(screen, DARK_RED, [
                        (obstacle.x - 10, obstacle.y),
                        (obstacle.x + obstacle.width // 2, obstacle.y - 30),
                        (obstacle.x + obstacle.width + 10, obstacle.y)
                    ])
                else:  # 木
                    # 幹
                    pygame.draw.rect(screen, BROWN, obstacle)
                    # 葉
                    pygame.draw.circle(screen, GREEN, 
                                     (obstacle.x + obstacle.width // 2, obstacle.y - 10), 30)
            else:  # 森
                # 木の幹
                pygame.draw.rect(screen, BROWN, obstacle)
                # 葉（大きめ）
                pygame.draw.circle(screen, DARK_GREEN, 
                                 (obstacle.x + obstacle.width // 2, obstacle.y), 40)
                pygame.draw.circle(screen, GREEN, 
                                 (obstacle.x + obstacle.width // 2, obstacle.y - 20), 35)