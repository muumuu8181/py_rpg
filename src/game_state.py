"""ゲームの進行状態を管理"""

class GameState:
    def __init__(self):
        # ストーリー進行フラグ
        self.talked_to_elder = False      # 村長と話したか
        self.got_quest = False           # クエストを受けたか
        self.defeated_slimes = 0         # 倒したスライムの数
        self.got_key_item = False        # 鍵アイテムを入手したか
        self.boss_defeated = False       # 中ボスを倒したか
        self.got_items_from_merchant = False  # 商人からアイテムをもらったか
        
        # ゲーム進行段階
        self.current_phase = 0  # 0:開始, 1:村長と話す, 2:森で修行, 3:ボス戦可能, 4:ボス撃破
        
        # ストーリーモード設定
        self.story_mode = True           # True: 雑魚戦をスキップして会話のみ進める
        self.skip_battles_until_boss = True  # 中ボスまでバトルをスキップ
        
    def update_phase(self):
        """進行状況に応じてフェーズを更新"""
        if self.boss_defeated:
            self.current_phase = 4
        elif self.got_key_item:
            self.current_phase = 3
        elif self.defeated_slimes >= 3:
            self.current_phase = 2
        elif self.talked_to_elder:
            self.current_phase = 1
        else:
            self.current_phase = 0
            
    def get_current_objective(self):
        """現在の目標を返す"""
        if self.story_mode:
            objectives = {
                0: "村長に話しかけよう",
                1: "森でスライムに話しかけよう (戦闘スキップ)",
                2: "森の奥を探索しよう",
                3: "闇の騎士を倒そう！",
                4: "おめでとう！中ボスを倒した！"
            }
        else:
            objectives = {
                0: "村長に話しかけよう",
                1: "森でスライムを3体倒そう",
                2: "森の奥を探索しよう",
                3: "闇の騎士を倒そう！",
                4: "おめでとう！中ボスを倒した！"
            }
        return objectives.get(self.current_phase, "")