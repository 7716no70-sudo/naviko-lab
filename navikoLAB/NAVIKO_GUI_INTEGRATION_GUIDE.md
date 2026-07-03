# Naviko GUI Enhancement - 統合ガイド

このガイドでは、新しく実装した3つのモジュールをnaviko.pyのTkinter GUIに統合する方法を説明します。

## 新モジュール概要

### 1. ErrorDiagnosticEngine (error_diagnostic_engine.py)
- エラー自動診断
- 日本語での解決策提案
- 自動修復機能

### 2. ExperienceMemory (experience_memory.py)
- エラー解決経験の蓄積
- 類似エラー検索
- 最適解決策提案

### 3. ProcessRecorder (process_recorder.py)
- 作業プロセス記録
- テンプレート化
- 別テーマでの再現

---

## 統合手順

### Step 1: naviko.py の import セクションに追加

```python
# naviko.py の冒頭に追加
from pathlib import Path
from navikoLAB.error_diagnostic_engine import ErrorDiagnosticEngine
from navikoLAB.experience_memory import ExperienceMemory
from navikoLAB.process_recorder import ProcessRecorder
```

### Step 2: NavikoApp クラスの __init__ に初期化コードを追加

```python
class NavikoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ナビ子 v1.5.0 - 自己改善AI")
        
        # ... 既存のコード ...
        
        # 新機能の初期化
        lab_dir = Path(__file__).parent / "navikoLAB"
        
        # ExperienceMemory初期化
        self.experience_memory = ExperienceMemory(lab_dir=lab_dir)
        
        # ErrorDiagnosticEngine初期化（ExperienceMemoryと連携）
        self.error_diagnostic = ErrorDiagnosticEngine(
            lab_dir=lab_dir,
            experience_memory=self.experience_memory
        )
        
        # ProcessRecorder初期化
        self.process_recorder = ProcessRecorder(lab_dir=lab_dir)
        
        # エラーパネルを作成
        self._create_error_panel()
        
        print("✅ ナビ子 v1.5.0 起動完了")
        print("   新機能: エラー診断、経験学習、プロセス記録")
```

### Step 3: エラーパネルの作成

```python
def _create_error_panel(self):
    """エラー診断パネルを作成"""
    # エラーパネルフレーム
    self.error_panel = tk.Frame(self.root, bg="#FFF3CD", padx=10, pady=10)
    # 初期状態では非表示
    
    # エラーメッセージ表示
    self.error_message_label = tk.Label(
        self.error_panel,
        text="",
        bg="#FFF3CD",
        fg="#856404",
        font=("Arial", 10),
        wraplength=600,
        justify=tk.LEFT
    )
    self.error_message_label.pack(anchor=tk.W)
    
    # 解決策ボタンフレーム
    self.solution_buttons_frame = tk.Frame(self.error_panel, bg="#FFF3CD")
    self.solution_buttons_frame.pack(fill=tk.X, pady=(5, 0))
```

### Step 4: エラーハンドリングを強化

