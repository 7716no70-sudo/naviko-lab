# Phase 3-C: GUI統合設計仕様

## 概要
SystemHealthMonitorとNavikoSystemControllerの機能をnaviko.pyのチャットGUIに統合する。

## 統合箇所
* **関数**: `open_custom_chat_window()` (naviko.py 9415行目)
* **追加位置**: `top_menu` フレームの直下

## GUI構成

### 1. Health Panel (健全性パネル)
```
health_panel (Frame, bg="#1e1e24")
├── status_frame (左側)
│   ├── status_label (システム状態ラベル)
│   └── status_indicator (色分け円形インジケーター)
├── metrics_frame (中央)
│   ├── health_score_label (健全性スコア: XX/100)
│   ├── cpu_label (CPU: XX%)
│   └── memory_label (メモリ: XX%)
└── action_frame (右側)
    └── recovery_button (自動対処ボタン)
```

### 2. 色分けルール
* **正常 (緑)**: 健全性スコア >= 70
* **要注意 (黄)**: 50 <= 健全性スコア < 70
* **異常 (赤)**: 健全性スコア < 50

## 実装ステップ

### Step 1: モジュールインポート
```python
from navikoLAB.system_health_monitor import SystemHealthMonitor
from navikoLAB.naviko_system_controller import NavikoSystemController
```

### Step 2: グローバルインスタンス初期化
```python
# チャットウィンドウ開く前（またはプログラム起動時）
health_monitor = SystemHealthMonitor()
system_controller = NavikoSystemController()
```

### Step 3: health_panel追加 (open_custom_chat_window内)
```python
# top_menu の直後に追加
health_panel = tk.Frame(c_win, bg="#1e1e24", height=60)
health_panel.pack(fill=tk.X, padx=10, pady=5)
```

### Step 4: コンポーネント配置

#### 4-1: ステータスインジケーター (左側)
```python
status_frame = tk.Frame(health_panel, bg="#1e1e24")
status_frame.pack(side=tk.LEFT, padx=10)

status_label = tk.Label(
    status_frame,
    text="システム状態:",
    bg="#1e1e24",
    fg="#a0a0b8",
    font=("MS Gothic", 9)
)
status_label.pack(side=tk.TOP)

# 円形インジケーター (Canvas)
status_indicator = tk.Canvas(
    status_frame,
    width=30,
    height=30,
    bg="#1e1e24",
    highlightthickness=0
)
status_indicator.pack(side=tk.TOP)
status_circle = status_indicator.create_oval(
    5, 5, 25, 25,
    fill="#10b981",  # 初期: 緑
    outline=""
)
```

#### 4-2: メトリクス表示 (中央)
```python
metrics_frame = tk.Frame(health_panel, bg="#1e1e24")
metrics_frame.pack(side=tk.LEFT, padx=20, fill=tk.Y)

health_score_label = tk.Label(
    metrics_frame,
    text="健全性: --/100",
    bg="#1e1e24",
    fg="#ffffff",
    font=("MS Gothic", 10, "bold")
)
health_score_label.pack(anchor="w")

cpu_label = tk.Label(
    metrics_frame,
    text="CPU: --%",
    bg="#1e1e24",
    fg="#a0a0b8",
    font=("MS Gothic", 9)
)
cpu_label.pack(anchor="w")

memory_label = tk.Label(
    metrics_frame,
    text="メモリ: --%",
    bg="#1e1e24",
    fg="#a0a0b8",
    font=("MS Gothic", 9)
)
memory_label.pack(anchor="w")
```

#### 4-3: 自動対処ボタン (右側)
```python
action_frame = tk.Frame(health_panel, bg="#1e1e24")
action_frame.pack(side=tk.RIGHT, padx=10)

recovery_button = tk.Button(
    action_frame,
    text="🔧 自動診断・対処",
    command=lambda: run_auto_recovery(c_area),
    bg="#dc2626",
    fg="#ffffff",
    font=("MS Gothic", 9, "bold"),
    bd=0,
    padx=15,
    pady=10
)
recovery_button.pack()
```

### Step 5: 更新ロジック実装

