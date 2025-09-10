"""NPCクラスの定義"""
import pygame
import math
from constants import *
from sprite_utils import load_sprite_sheet, get_animation_frames

class NPC:
    def __init__(self, x, y, name, dialogue, portrait_path=None, sprite_path=None, 
                 is_sprite_sheet=False, frame_width=32, frame_height=32):
        self.x = x
        self.y = y
        self.size = NPC_SIZE
        self.name = name
        self.dialogue = dialogue
        self.is_talking = False
        self.portrait_path = portrait_path
        self.portrait = None
        self.sprite_path = sprite_path
        self.sprite = None
        self.sprite_sheet = None
        self.current_frame = 0
        self.animation_frames = []
        self.is_sprite_sheet = is_sprite_sheet
        
        # ポートレート画像を読み込む
        if portrait_path:
            try:
                self.portrait = pygame.image.load(portrait_path)
                # 画像サイズを調整（会話ウィンドウ用）
                self.portrait = pygame.transform.scale(self.portrait, (150, 150))
                print(f"ポートレートを読み込みました: {portrait_path}")
            except Exception as e:
                print(f"ポートレートを読み込めませんでした: {portrait_path}")
                print(f"エラー: {e}")
        
        # スプライト画像を読み込む
        if sprite_path:
            try:
                if is_sprite_sheet:
                    # スプライトシートとして読み込み（元サイズで）
                    self.sprite_sheet = load_sprite_sheet(sprite_path, frame_width, frame_height, 1.0)
                    if self.sprite_sheet:
                        self.animation_frames = get_animation_frames(self.sprite_sheet, "down")
                        if self.animation_frames:
                            # フレームをゲームサイズに調整
                            self.sprite = pygame.transform.scale(self.animation_frames[0], (self.size, self.size))
                        print(f"スプライトシートを読み込みました: {sprite_path}")
                else:
                    # 単一画像として読み込み
                    self.sprite = pygame.image.load(sprite_path)
                    # スプライトサイズを調整
                    self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))
                    print(f"スプライトを読み込みました: {sprite_path}")
            except Exception as e:
                print(f"スプライトを読み込めませんでした: {sprite_path}")
                print(f"エラー: {e}")
        
    def draw(self, screen, font):
        # スプライト画像があれば描画、なければ青い四角
        if self.sprite:
            # 画像を中央に配置
            sprite_rect = self.sprite.get_rect()
            sprite_rect.center = (self.x + self.size // 2, self.y + self.size // 2)
            screen.blit(self.sprite, sprite_rect)
        else:
            pygame.draw.rect(screen, BLUE, (self.x, self.y, self.size, self.size))
        
        # Draw name above NPC
        name_text = font.render(self.name, True, WHITE)
        name_rect = name_text.get_rect(center=(self.x + self.size // 2, self.y - 10))
        screen.blit(name_text, name_rect)
    
    def get_center(self):
        return (self.x + self.size // 2, self.y + self.size // 2)
    
    def get_distance_to(self, player):
        px, py = player.get_center()
        nx, ny = self.get_center()
        return math.sqrt((px - nx)**2 + (py - ny)**2)