"""スキルシステム"""

class Skill:
    def __init__(self, name, description, max_level=5):
        self.name = name
        self.description = description
        self.level = 0
        self.max_level = max_level
        
    def level_up(self):
        """スキルレベルを上げる"""
        if self.level < self.max_level:
            self.level += 1
            return True
        return False
        
    def get_effect_value(self):
        """スキル効果の値を取得"""
        return self.level

class SkillSystem:
    def __init__(self):
        self.skill_points = 0
        self.skills = {
            "attack_boost": Skill("攻撃力強化", "攻撃力を恒久的に増加させる", 10),
            "defense_boost": Skill("防御力強化", "防御力を恒久的に増加させる", 10),
            "hp_boost": Skill("HP強化", "最大HPを恒久的に増加させる", 10),
            "critical": Skill("クリティカル", "クリティカル率を上昇させる", 5),
            "exp_boost": Skill("経験値ブースト", "獲得経験値を増加させる", 5)
        }
        
    def add_skill_point(self, amount=1):
        """スキルポイントを追加"""
        self.skill_points += amount
        
    def upgrade_skill(self, skill_name):
        """スキルをアップグレード"""
        if self.skill_points <= 0:
            return False, "スキルポイントが不足しています"
            
        if skill_name not in self.skills:
            return False, "そのスキルは存在しません"
            
        skill = self.skills[skill_name]
        if skill.level_up():
            self.skill_points -= 1
            return True, f"{skill.name}がLv.{skill.level}になった！"
        else:
            return False, f"{skill.name}は最大レベルです"
            
    def get_attack_bonus(self):
        """攻撃力ボーナスを計算"""
        return self.skills["attack_boost"].level * 3
        
    def get_defense_bonus(self):
        """防御力ボーナスを計算"""
        return self.skills["defense_boost"].level * 2
        
    def get_hp_bonus(self):
        """HPボーナスを計算"""
        return self.skills["hp_boost"].level * 10
        
    def get_critical_rate(self):
        """クリティカル率を計算"""
        return self.skills["critical"].level * 0.05  # 5%ずつ上昇
        
    def get_exp_multiplier(self):
        """経験値倍率を計算"""
        return 1.0 + (self.skills["exp_boost"].level * 0.1)  # 10%ずつ上昇