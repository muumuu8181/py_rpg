"""メインゲームループ"""
import pygame
import sys
from constants import *
from player import Player
from map import Map
from ui import DialogueBox
from battle import Battle
from camera import Camera
from game_state import GameState

def main():
    # Pygame初期化
    pygame.init()
    
    # フォント設定
    try:
        font = pygame.font.Font(FONT_PATH, FONT_SIZE)
    except:
        font = pygame.font.Font(None, 24)
    
    # 画面設定
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
    pygame.display.set_caption(f"RPG Adventure v{VERSION}")
    clock = pygame.time.Clock()
    
    # ゲームオブジェクト作成
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    game_state = GameState()
    current_map_id = 0
    current_map = Map(current_map_id)
    dialogue_box = DialogueBox()
    battle = None
    # camera = Camera(player)  # カメラは使わない
    
    # ゲームループ
    running = True
    space_pressed = False
    
    while running:
        # イベント処理
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
                elif event.key == pygame.K_h:  # Hキーで回復
                    if battle and battle.active and battle.turn == "player" and battle.message_timer == 0:
                        # バトル中のポーション使用
                        if player.inventory.get_count("potion") > 0:
                            result = player.inventory.use_item("potion", player)
                            if result:
                                battle.message = result
                                battle.message_timer = 120
                                battle.turn = "enemy"  # ターンを敵に渡す
                        elif player.inventory.get_count("super_potion") > 0:
                            result = player.inventory.use_item("super_potion", player)
                            if result:
                                battle.message = result
                                battle.message_timer = 120
                                battle.turn = "enemy"
                    elif not battle:
                        # 通常時のポーション使用
                        if player.inventory.get_count("potion") > 0:
                            result = player.inventory.use_item("potion", player)
                            if result:
                                dialogue_box.show("システム", [result])
                elif event.key == pygame.K_p and battle and battle.active and battle.turn == "player" and battle.message_timer == 0:
                    # Pキーで攻撃力UP
                    if player.inventory.get_count("power_up") > 0:
                        result = player.inventory.use_item("power_up", player)
                        if result:
                            battle.message = result
                            battle.message_timer = 120
                            battle.turn = "enemy"
                elif event.key == pygame.K_d and battle and battle.active and battle.turn == "player" and battle.message_timer == 0:
                    # Dキーで防御力UP
                    if player.inventory.get_count("defense_up") > 0:
                        result = player.inventory.use_item("defense_up", player)
                        if result:
                            battle.message = result
                            battle.message_timer = 120
                            battle.turn = "enemy"
                elif event.key == pygame.K_s and not battle and not dialogue_box.active:
                    # Sキーでスキルメニュー
                    skill_messages = []
                    skill_messages.append(f"スキルポイント: {player.skills.skill_points}")
                    skill_messages.append("")
                    for skill_name, skill in player.skills.skills.items():
                        skill_messages.append(f"{skill.name} Lv.{skill.level}/{skill.max_level}")
                        skill_messages.append(f"  {skill.description}")
                    skill_messages.append("")
                    skill_messages.append("スキルポイントはレベルアップ時に獲得できます")
                    dialogue_box.show("スキルメニュー", skill_messages)
        
        # キー状態取得
        keys = pygame.key.get_pressed()
        
        # 更新処理
        if battle and battle.active:
            # バトルモード
            battle.update()
            if space_pressed and battle.turn == "player" and battle.message_timer == 0:
                battle.player_attack()
        elif not dialogue_box.active:
            # 通常モード
            # NPCと敵の衝突判定用リストを作成
            character_obstacles = []
            
            # NPCを障害物として追加（少し大きめの当たり判定）
            for npc in current_map.npcs:
                # 少し余裕を持たせた判定箱
                padding = 5
                npc_rect = pygame.Rect(npc.x - padding, npc.y - padding, 
                                      npc.size + padding*2, npc.size + padding*2)
                character_obstacles.append(npc_rect)
            
            # 生きている敵を障害物として追加（少し大きめの当たり判定）
            for enemy in current_map.enemies:
                if enemy.hp > 0:
                    padding = 5
                    enemy_rect = pygame.Rect(enemy.x - padding, enemy.y - padding, 
                                           enemy.size + padding*2, enemy.size + padding*2)
                    character_obstacles.append(enemy_rect)
            
            # マップの障害物とキャラクター障害物を合わせて移動判定
            all_obstacles = current_map.obstacles + character_obstacles
            player.move(keys, all_obstacles)
            
            # プレイヤーの移動速度をマップに応じて設定
            player.set_speed_for_map(current_map_id)
            
            # マップ遷移
            if player.y <= 0 and current_map_id == 0:  # 村から北へ
                current_map_id = 1
                current_map = Map(current_map_id)
                player.y = SCREEN_HEIGHT - player.size - 10
                player.set_speed_for_map(current_map_id)
            elif player.y >= SCREEN_HEIGHT - player.size and current_map_id == 1:  # 森から南へ
                current_map_id = 0
                current_map = Map(current_map_id)
                player.y = 10
                player.set_speed_for_map(current_map_id)
            elif player.y <= 0 and current_map_id == 1 and game_state.defeated_slimes >= 3:  # 森から北（ボスエリア）へ
                current_map_id = 2
                current_map = Map(current_map_id)
                player.y = SCREEN_HEIGHT - player.size - 150
                player.set_speed_for_map(current_map_id)
            elif player.y >= SCREEN_HEIGHT - player.size and current_map_id == 2:  # ボスエリアから南へ
                current_map_id = 1
                current_map = Map(current_map_id)
                player.y = 10
                player.set_speed_for_map(current_map_id)
            
            # NPC との対話チェック
            if space_pressed:
                for npc in current_map.npcs:
                    if npc.get_distance_to(player) < INTERACTION_DISTANCE:
                        # 特別なNPCの対話処理
                        if npc.name == "商人":
                            # 商人の場合、アイテムを販売
                            if game_state.story_mode and not game_state.got_items_from_merchant:
                                # ストーリーモードなら特別アイテムを提供
                                dialogue = ["いらっしゃい！", 
                                          "ストーリーモードのお客様へ特別サービス！",
                                          "強化アイテムを無料で差し上げます！"]
                                # アイテムを追加
                                player.inventory.add_item("super_potion", 2)
                                player.inventory.add_item("power_up", 2)
                                player.inventory.add_item("defense_up", 2)
                                dialogue.append("スーパーポーションx2、攻撃UP x2、防御UP x2 を入手！")
                                dialogue.append("闇の騎士に挑戦する前に使ってくださいね！")
                                game_state.got_items_from_merchant = True
                            elif game_state.story_mode and game_state.got_items_from_merchant:
                                dialogue = ["もう強化アイテムをお渡ししましたね！",
                                          "闇の騎士は強敵です。",
                                          "バトル中にアイテムを使うのを忘れずに！",
                                          "H:ポーション P:攻撃UP D:防御UP"]
                            else:
                                # 通常モードの商品販売
                                dialogue = ["いらっしゃい！何かお探しですか？",
                                          "ポーションは50G、スーパーポーションは100Gです！"]
                            dialogue_box.show(npc.name, dialogue, npc.portrait)
                        elif npc.name == "村長":
                            if not game_state.talked_to_elder:
                                dialogue = ["ようこそ、我が村へ！", 
                                          "実は困ったことがあってな...",
                                          "北の森にモンスターが増えてしまった。",
                                          "まずはスライムを3体倒してくれないか？"]
                                game_state.talked_to_elder = True
                                game_state.got_quest = True
                            elif game_state.defeated_slimes < 3:
                                dialogue = [f"スライムを{game_state.defeated_slimes}/3体倒したな。",
                                          "あと{3 - game_state.defeated_slimes}体頼む！"]
                            elif not game_state.boss_defeated:
                                dialogue = ["よくやった！スライムを倒してくれたな！",
                                          "しかし森の奥にはもっと強い魔物がいる...",
                                          "闇の騎士と呼ばれる中ボスだ。",
                                          "準備ができたら挑戦してみてくれ！"]
                            else:
                                dialogue = ["素晴らしい！闇の騎士を倒してくれたのか！",
                                          "君は真の勇者だ！"]
                            dialogue_box.show(npc.name, dialogue, npc.portrait)
                        else:
                            dialogue_box.show(npc.name, npc.dialogue, npc.portrait)
                        break
                
                # 敵との戦闘チェック
                for enemy in current_map.enemies:
                    if enemy.hp > 0 and enemy.get_distance_to(player) < INTERACTION_DISTANCE:
                        # ストーリーモードなら全ての戦闘をスキップ
                        if game_state.story_mode:
                            # 経験値計算
                            if enemy.name == "闇の騎士":
                                exp_gain = 500
                                game_state.boss_defeated = True
                                dialogue = ["ストーリーモード: 闇の騎士を倒した！",
                                          f"{exp_gain}の経験値を獲得！",
                                          "おめでとう！ゲームクリア！"]
                            elif enemy.name == "スライム":
                                exp_gain = 50
                                if game_state.defeated_slimes < 3:
                                    game_state.defeated_slimes += 1
                                dialogue = [f"ストーリーモード: {enemy.name}を倒した！",
                                          f"{exp_gain}の経験値を獲得！"]
                            elif enemy.name == "ゴブリン":
                                exp_gain = 80
                                dialogue = [f"ストーリーモード: {enemy.name}を倒した！",
                                          f"{exp_gain}の経験値を獲得！"]
                            elif enemy.name == "オーク":
                                exp_gain = 120
                                dialogue = [f"ストーリーモード: {enemy.name}を倒した！",
                                          f"{exp_gain}の経験値を獲得！"]
                            elif enemy.name == "ゴースト":
                                exp_gain = 150
                                dialogue = [f"ストーリーモード: {enemy.name}を倒した！",
                                          f"{exp_gain}の経験値を獲得！"]
                            else:
                                exp_gain = 30
                                dialogue = [f"ストーリーモード: {enemy.name}を倒した！",
                                          f"{exp_gain}の経験値を獲得！"]
                            
                            # 経験値獲得とレベルアップ処理
                            level_up_messages = player.gain_exp(exp_gain)
                            dialogue.extend(level_up_messages)
                            
                            enemy.hp = 0  # 敵を倒した状態にする
                            dialogue_box.show("システム", dialogue)
                        else:
                            # 通常の戦闘開始
                            battle = Battle(player, enemy, game_state)
                            battle.start()
                        break
        else:
            # ダイアログモード
            if space_pressed:
                if not dialogue_box.next_line():
                    dialogue_box.hide()
        
        space_pressed = False
        
        # 描画処理
        screen.fill(BLACK)
        
        # マップ描画
        current_map.draw_tiles(screen)
        current_map.draw_obstacles(screen)
        
        # NPC描画
        for npc in current_map.npcs:
            npc.draw(screen, font)
            # インタラクションヒント
            if npc.get_distance_to(player) < INTERACTION_DISTANCE and not dialogue_box.active and not (battle and battle.active):
                hint_text = font.render("スペースキーで話す", True, YELLOW)
                hint_rect = hint_text.get_rect(center=(player.x + player.size // 2, player.y - 20))
                screen.blit(hint_text, hint_rect)
        
        # 敵描画
        for enemy in current_map.enemies:
            if enemy.hp > 0:
                enemy.draw(screen, font)
                # バトルヒント
                if enemy.get_distance_to(player) < INTERACTION_DISTANCE and not dialogue_box.active and not (battle and battle.active):
                    if game_state.story_mode and enemy.name != "闇の騎士":
                        hint_text = font.render("スペースキーで話を進める", True, YELLOW)
                    else:
                        hint_text = font.render("スペースキーで戦う", True, YELLOW)
                    hint_rect = hint_text.get_rect(center=(player.x + player.size // 2, player.y - 20))
                    screen.blit(hint_text, hint_rect)
        
        # プレイヤー描画
        player.draw(screen)
        
        # UI描画
        dialogue_box.draw(screen, font)
        if battle:
            battle.draw(screen, font)
        
        # マップ名表示
        map_names = ["村", "森", "ボスエリア"]
        map_text = font.render(f"現在地: {map_names[current_map_id]}", True, WHITE)
        screen.blit(map_text, (10, 10))
        
        # ステータス表示
        status_text = font.render(f"Lv.{player.level} HP:{player.hp}/{player.max_hp} ポーション:{player.inventory.get_count('potion')}個 SP:{player.skills.skill_points}", True, WHITE)
        screen.blit(status_text, (10, 40))
        
        # 経験値表示
        exp_text = font.render(f"EXP: {player.exp}/{player.exp_to_next_level}", True, WHITE)
        screen.blit(exp_text, (10, 70))
        
        # アイテム数表示
        if player.inventory.get_count('super_potion') > 0 or player.inventory.get_count('power_up') > 0 or player.inventory.get_count('defense_up') > 0:
            item_text = "アイテム: "
            if player.inventory.get_count('super_potion') > 0:
                item_text += f"スーパーポーション:{player.inventory.get_count('super_potion')} "
            if player.inventory.get_count('power_up') > 0:
                item_text += f"攻撃UP:{player.inventory.get_count('power_up')} "
            if player.inventory.get_count('defense_up') > 0:
                item_text += f"防御UP:{player.inventory.get_count('defense_up')} "
            item_render = font.render(item_text, True, WHITE)
            screen.blit(item_render, (10, 100))
        
        # ストーリーモード表示
        if game_state.story_mode:
            story_mode_text = font.render("[ストーリーモード] 雑魚戦スキップ", True, CYAN)
            screen.blit(story_mode_text, (SCREEN_WIDTH - 250, 40))
        
        # 現在の目標表示
        game_state.update_phase()
        objective_text = font.render(f"目標: {game_state.get_current_objective()}", True, YELLOW)
        screen.blit(objective_text, (10, 130))
        
        # 操作ヒント
        if not dialogue_box.active and not (battle and battle.active):
            hint_text = font.render("Hキー：ポーション使用 Sキー：スキルメニュー", True, WHITE)
            screen.blit(hint_text, (SCREEN_WIDTH - 280, 10))
        
        # 画面更新
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()