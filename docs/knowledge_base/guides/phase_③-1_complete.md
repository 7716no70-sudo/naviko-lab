# Phase ③-1: 音声起動改善 - 完了報告

**作成日**: 2026-07-08  
**ステータス**: ✅ 完了  
**所要時間**: 約2時間  
**実装者**: Assistant (Genie Code)

---

## 📋 概要

PC起動時にNavikoを自動起動し、バックグラウンドで常時待機する機能を実装しました。音声コマンド「ナビ子」で表示、「隠れて」で非表示に切り替えることができます。

---

## 🎯 目標（達成済み）

### 達成前の課題
* ❌ naviko.pyを手動で実行する必要がある
* ❌ 起動時に必ずウィンドウが表示される
* ❌ バックグラウンドモードがない

### 達成後の状態
* ✅ PC起動時に自動でNavikoが起動
* ✅ バックグラウンドで常時待機（画面に表示されない）
* ✅ 「ナビ子」で表示、「隠れて」で非表示に切り替え可能
* ✅ プロセスは常に音声を監視

---

## 🔧 実装内容

### 1. 起動時非表示機能（naviko.py）

**場所**: naviko.py 8505行目付近（16行追加）

**実装内容**:
```python
# ============================================================
# ③-1: 起動時非表示機能（--hidden引数対応）
# ============================================================
START_HIDDEN = "--hidden" in sys.argv
if START_HIDDEN:
    print("🔇 バックグラウンドモードで起動します（--hidden）")
else:
    print("🖥️ 通常モードで起動します")

root = tk.Tk()
# ... 他のGUI設定 ...

# 起動時非表示の場合、ウィンドウを隠す
if START_HIDDEN:
    root.withdraw()  # ウィンドウを非表示にする
    print("✅ メインウィンドウを非表示にしました（音声で呼び出し可能）")
```

**機能**:
* `--hidden` 引数で起動時にウィンドウを非表示
* `root.withdraw()` でGUIを生成するが画面に表示しない
* 音声認識は正常に動作

---

### 2. 音声コマンド「隠れて」（naviko.py）

**場所**: naviko.py 11055行目付近（14行追加）

**実装内容**:
```python
def on_wake_word_detected(detected_text):
    print(f"🎉 ウェイクワード検出: {detected_text}")
    
    # ③-1: 「隠れて」コマンド処理
    if "隠れて" in detected_text or "バックグラウンド" in detected_text or "かくれて" in detected_text:
        # チャットウィンドウを非表示にする
        if pet_vars.get("chat_win") and pet_vars["chat_win"].winfo_exists():
            pet_vars["chat_win"].withdraw()  # ウィンドウを非表示
            print("✅ チャットウィンドウを非表示にしました（バックグラウンドモード）")
            # ナビ子のidle状態に変更
            pet_vars["state"] = "idle"
            pet_vars["frame"] = 0
        else:
            print("⚠️ チャットウィンドウが見つかりません")
        return  # ここで処理終了
    
    # 既存の「ナビ子」処理（表示）
    # ...
```

**機能**:
* 「隠れて」「バックグラウンド」「かくれて」を検出
* チャットウィンドウを `withdraw()` で非表示
* プロセスは継続（音声監視は続く）

---

### 3. スタートアップランチャー（naviko_launcher.pyw）

**ファイル**: naviko_launcher.pyw（新規作成、3,362 bytes）

**特徴**:
* `.pyw` 拡張子でコンソールウィンドウが表示されない
* `subprocess.Popen` でnavikoを独立プロセスとして起動
* エラーハンドリング付き
* 起動ログとエラーログを記録

**主要機能**:
```python
# naviko.pyをバックグラウンドモード（--hidden）で起動
process = subprocess.Popen(
    [python_exe, str(naviko_path), "--hidden"],
    cwd=str(script_dir),
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
)
```

**ログファイル**:
* `naviko_launcher.log`: 起動成功ログ
* `naviko_launcher_error.log`: エラーログ

---

### 4. スタートアップ登録手順書（STARTUP_GUIDE.md）

**ファイル**: STARTUP_GUIDE.md（新規作成、8,222 bytes）

**内容**:
1. スタートアップフォルダの開き方（2つの方法）
2. ショートカット作成手順（手動/自動）
3. 動作確認方法
4. トラブルシューティング（4つの問題パターン）
5. 自動起動の無効化方法
6. 起動ログの確認方法

---

## 📊 変更ファイル