```python
def handle_error(self, error_message: str, context: dict = None):
    """
    エラーを処理（新機能）
    
    Args:
        error_message: エラーメッセージ
        context: コンテキスト情報
    """
    # エラーを診断
    diagnosis = self.error_diagnostic.diagnose_error(error_message, context)
    
    # エラーパネルを表示
    self._show_error_panel(diagnosis)
    
    # 解決策を提案
    solutions = self.error_diagnostic.suggest_solutions(diagnosis)
    self._display_solutions(solutions, diagnosis)
    
    # チャット画面にも表示
    self.display_error_with_solutions(diagnosis, solutions)

def _show_error_panel(self, diagnosis: dict):
    """エラーパネルを表示"""
    self.error_panel.pack(fill=tk.X, padx=10, pady=(0, 10))
    
    error_text = f"⚠️ エラーが検出されました\n\n"
    error_text += f"エラータイプ: {diagnosis['error_type']}\n"
    error_text += f"カテゴリー: {diagnosis['category']} ({diagnosis['severity']})\n\n"
    error_text += f"🔍 ナビ子の診断:\n"
    
    if diagnosis.get('learned_solution'):
        error_text += f"✅ 過去の経験から解決策を見つけました！\n"
    else:
        for cause in diagnosis['common_causes'][:2]:
            error_text += f"  • {cause}\n"
    
    self.error_message_label.config(text=error_text)

def _display_solutions(self, solutions: list, diagnosis: dict):
    """解決策ボタンを表示"""
    # 既存のボタンをクリア
    for widget in self.solution_buttons_frame.winfo_children():
        widget.destroy()
    
    for i, solution in enumerate(solutions[:3]):  # 上位3つまで表示
        btn = tk.Button(
            self.solution_buttons_frame,
            text=solution['title'],
            command=lambda s=solution, d=diagnosis: self._apply_solution(s, d),
            bg="#28A745" if solution.get('auto_fixable') else "#007BFF",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=10,
            pady=5
        )
        btn.pack(side=tk.LEFT, padx=5)
    
    # 閉じるボタン
    close_btn = tk.Button(
        self.solution_buttons_frame,
        text="✕ 閉じる",
        command=self._hide_error_panel,
        bg="#DC3545",
        fg="white",
        padx=10,
        pady=5
    )
    close_btn.pack(side=tk.RIGHT, padx=5)

def _apply_solution(self, solution: dict, diagnosis: dict):
    """解決策を適用"""
    if solution.get('auto_fixable'):
        # 自動修復を実行
        result = self.error_diagnostic.auto_fix(solution, diagnosis)
        
        if result['success']:
            messagebox.showinfo("成功", result['message'])
            
            # 成功した解決策を記録
            self.experience_memory.record_solution(
                error_type=diagnosis['error_type'],
                error_message=diagnosis['original_error'],
                solution=solution['description'],
                success=True,
                context=diagnosis.get('context', {}),
                category=diagnosis['category'],
                severity=diagnosis['severity']
            )
            
            # エラーパネルを閉じる
            self._hide_error_panel()
        else:
            messagebox.showerror("エラー", result['message'])
    else:
        # 手動実行の手順を表示
        steps = "\n".join(solution.get('steps', ['詳細は解決策を参照してください']))
        messagebox.showinfo(
            solution['title'],
            f"{solution['description']}\n\n手順:\n{steps}"
        )

def _hide_error_panel(self):
    """エラーパネルを非表示"""
    self.error_panel.pack_forget()

def display_error_with_solutions(self, diagnosis: dict, solutions: list):
    """チャット画面にエラーと解決策を表示"""
    message = "⚠️ エラーが検出されました\n\n"
    message += f"**エラー内容:**\n{diagnosis['original_error'][:200]}...\n\n"
    
    message += f"**🔍 ナビ子の診断:**\n"
    message += f"エラータイプ: {diagnosis['error_type']}\n"
    message += f"カテゴリー: {diagnosis['category']} ({diagnosis['severity']})\n\n"
    
    if diagnosis.get('learned_solution'):
        learned = diagnosis['learned_solution']
        message += f"**🎓 過去の経験から（成功率: {learned['success_rate']:.0%}）:**\n"
        message += f"{learned['solution']}\n\n"
    
    message += f"**💡 提案する解決策:**\n"
    for i, solution in enumerate(solutions[:3], 1):
        auto_mark = " ✨自動修復対応" if solution.get('auto_fixable') else ""
        message += f"{i}. {solution['title']}{auto_mark}\n"
        message += f"   {solution['description']}\n\n"
    
    self.add_message("ナビ子", message)
```

### Step 5: 既存のエラーハンドリングを置き換え

既存のtry-exceptブロックを以下のように変更：

```python
# 変更前
try:
    # 何か処理
    pass
except Exception as e:
    print(f"エラー: {str(e)}")
    messagebox.showerror("エラー", str(e))

# 変更後
try:
    # 何か処理
    pass
except Exception as e:
    # 新しいエラーハンドリング
    self.handle_error(str(e), context={"operation": "処理名"})
```

---

## 追加機能: プロセスレコーダーの統合

### メニューに「プロセス記録」を追加

