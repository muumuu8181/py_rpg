"""プレイヤークラスの定義"""
import pygame
from constants import *

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.hp = 100
        self.max_hp = 100
        self.attack = 20
        self.level = 1
        
    def move(self, keys, obstacles):
        old_x = self.x
        old_y = self.y
        
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        
        # Check collision with obstacles
        player_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle):
                self.x = old_x
                self.y = old_y
                break
        
        # Keep player on screen
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.size))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.size))
    
    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.size, self.size))
    
    def get_center(self):
        return (self.x + self.size // 2, self.y + self.size // 2)
    
    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)
        return self.hp > 0  # Returns True if still alive