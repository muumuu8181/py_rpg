# Minimal RPG Game

A simple RPG game with basic player movement using Pygame.

## 重要なルール（AIアシスタント向け）
- **新しいファイルやフォルダを作成する前に必ずユーザーに相談すること**
- **このREADMEファイルは必要以上に編集しないこと**
- **同じ内容を重複して書かないこと**
- **作業はこのフォルダ内で完結させ、外部を汚さないこと**

## Setup
```bash
pip install -r requirements.txt
```

## Run
```bash
# 旧バージョン
python main.py

# 新バージョン（モジュール化済み）
python src/main.py
```

## Controls
- 矢印キー: 移動
- スペースキー: 話す/戦う/決定
- ESCキー: 戦闘から逃げる

## フォルダ構造
```
minimal-rpg-game/
├── src/              # ソースコード
├── assets/           # 画像・音声リソース
│   ├── sprites/      # キャラクター画像
│   ├── tiles/        # マップチップ
│   └── fonts/        # フォント
├── maps/            # マップデータ
└── config/          # 設定ファイル
```