```python
def _create_menu(self):
    """メニューバーを作成"""
    menubar = tk.Menu(self.root)
    self.root.config(menu=menubar)
    
    # ... 既存のメニュー ...
    
    # プロセスメニュー
    process_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="プロセス", menu=process_menu)
    process_menu.add_command(label="記録開始", command=self._start_process_recording)
    process_menu.add_command(label="記録停止＆保存", command=self._stop_process_recording)
    process_menu.add_separator()
    process_menu.add_command(label="テンプレート一覧", command=self._show_process_templates)
    process_menu.add_command(label="プロセス再現", command=self._replay_process)

def _start_process_recording(self):
    """プロセス記録開始"""
    name = simpledialog.askstring("プロセス記録", "プロセス名を入力してください:")
    if name:
        result = self.process_recorder.start_recording(name)
        if result['success']:
            messagebox.showinfo("記録開始", f"プロセス '{name}' の記録を開始しました")
            self.add_message("ナビ子", f"📝 プロセス記録開始: {name}")
        else:
            messagebox.showerror("エラー", result['error'])

def _stop_process_recording(self):
    """プロセス記録停止＆保存"""
    if not self.process_recorder.current_recording:
        messagebox.showwarning("警告", "記録中のプロセスがありません")
        return
    
    name = simpledialog.askstring(
        "テンプレート保存",
        f"テンプレート名を入力してください\n（現在の記録: {self.process_recorder.current_recording['name']}）:"
    )
    
    if name:
        result = self.process_recorder.save_template(name)
        if result['success']:
            messagebox.showinfo("保存完了", f"テンプレート '{name}' を保存しました")
            self.add_message("ナビ子", f"✅ プロセステンプレート保存完了: {name}")
        else:
            messagebox.showerror("エラー", result.get('error', '不明なエラー'))
```

---

## 使用例: 今回のAPIキーエラーへの対応

```python
# naviko.py内のGroq API呼び出し部分
try:
    response = groq_client.chat.completions.create(...)
except Exception as e:
    # 新しいエラーハンドリング
    self.handle_error(
        error_message=str(e),
        context={
            "service": "Groq API",
            "operation": "chat_completion",
            "model": "llama-3.1-8b-instant"
        }
    )
    
    # これにより、ナビ子が自動で：
    # 1. エラーを診断（401 Unauthorized）
    # 2. 過去の経験から解決策を検索
    # 3. 「環境変数のAPIキーを更新」を提案
    # 4. ユーザーがボタンをクリックするだけで解決
```

---

## テスト手順

### 1. インポートテスト

```python
# naviko.py の先頭で実行
from navikoLAB.error_diagnostic_engine import ErrorDiagnosticEngine
from navikoLAB.experience_memory import ExperienceMemory
from navikoLAB.process_recorder import ProcessRecorder

print("✅ 全モジュールのインポート成功")
```

### 2. 初期化テスト

```python
from pathlib import Path

lab_dir = Path(__file__).parent / "navikoLAB"

experience_memory = ExperienceMemory(lab_dir=lab_dir)
error_diagnostic = ErrorDiagnosticEngine(lab_dir=lab_dir, experience_memory=experience_memory)
process_recorder = ProcessRecorder(lab_dir=lab_dir)

print("✅ 全モジュールの初期化成功")
```

### 3. エラー診断テスト

```python
# 401エラーのテスト
error_msg = "401 Client Error: Unauthorized for url: https://api.groq.com/openai/v1/chat/completions"

diagnosis = error_diagnostic.diagnose_error(error_msg)
print(error_diagnostic.format_diagnosis(diagnosis))

solutions = error_diagnostic.suggest_solutions(diagnosis)
print(error_diagnostic.format_solutions(solutions))
```

---

## バージョンアップ

naviko.py の __init__ で：

```python
self.root.title("ナビ子 v1.5.0 - 自己改善AI")
```

起動メッセージ：

```python
print("=" * 60)
print("🤖 ナビ子 v1.5.0 起動")
print("   新機能:")
print("   ✅ エラー自動診断・解決提案")
print("   ✅ 経験から学習する自己改善")
print("   ✅ プロセス記録・再現")
print("=" * 60)
```

---

## まとめ

この統合により、ナビ子は以下が可能になります：

1. **エラーを自分で診断**
   - 401 Unauthorized → 「APIキーが無効です」
   - ModuleNotFoundError → 「groqパッケージをインストールしてください」

2. **日本語で解決策を提案**
   - 具体的な手順を表示
   - 自動修復可能な場合はボタンを提供

3. **経験から学習**
   - 過去に解決したエラーを記録
   - 類似エラー発生時に最適解を提案
   - 成功率の高い解決策を優先

4. **プロセスを記録・再現**
   - ユーザーの作業手順を記録
   - 別のテーマで同じプロセスを再現
   - 「前回と同じように作って」が可能に

**次回セッションでの完全統合を推奨します！**
