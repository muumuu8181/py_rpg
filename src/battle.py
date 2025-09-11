"""戦闘システムの定義"""
import pygame
import random
from constants import *
from enemy import Boss

class Battle:
    def __init__(self, player, enemy, game_state=None):
        self.player = player
        self.enemy = enemy
        self.game_state = game_state
        self.active = False
        self.turn = "player"  # player or enemy
        self.message = ""
        self.message_timer = 0
        self.victory_exp = 0  # 獲得経験値
        self.victory_items = []  # ドロップアイテム
        self.level_up_messages = []  # レベルアップメッセージ
        
    def start(self):
        self.active = True
        self.message = f"{self.enemy.name}が現れた！"
        self.message_timer = 120
        
    def player_attack(self):
        # 防御力を考慮したダメージ計算（バフを考慮）
        base_damage = self.player.get_total_attack()
        enemy_defense = getattr(self.enemy, 'defense', 0)
        damage = max(1, base_damage - enemy_defense)
        
        self.enemy.take_damage(damage)
        self.message = f"プレイヤーの攻撃！ {damage}のダメージ！"
        self.message_timer = 120
        
        if self.enemy.hp <= 0:
            self.victory()
        else:
            self.turn = "enemy"
            
    def enemy_attack(self):
        # ボスの場合は特殊攻撃を考慮
        if isinstance(self.enemy, Boss):
            damage = int(self.enemy.get_attack_damage())
        else:
            damage = self.enemy.attack
            
        # 防御力を考慮（バフを考慮）
        actual_damage = max(1, damage - self.player.get_total_defense())
        self.player.take_damage(actual_damage)
        
        self.message = f"{self.enemy.name}の攻撃！ {actual_damage}のダメージ！"
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
            
        # バフターンをカウントダウン
        if self.turn == "player" and self.message_timer == 0 and self.player.inventory.buffs["buff_turns"] > 0:
            self.player.inventory.buffs["buff_turns"] -= 1
            if self.player.inventory.buffs["buff_turns"] == 0:
                # バフ終了
                self.player.inventory.buffs["attack_boost"] = 0
                self.player.inventory.buffs["defense_boost"] = 0
            
    def victory(self):
        """勝利時の処理"""
        # 経験値計算
        if isinstance(self.enemy, Boss):
            self.victory_exp = 500
        else:
            self.victory_exp = 50
            
        # アイテムドロップ
        if isinstance(self.enemy, Boss):
            # ボスは必ず鍵アイテムドロップ
            self.player.inventory.add_item("key_item", 1)
            self.victory_items.append("鍵アイテム")
            if self.game_state:
                self.game_state.got_key_item = True
                self.game_state.boss_defeated = True
        else:
            # 通常敵は確率でポーションドロップ
            if random.random() < 0.3:  # 30%の確率
                self.player.inventory.add_item("potion", 1)
                self.victory_items.append("ポーション")
                
        # ゲーム進行更新
        if self.game_state and self.enemy.name == "スライム":
            self.game_state.defeated_slimes += 1
            
        # 経験値獲得
        self.level_up_messages = self.player.gain_exp(self.victory_exp)
        
        # メッセージ作成
        self.message = f"{self.enemy.name}を倒した！"
        if self.victory_items:
            self.message += f" {', '.join(self.victory_items)}を手に入れた！"
        
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
        hp_text = font.render(f"プレイヤー Lv.{self.player.level} HP: {self.player.hp}/{self.player.max_hp}", True, WHITE)
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
            action_text = font.render("スペース：攻撃  H：ポーション  P：攻撃UP  D：防御UP  ESC：逃げる", True, WHITE)
            action_rect = action_text.get_rect(center=(SCREEN_WIDTH // 2, battle_box_y + 150))
            screen.blit(action_text, action_rect)
            
        # バフ状態表示
        if self.player.inventory.buffs["buff_turns"] > 0:
            buff_text = ""
            if self.player.inventory.buffs["attack_boost"] > 0:
                buff_text = f"攻撃力+{self.player.inventory.buffs['attack_boost']} "
            if self.player.inventory.buffs["defense_boost"] > 0:
                buff_text += f"防御力+{self.player.inventory.buffs['defense_boost']} "
            buff_text += f"(残り{self.player.inventory.buffs['buff_turns']}ターン)"
            
            buff_render = font.render(buff_text, True, YELLOW)
            screen.blit(buff_render, (40, battle_box_y + 75))