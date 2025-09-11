"""ストーリーモードのテスト"""
import sys
sys.path.append('src')

from game_state import GameState

# ゲーム状態をテスト
gs = GameState()
print(f"ストーリーモード: {gs.story_mode}")
print(f"バトルスキップ設定: {gs.skip_battles_until_boss}")
print(f"初期フェーズ: {gs.current_phase}")
print(f"初期目標: {gs.get_current_objective()}")

# クエスト進行シミュレーション
print("\n--- クエスト進行テスト ---")
gs.talked_to_elder = True
gs.update_phase()
print(f"村長と会話後の目標: {gs.get_current_objective()}")

# スライム討伐シミュレーション
for i in range(3):
    gs.defeated_slimes += 1
    gs.update_phase()
    print(f"スライム{i+1}体目討伐後: {gs.get_current_objective()}")

print(f"\n最終フェーズ: {gs.current_phase}")
print("ボスエリアへのアクセスが可能になりました！")