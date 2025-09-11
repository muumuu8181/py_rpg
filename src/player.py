"""プレイヤークラスの定義"""
import pygame
from constants import *
from item import Inventory
from skill import SkillSystem

class Player:
    def __init__(self, x, y):
        self.x = float(x)  # float型で精密な位置計算
        self.y = float(y)
        self.size = PLAYER_SIZE
        self.base_speed = PLAYER_SPEED_VILLAGE  # デフォルトは村の速度
        self.hp = 100
        self.max_hp = 100
        self.attack = 20
        self.defense = 5
        self.level = 1
        self.exp = 0
        self.exp_to_next_level = 100
        # 移動の滑らかさのための変数
        self.vel_x = 0.0  # 速度
        self.vel_y = 0.0
        self.acceleration = 0.5  # 加速度
        # インベントリ
        self.inventory = Inventory()
        # スキルシステム
        self.skills = SkillSystem()
        
    def move(self, keys, obstacles):
        old_x = self.x
        old_y = self.y
        
        # 目標速度を設定
        target_vel_x = 0
        target_vel_y = 0
        
        if keys[pygame.K_LEFT]:
            target_vel_x = -self.base_speed
        if keys[pygame.K_RIGHT]:
            target_vel_x = self.base_speed
        if keys[pygame.K_UP]:
            target_vel_y = -self.base_speed
        if keys[pygame.K_DOWN]:
            target_vel_y = self.base_speed
        
        # 速度を徐々に目標速度に近づける（加速・減速）
        self.vel_x += (target_vel_x - self.vel_x) * self.acceleration
        self.vel_y += (target_vel_y - self.vel_y) * self.acceleration
        
        # X軸方向の移動を先に処理
        self.x += self.vel_x
        player_rect = pygame.Rect(int(self.x), int(self.y), self.size, self.size)
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle):
                self.x = old_x
                self.vel_x = 0  # 衝突時は速度をリセット
                break
        
        # Y軸方向の移動を処理
        self.y += self.vel_y
        player_rect = pygame.Rect(int(self.x), int(self.y), self.size, self.size)
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle):
                self.y = old_y
                self.vel_y = 0  # 衝突時は速度をリセット
                break
        
        # Keep player within screen bounds
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.size))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.size))
    
    def draw(self, screen):
        pygame.draw.rect(screen, RED, (int(self.x), int(self.y), self.size, self.size))
    
    def draw_at_position(self, screen, x, y):
        pygame.draw.rect(screen, RED, (int(x), int(y), self.size, self.size))
    
    def get_center(self):
        return (self.x + self.size // 2, self.y + self.size // 2)
    
    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)
        return self.hp > 0  # Returns True if still alive
    
    def get_total_attack(self):
        """バフとスキルを含めた総攻撃力を取得"""
        base_attack = self.attack + self.skills.get_attack_bonus()
        return base_attack + self.inventory.buffs.get("attack_boost", 0)
    
    def get_total_defense(self):
        """バフとスキルを含めた総防御力を取得"""
        base_defense = self.defense + self.skills.get_defense_bonus()
        return base_defense + self.inventory.buffs.get("defense_boost", 0)
    
    def set_speed_for_map(self, map_id):
        """マップに応じて移動速度を設定"""
        if map_id == 0:  # 村
            self.base_speed = PLAYER_SPEED_VILLAGE
        elif map_id == 1:  # 森
            self.base_speed = PLAYER_SPEED_FIELD
        elif map_id == 2:  # ボスエリア
            self.base_speed = PLAYER_SPEED_BOSS
        else:
            self.base_speed = PLAYER_SPEED_VILLAGE
            
    def gain_exp(self, amount):
        """経験値を獲得"""
        # 経験値ブーストを適用
        boosted_amount = int(amount * self.skills.get_exp_multiplier())
        self.exp += boosted_amount
        messages = []
        if boosted_amount > amount:
            messages.append(f"{amount}の経験値 + {boosted_amount - amount}のボーナス経験値を獲得！")
        else:
            messages.append(f"{boosted_amount}の経験値を獲得！")
        
        # レベルアップチェック
        while self.exp >= self.exp_to_next_level:
            self.exp -= self.exp_to_next_level
            self.level_up()
            messages.append(f"レベル{self.level}に上がった！")
            messages.append(f"スキルポイントを１獲得！ (SP: {self.skills.skill_points})")
            
        return messages
        
    def level_up(self):
        """レベルアップ処理"""
        self.level += 1
        # スキルボーナスを適用
        hp_bonus = self.skills.get_hp_bonus()
        self.max_hp += 20 + hp_bonus
        self.hp = self.max_hp  # 全回復
        self.attack += 5
        self.defense += 2
        self.exp_to_next_level = self.level * 100  # 次のレベルに必要な経験値
        # スキルポイントを付与
        self.skills.add_skill_point(1)