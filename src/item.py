"""アイテムクラスの定義"""
import pygame
from constants import *

class Item:
    def __init__(self, item_type, name, value):
        self.type = item_type  # "potion", "key_item" など
        self.name = name
        self.value = value  # 回復量など
        
class Inventory:
    def __init__(self):
        self.items = {
            "potion": 3,  # 初期ポーション3個
            "super_potion": 0,  # 全回復ポーション
            "power_up": 0,  # 攻撃力アップ
            "defense_up": 0,  # 防御力アップ
            "key_item": 0  # 鍵アイテム
        }
        # バフ状態
        self.buffs = {
            "attack_boost": 0,  # 攻撃力ブースト量
            "defense_boost": 0,  # 防御力ブースト量
            "buff_turns": 0  # バフ残りターン数
        }
        
    def use_item(self, item_type, player):
        """アイテムを使用"""
        if self.items.get(item_type, 0) <= 0:
            return None
            
        if item_type == "potion":
            # ポーション使用
            heal_amount = 50
            old_hp = player.hp
            player.hp = min(player.hp + heal_amount, player.max_hp)
            self.items["potion"] -= 1
            return f"{player.hp - old_hp}回復した！"
            
        elif item_type == "super_potion":
            # スーパーポーション使用（全回復）
            old_hp = player.hp
            player.hp = player.max_hp
            self.items["super_potion"] -= 1
            return f"HPが全回復した！({player.hp - old_hp}回復)"
            
        elif item_type == "power_up":
            # 攻撃力アップ使用
            self.items["power_up"] -= 1
            self.buffs["attack_boost"] = 15  # 攻撃力+15
            self.buffs["buff_turns"] = 5  # 5ターン持続
            return "攻撃力が大幅にアップした！(5ターン)"
            
        elif item_type == "defense_up":
            # 防御力アップ使用
            self.items["defense_up"] -= 1
            self.buffs["defense_boost"] = 10  # 防御力+10
            self.buffs["buff_turns"] = 5  # 5ターン持続
            return "防御力が大幅にアップした！(5ターン)"
            
        return None
        
    def add_item(self, item_type, count=1):
        """アイテムを追加"""
        if item_type in self.items:
            self.items[item_type] += count
        else:
            self.items[item_type] = count
            
    def has_item(self, item_type):
        """アイテムを持っているか確認"""
        return self.items.get(item_type, 0) > 0
        
    def get_count(self, item_type):
        """アイテムの個数を取得"""
        return self.items.get(item_type, 0)