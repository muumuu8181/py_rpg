"""プレイヤークラスの定義"""
import pygame
from constants import *

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = PLAYER_SIZE
        self.base_speed = PLAYER_SPEED_VILLAGE  # デフォルトは村の速度
        self.hp = 100
        self.max_hp = 100
        self.attack = 20
        self.level = 1
        
    def move(self, keys, obstacles):
        old_x = self.x
        old_y = self.y
        
        if keys[pygame.K_LEFT]:
            self.x -= self.base_speed
        if keys[pygame.K_RIGHT]:
            self.x += self.base_speed
        if keys[pygame.K_UP]:
            self.y -= self.base_speed
        if keys[pygame.K_DOWN]:
            self.y += self.base_speed
        
        # Check collision with obstacles
        player_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle):
                self.x = old_x
                self.y = old_y
                break
        
        # Keep player within map bounds
        self.x = max(0, min(self.x, MAP_WIDTH - self.size))
        self.y = max(0, min(self.y, MAP_HEIGHT - self.size))
    
    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.size, self.size))
    
    def draw_at_position(self, screen, x, y):
        pygame.draw.rect(screen, RED, (x, y, self.size, self.size))
    
    def get_center(self):
        return (self.x + self.size // 2, self.y + self.size // 2)
    
    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)
        return self.hp > 0  # Returns True if still alive
    
    def set_speed_for_map(self, map_id):
        """マップに応じて移動速度を設定"""
        if map_id == 0:  # 村
            self.base_speed = PLAYER_SPEED_VILLAGE
        elif map_id == 1:  # 森
            self.base_speed = PLAYER_SPEED_FIELD
        else:
            self.base_speed = PLAYER_SPEED_VILLAGE