| ファイル | 変更内容 | 行数変化 |
|---------|---------|----------|
| `naviko.py` | 起動時非表示 + 「隠れて」コマンド追加 | +30行 (11,075 → 11,105) |
| `naviko_launcher.pyw` | 新規作成 | +93行 |
| `STARTUP_GUIDE.md` | 新規作成 | +264行 |
| `naviko.py.backup_before_③-1_*` | バックアップ作成 | - |

**Git コミット**:
```
feat: ③-1 音声起動改善（起動時非表示・隠れてコマンド・スタートアップランチャー）

実装内容:
- naviko.py: --hidden引数で起動時非表示機能追加
- naviko.py: 「隠れて」音声コマンドでウィンドウ非表示機能追加
- naviko_launcher.pyw: PC起動時の自動起動ランチャー作成
- STARTUP_GUIDE.md: スタートアップ登録手順書作成

機能:
- PC起動時に自動でNavikoがバックグラウンドモードで起動
- 「ナビ子」で画面表示、「隠れて」でバックグラウンドに戻る
- プロセスは常に音声を監視し続ける
```

---

## 🚀 使用方法

### 手動起動（テスト用）

#### 通常モード
```bash
python naviko.py
```

#### バックグラウンドモード
```bash
python naviko.py --hidden
```

### 自動起動設定

詳細は `STARTUP_GUIDE.md` を参照してください。

**簡単な手順**:
1. Win + R → `shell:startup` → Enter
2. `naviko_launcher.pyw` のショートカットをスタートアップフォルダにコピー
3. PC再起動

---

## 🎤 音声コマンド

### 表示コマンド
* **「ナビ子」**
  - チャットウィンドウを表示
  - 前面に持ってくる
  - フォーカスを当てる

### 非表示コマンド
* **「隠れて」**
* **「バックグラウンド」**
* **「かくれて」**
  - チャットウィンドウを非表示
  - プロセスは継続（音声監視は続く）

---

## ✅ テスト結果

### Workspaceでの実装確認
* ✅ バックアップ作成成功
* ✅ naviko.pyへのコード追加成功
* ✅ naviko_launcher.pyw作成成功
* ✅ STARTUP_GUIDE.md作成成功
* ✅ Git commit_and_push成功

### ローカルPCでの動作確認（TODO #5）
* ⏳ ローカルPCで実施予定
  - `python naviko.py --hidden` でウィンドウ非表示確認
  - 「ナビ子」で表示確認
  - 「隠れて」で非表示確認
  - PC再起動で自動起動確認

---

## 🔍 トラブルシューティング

### 問題1: PC起動後もNavikoが起動しない

**対策**:
1. スタートアップフォルダにショートカットがあるか確認
2. ショートカットのパスが正しいか確認
3. `naviko_launcher_error.log` でエラーを確認

### 問題2: コンソールウィンドウが表示される

**対策**:
1. `pythonw.exe` を使用しているか確認
2. `.pyw` 拡張子のファイルを使用しているか確認

### 問題3: 音声コマンドが動作しない

**対策**:
1. マイクが認識されているか確認
2. Voskモデルが存在するか確認
3. 手動起動でログを確認

詳細は `STARTUP_GUIDE.md` を参照してください。

---

## 🎯 次のステップ

### ③-2: 返答専用チャット画面の作成
* マスター画面とは別の返答専用ウィンドウを作成
* 所要時間: 3-4時間（推定）

### ③-3: UIデザイン改善
* ボタン配置の整理
* スマホアプリのような自由配置システム
* 所要時間: 1-2時間（短期）、5-8時間（長期）

---

## 📝 関連ドキュメント

* `STARTUP_GUIDE.md`: スタートアップ登録手順書
* `naviko_launcher.pyw`: スタートアップランチャー
* `docs/knowledge_base/guides/session_20260708.md`: 前回セッション記録
* `docs/knowledge_base/phases/phase_d_1.md`: Vosk音声起動基盤

---

## 🔒 注意事項

### バックアップファイル
* `naviko.py.backup_before_③-1_*` はGitにコミットしていません
* ローカルにのみ保存されています
* 必要に応じて手動で削除してください

### システム要件
* Windows 10/11
* Python 3.x
* Voskモデル（`C:\vosk_models\vosk-model-small-ja-0.22`）
* マイク（音声入力用）

---

**結論**: Phase ③-1の実装は完了しました。PC起動時の自動起動、バックグラウンドモード、音声コマンドによる表示/非表示切り替えがすべて実装され、ローカルPCでのテストを待つのみです。

---

**作成日**: 2026-07-08  
**最終更新**: 2026-07-08
