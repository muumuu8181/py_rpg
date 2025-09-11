"""敵クラスの定義"""
import pygame
import math
from constants import *

class Enemy:
    def __init__(self, x, y, name="スライム", enemy_type="slime"):
        self.x = x
        self.y = y
        self.size = ENEMY_SIZE
        self.name = name
        self.enemy_type = enemy_type
        
        # 敵の種類によってステータスを設定
        if enemy_type == "slime":
            self.hp = 50
            self.max_hp = 50
            self.attack = 15
            self.defense = 0
            self.color = PURPLE
        elif enemy_type == "goblin":
            self.hp = 80
            self.max_hp = 80
            self.attack = 20
            self.defense = 2
            self.color = GREEN
        elif enemy_type == "orc":
            self.hp = 120
            self.max_hp = 120
            self.attack = 25
            self.defense = 5
            self.color = DARK_GREEN
        elif enemy_type == "ghost":
            self.hp = 100
            self.max_hp = 100
            self.attack = 30
            self.defense = 0
            self.color = LIGHT_BLUE
        else:
            # デフォルト
            self.hp = 50
            self.max_hp = 50
            self.attack = 15
            self.defense = 0
            self.color = PURPLE
        
    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        # Draw enemy name
        name_text = font.render(self.name, True, WHITE)
        name_rect = name_text.get_rect(center=(self.x + self.size // 2, self.y - 10))
        screen.blit(name_text, name_rect)
    
    def draw_at_position(self, screen, font, x, y):
        pygame.draw.rect(screen, self.color, (x, y, self.size, self.size))
        # Draw enemy name
        name_text = font.render(self.name, True, WHITE)
        name_rect = name_text.get_rect(center=(x + self.size // 2, y - 10))
        screen.blit(name_text, name_rect)
    
    def get_center(self):
        return (self.x + self.size // 2, self.y + self.size // 2)
    
    def get_distance_to(self, player):
        px, py = player.get_center()
        ex, ey = self.get_center()
        return math.sqrt((px - ex)**2 + (py - ey)**2)
    
    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)
        return self.hp > 0  # Returns True if still alive

class Boss(Enemy):
    """中ボスクラス"""
    def __init__(self, x, y, name="闇の騎士"):
        super().__init__(x, y, name)
        self.size = ENEMY_SIZE + 20  # ボスは大きめ
        self.hp = 150  # HPを200から150に減らす
        self.max_hp = 150
        self.attack = 20  # 攻撃力を少し下げる
        self.defense = 3  # 防御力も調整
        self.phase = 1  # 戦闘フェーズ
        self.special_attack_cooldown = 0
        
    def draw(self, screen, font):
        # ボスは濃い赤色
        pygame.draw.rect(screen, DARK_RED, (self.x, self.y, self.size, self.size))
        # Draw boss name
        name_text = font.render(self.name, True, YELLOW)
        name_rect = name_text.get_rect(center=(self.x + self.size // 2, self.y - 10))
        screen.blit(name_text, name_rect)
        
    def draw_at_position(self, screen, font, x, y):
        pygame.draw.rect(screen, DARK_RED, (x, y, self.size, self.size))
        # Draw boss name
        name_text = font.render(self.name, True, YELLOW)
        name_rect = name_text.get_rect(center=(x + self.size // 2, y - 10))
        screen.blit(name_text, name_rect)
        
    def get_attack_damage(self):
        """フェーズに応じた攻撃力を返す"""
        if self.hp < self.max_hp * 0.3:  # HP30%以下
            self.phase = 2
            return int(self.attack * 1.3)  # 攻撃力1.3倍に調整
        return self.attack