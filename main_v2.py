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
TILE_SIZE = 40
PLAYER_SIZE = 32
PLAYER_SPEED = 5
NPC_SIZE = 32
ENEMY_SIZE = 40
INTERACTION_DISTANCE = 50

# Colors
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
                NPC(300, 200, "商人", "いい品物がありますよ〜"),
                NPC(850, 400, "戦士", "モンスターには気をつけろ！"),
                NPC(200, 300, "子供", "お兄ちゃん、どこから来たの？")
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
                NPC(600, 200, "魔法使い", "この森には強いモンスターがいる..."),
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

def main():
    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("RPG Adventure")
    
    # Clock for controlling frame rate
    clock = pygame.time.Clock()
    
    # Create player
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    # Current map
    current_map_id = 0
    current_map = Map(current_map_id)
    
    # Create dialogue box
    dialogue_box = DialogueBox()
    
    # Battle system (will be created when needed)
    battle = None
    
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
                elif event.key == pygame.K_ESCAPE and battle and battle.active:
                    battle.active = False
                    battle.message = "逃げ出した！"
                    battle.message_timer = 60
        
        # Get key states
        keys = pygame.key.get_pressed()
        
        # Update
        if battle and battle.active:
            # Battle mode
            battle.update()
            if space_pressed and battle.turn == "player" and battle.message_timer == 0:
                battle.player_attack()
        elif not dialogue_box.active:
            # Normal mode
            player.move(keys, current_map.obstacles)
            
            # マップ遷移チェック
            if player.y <= 0 and current_map_id == 0:  # 村から北へ
                current_map_id = 1
                current_map = Map(current_map_id)
                player.y = SCREEN_HEIGHT - player.size - 10
            elif player.y >= SCREEN_HEIGHT - player.size and current_map_id == 1:  # 森から南へ
                current_map_id = 0
                current_map = Map(current_map_id)
                player.y = 10
            
            # Check for NPC interactions
            if space_pressed:
                for npc in current_map.npcs:
                    if npc.get_distance_to(player) < INTERACTION_DISTANCE:
                        dialogue_box.show(npc.name, npc.dialogue)
                        break
                
                # Check for enemy interaction
                for enemy in current_map.enemies:
                    if enemy.hp > 0 and enemy.get_distance_to(player) < INTERACTION_DISTANCE:
                        battle = Battle(player, enemy)
                        battle.start()
                        break
        else:
            # Dialogue mode
            if space_pressed:
                dialogue_box.hide()
        
        space_pressed = False
        
        # Draw
        screen.fill(BLACK)
        
        # Draw map
        current_map.draw_tiles(screen)
        current_map.draw_obstacles(screen)
        
        # Draw NPCs
        for npc in current_map.npcs:
            npc.draw(screen)
            # Show interaction hint
            if npc.get_distance_to(player) < INTERACTION_DISTANCE and not dialogue_box.active and not (battle and battle.active):
                hint_text = font.render("スペースキーで話す", True, YELLOW)
                hint_rect = hint_text.get_rect(center=(player.x + player.size // 2, player.y - 20))
                screen.blit(hint_text, hint_rect)
        
        # Draw enemies
        for enemy in current_map.enemies:
            if enemy.hp > 0:
                enemy.draw(screen)
                # Show battle hint
                if enemy.get_distance_to(player) < INTERACTION_DISTANCE and not dialogue_box.active and not (battle and battle.active):
                    hint_text = font.render("スペースキーで戦う", True, YELLOW)
                    hint_rect = hint_text.get_rect(center=(player.x + player.size // 2, player.y - 20))
                    screen.blit(hint_text, hint_rect)
        
        player.draw(screen)
        dialogue_box.draw(screen)
        if battle:
            battle.draw(screen)
        
        # マップ名表示
        map_names = ["村", "森"]
        map_text = font.render(f"現在地: {map_names[current_map_id]}", True, WHITE)
        screen.blit(map_text, (10, 10))
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()