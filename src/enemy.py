"""敵クラスの定義"""
import pygame
import math
from constants import *

class Enemy:
    def __init__(self, x, y, name="スライム"):
        self.x = x
        self.y = y
        self.size = ENEMY_SIZE
        self.hp = 50
        self.max_hp = 50
        self.attack = 15
        self.name = name
        
    def draw(self, screen, font):
        pygame.draw.rect(screen, PURPLE, (self.x, self.y, self.size, self.size))
        # Draw enemy name
        name_text = font.render(self.name, True, WHITE)
        name_rect = name_text.get_rect(center=(self.x + self.size // 2, self.y - 10))
        screen.blit(name_text, name_rect)
    
    def draw_at_position(self, screen, font, x, y):
        pygame.draw.rect(screen, PURPLE, (x, y, self.size, self.size))
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