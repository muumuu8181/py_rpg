"""戦闘システムの定義"""
import pygame
from constants import *

class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.active = False
        self.turn = "player"  # player or enemy
        self.message = ""
        self.message_timer = 0
        
    def start(self):
        self.active = True
        self.message = f"{self.enemy.name}が現れた！"
        self.message_timer = 120
        
    def player_attack(self):
        damage = self.player.attack
        self.enemy.take_damage(damage)
        self.message = f"プレイヤーの攻撃！ {damage}のダメージ！"
        self.message_timer = 120
        if self.enemy.hp <= 0:
            self.message = f"{self.enemy.name}を倒した！"
            self.active = False
        else:
            self.turn = "enemy"
            
    def enemy_attack(self):
        damage = self.enemy.attack
        self.player.take_damage(damage)
        self.message = f"{self.enemy.name}の攻撃！ {damage}のダメージ！"
        self.message_timer = 120
        if self.player.hp <= 0:
            self.message = "プレイヤーは倒れてしまった..."
        else:
            self.turn = "player"
    
    def update(self):
        if self.message_timer > 0:
            self.message_timer -= 1
            
        # Auto enemy turn after message
        if self.turn == "enemy" and self.message_timer == 60:
            self.enemy_attack()
    
    def draw(self, screen, font):
        if not self.active:
            return
            
        # Draw battle UI background
        battle_box_height = 200
        battle_box_y = SCREEN_HEIGHT - battle_box_height - 20
        pygame.draw.rect(screen, BLACK, (20, battle_box_y, SCREEN_WIDTH - 40, battle_box_height))
        pygame.draw.rect(screen, WHITE, (20, battle_box_y, SCREEN_WIDTH - 40, battle_box_height), 2)
        
        # Draw HP bars
        # Player HP
        hp_bar_width = 200
        hp_bar_height = 20
        hp_ratio = self.player.hp / self.player.max_hp
        pygame.draw.rect(screen, WHITE, (40, battle_box_y + 20, hp_bar_width, hp_bar_height), 2)
        pygame.draw.rect(screen, GREEN, (40, battle_box_y + 20, int(hp_bar_width * hp_ratio), hp_bar_height))
        hp_text = font.render(f"プレイヤー HP: {self.player.hp}/{self.player.max_hp}", True, WHITE)
        screen.blit(hp_text, (40, battle_box_y + 45))
        
        # Enemy HP
        enemy_hp_ratio = self.enemy.hp / self.enemy.max_hp
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - 240, battle_box_y + 20, hp_bar_width, hp_bar_height), 2)
        pygame.draw.rect(screen, RED, (SCREEN_WIDTH - 240, battle_box_y + 20, int(hp_bar_width * enemy_hp_ratio), hp_bar_height))
        enemy_hp_text = font.render(f"{self.enemy.name} HP: {self.enemy.hp}/{self.enemy.max_hp}", True, WHITE)
        screen.blit(enemy_hp_text, (SCREEN_WIDTH - 240, battle_box_y + 45))
        
        # Draw message
        if self.message:
            msg_text = font.render(self.message, True, YELLOW)
            msg_rect = msg_text.get_rect(center=(SCREEN_WIDTH // 2, battle_box_y + 100))
            screen.blit(msg_text, msg_rect)
        
        # Draw action buttons (if player turn and no message)
        if self.turn == "player" and self.message_timer == 0 and self.player.hp > 0:
            action_text = font.render("スペースキー：攻撃　　ESCキー：逃げる", True, WHITE)
            action_rect = action_text.get_rect(center=(SCREEN_WIDTH // 2, battle_box_y + 150))
            screen.blit(action_text, action_rect)