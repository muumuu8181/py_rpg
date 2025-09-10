import pygame
import sys
import math

# Initialize Pygame
pygame.init()
# 日本語フォントを使用（Windows標準のメイリオ）
try:
    font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 20)
except:
    # フォントが見つからない場合はデフォルトフォントを使用
    font = pygame.font.Font(None, 24)

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
PLAYER_SIZE = 32
PLAYER_SPEED = 5
NPC_SIZE = 32
INTERACTION_DISTANCE = 50
ENEMY_SIZE = 40

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
DARK_RED = (139, 0, 0)

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
        
    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        
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

class NPC:
    def __init__(self, x, y, name, dialogue):
        self.x = x
        self.y = y
        self.size = NPC_SIZE
        self.name = name
        self.dialogue = dialogue
        self.is_talking = False
        
    def draw(self, screen):
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

class DialogueBox:
    def __init__(self):
        self.active = False
        self.text = ""
        self.speaker = ""
        
    def show(self, speaker, text):
        self.active = True
        self.speaker = speaker
        self.text = text
    
    def hide(self):
        self.active = False
    
    def draw(self, screen):
        if not self.active:
            return
            
        # Draw dialogue box
        box_height = 120
        box_y = SCREEN_HEIGHT - box_height - 20
        pygame.draw.rect(screen, BLACK, (20, box_y, SCREEN_WIDTH - 40, box_height))
        pygame.draw.rect(screen, WHITE, (20, box_y, SCREEN_WIDTH - 40, box_height), 2)
        
        # Draw speaker name
        speaker_text = font.render(self.speaker + ":", True, YELLOW)
        screen.blit(speaker_text, (30, box_y + 10))
        
        # Draw dialogue text
        dialogue_text = font.render(self.text, True, WHITE)
        screen.blit(dialogue_text, (30, box_y + 40))
        
        # Draw instruction
        instruction_text = font.render("スペースキーで閉じる", True, WHITE)
        screen.blit(instruction_text, (30, box_y + 80))

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = ENEMY_SIZE
        self.hp = 50
        self.max_hp = 50
        self.attack = 15
        self.name = "スライム"
        
    def draw(self, screen):
        pygame.draw.rect(screen, PURPLE, (self.x, self.y, self.size, self.size))
        # Draw enemy name
        name_text = font.render(self.name, True, WHITE)
        name_rect = name_text.get_rect(center=(self.x + self.size // 2, self.y - 10))
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
    
    def draw(self, screen):
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

def main():
    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Minimal RPG")
    
    # Clock for controlling frame rate
    clock = pygame.time.Clock()
    
    # Create player
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    # Create NPCs
    npcs = [
        NPC(200, 150, "村長", "ようこそ、我が村へ！"),
        NPC(500, 200, "商人", "いい品物がありますよ〜"),
        NPC(350, 400, "戦士", "モンスターには気をつけろ！"),
        NPC(800, 350, "魔法使い", "魔法の力を感じる..."),
        NPC(150, 350, "子供", "お兄ちゃん、どこから来たの？")
    ]
    
    # Create enemy
    enemy = Enemy(900, 500)
    
    # Create dialogue box
    dialogue_box = DialogueBox()
    
    # Create battle system
    battle = Battle(player, enemy)
    
    # Game loop
    running = True
    space_pressed = False
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space_pressed = True
                elif event.key == pygame.K_ESCAPE and battle.active:
                    battle.active = False
                    battle.message = "逃げ出した！"
                    battle.message_timer = 60
        
        # Get key states
        keys = pygame.key.get_pressed()
        
        # Update
        if battle.active:
            # Battle mode
            battle.update()
            if space_pressed and battle.turn == "player" and battle.message_timer == 0:
                battle.player_attack()
        elif not dialogue_box.active:
            # Normal mode
            player.move(keys)
            
            # Check for NPC interactions
            if space_pressed:
                for npc in npcs:
                    if npc.get_distance_to(player) < INTERACTION_DISTANCE:
                        dialogue_box.show(npc.name, npc.dialogue)
                        break
                
                # Check for enemy interaction
                if enemy.hp > 0 and enemy.get_distance_to(player) < INTERACTION_DISTANCE:
                    battle.start()
        else:
            # Dialogue mode
            if space_pressed:
                dialogue_box.hide()
        
        space_pressed = False
        
        # Draw
        screen.fill(BLACK)
        
        # Draw NPCs
        for npc in npcs:
            npc.draw(screen)
            # Show interaction hint
            if npc.get_distance_to(player) < INTERACTION_DISTANCE and not dialogue_box.active and not battle.active:
                hint_text = font.render("スペースキーで話す", True, YELLOW)
                hint_rect = hint_text.get_rect(center=(player.x + player.size // 2, player.y - 20))
                screen.blit(hint_text, hint_rect)
        
        # Draw enemy if alive
        if enemy.hp > 0:
            enemy.draw(screen)
            # Show battle hint
            if enemy.get_distance_to(player) < INTERACTION_DISTANCE and not dialogue_box.active and not battle.active:
                hint_text = font.render("スペースキーで戦う", True, YELLOW)
                hint_rect = hint_text.get_rect(center=(player.x + player.size // 2, player.y - 20))
                screen.blit(hint_text, hint_rect)
        
        player.draw(screen)
        dialogue_box.draw(screen)
        battle.draw(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()