#### 5-1: ダッシュボード更新関数
```python
def update_health_dashboard():
    """
    SystemHealthMonitorから最新データを取得してGUI更新
    """
    try:
        # ダッシュボードデータ取得
        dashboard = health_monitor.get_dashboard()
        
        # 健全性スコア取得
        health_score = dashboard["health_score"]
        
        # メトリクス取得
        metrics = dashboard["current_metrics"]
        cpu_usage = metrics["cpu_percent"]
        memory_usage = metrics["memory_percent"]
        
        # ラベル更新
        health_score_label.config(text=f"健全性: {health_score:.0f}/100")
        cpu_label.config(text=f"CPU: {cpu_usage:.1f}%")
        memory_label.config(text=f"メモリ: {memory_usage:.1f}%")
        
        # インジケーター色更新
        if health_score >= 70:
            color = "#10b981"  # 緑
            status_text = "正常"
        elif health_score >= 50:
            color = "#f59e0b"  # 黄
            status_text = "要注意"
        else:
            color = "#ef4444"  # 赤
            status_text = "異常"
        
        status_indicator.itemconfig(status_circle, fill=color)
        status_label.config(text=f"システム状態: {status_text}")
        
        # 次回更新スケジュール (5秒後)
        c_win.after(5000, update_health_dashboard)
        
    except Exception as e:
        print(f"❌ ダッシュボード更新エラー: {e}")
        # エラー時も再スケジュール
        c_win.after(10000, update_health_dashboard)
```

#### 5-2: 初回更新トリガー
```python
# チャットウィンドウ作成後に初回更新を開始
c_win.after(1000, update_health_dashboard)  # 1秒後に開始
```

#### 5-3: 自動対処実行関数
```python
def run_auto_recovery(c_area):
    """
    自動診断・対処を実行
    """
    try:
        append_chat_bubble(c_area, "navi", "🔧 自動診断を開始します...")
        
        # 安全性チェック実行
        check_result = system_controller.run_safety_check()
        
        if check_result["status"] == "healthy":
            append_chat_bubble(
                c_area,
                "navi",
                "✅ システムは正常です。問題は検出されませんでした。"
            )
        else:
            # 問題検出時
            issues = check_result.get("issues", [])
            append_chat_bubble(
                c_area,
                "navi",
                f"⚠️ {len(issues)}件の問題を検出しました。自動対処を試みます..."
            )
            
            # システムステータス取得
            status = system_controller.get_system_status()
            append_chat_bubble(
                c_area,
                "navi",
                f"システム状態:\n{json.dumps(status, indent=2, ensure_ascii=False)}"
            )
        
        # ダッシュボード即座に更新
        update_health_dashboard()
        
    except Exception as e:
        append_chat_bubble(
            c_area,
            "navi",
            f"❌ 自動対処エラー: {str(e)}"
        )
```

## 変更箇所サマリー

### naviko.py への追加・変更
1. **インポート追加** (ファイル上部)
   ```python
   from navikoLAB.system_health_monitor import SystemHealthMonitor
   from navikoLAB.naviko_system_controller import NavikoSystemController
   ```

2. **グローバルインスタンス初期化** (GUI起動前)
   ```python
   health_monitor = SystemHealthMonitor()
   system_controller = NavikoSystemController()
   ```

3. **`open_custom_chat_window()`関数内に追加**
   - health_panel フレーム
   - status_indicator (Canvas)
   - health_score_label, cpu_label, memory_label
   - recovery_button
   - update_health_dashboard() 関数
   - run_auto_recovery() 関数
   - 初回更新トリガー

## 期待される動作

1. チャットウィンドウを開くと、トップメニューの下にヘルスパネルが表示される
2. 5秒ごとにシステムメトリクスが自動更新される
3. 健全性スコアに応じてインジケーターの色が変化する
4. 「自動診断・対処」ボタンをクリックすると、システムチェック→結果表示が実行される
5. 問題検出時は、チャットエリアに詳細情報が表示される

## 次のステップ

* この設計仕様に基づいて、naviko.pyに実際のコードを追加
* 動作テスト実施
* Git同期（Workspace → GitHub → ローカルPC）
