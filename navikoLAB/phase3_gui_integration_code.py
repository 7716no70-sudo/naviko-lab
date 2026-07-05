#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3-C GUI統合コード

このファイルは、naviko.pyに追加するコードのテンプレートです。
以下の3つのセクションに分かれています：

【セクション1】ファイル冒頭に追加するインポート文
【セクション2】GUI起動前に追加するグローバル変数初期化
【セクション3】open_custom_chat_window()関数内に追加するコード

ローカルPCのnaviko.pyに手動で追加してください。
"""

# ============================================================================
# 【セクション1】ファイル冒頭に追加するインポート文
# ============================================================================
# naviko.py の既存インポート文の後（70行目付近）に追加

# Phase 3モジュールインポート
try:
    from navikoLAB.system_health_monitor import SystemHealthMonitor
    from navikoLAB.naviko_system_controller import NavikoSystemController
    PHASE3_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Phase 3モジュールが見つかりません: {e}")
    PHASE3_AVAILABLE = False
    SystemHealthMonitor = None
    NavikoSystemController = None


# ============================================================================
# 【セクション2】GUI起動前に追加するグローバル変数初期化
# ============================================================================
# naviko.py の "root = tk.Tk()" の直前（8177行目付近）に追加

# Phase 3モジュールのグローバルインスタンス
health_monitor = None
system_controller = None

if PHASE3_AVAILABLE:
    try:
        health_monitor = SystemHealthMonitor(
            lab_dir=str(ROOT / "navikoLAB")
        )
        system_controller = NavikoSystemController(
            lab_dir=str(ROOT / "navikoLAB")
        )
        print("✅ Phase 3モジュール初期化完了")
    except Exception as e:
        print(f"⚠️ Phase 3モジュール初期化失敗: {e}")
        health_monitor = None
        system_controller = None
else:
    print("⚠️ Phase 3モジュール無効（インポート失敗）")


# ============================================================================
# 【セクション3】open_custom_chat_window()関数内に追加するコード
# ============================================================================
# 以下のコードを open_custom_chat_window() 関数内の適切な位置に追加
# 推奨位置: top_menu.pack() の直後（9552行目付近）

# ============================================================================
# Phase 3-C: Health Panel（健全性ダッシュボード）
# ============================================================================

if PHASE3_AVAILABLE and health_monitor and system_controller:
    # health_panel フレーム
    health_panel = tk.Frame(c_win, bg="#1e1e24", height=60)
    health_panel.pack(fill=tk.X, padx=10, pady=5)
    
    # --------------------------------------------------------------------
    # 左側: ステータスインジケーター
    # --------------------------------------------------------------------
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
    
    # --------------------------------------------------------------------
    # 中央: メトリクス表示
    # --------------------------------------------------------------------
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
    
    # --------------------------------------------------------------------
    # 右側: 自動対処ボタン
    # --------------------------------------------------------------------
    action_frame = tk.Frame(health_panel, bg="#1e1e24")
    action_frame.pack(side=tk.RIGHT, padx=10)
    
    # run_auto_recovery関数の定義（ボタンより先に定義）
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
                status_text = json.dumps(status, indent=2, ensure_ascii=False)
                append_chat_bubble(
                    c_area,
                    "navi",
                    f"システム状態:\n{status_text}"
                )
            
            # ダッシュボード即座に更新
            update_health_dashboard()
            
        except Exception as e:
            append_chat_bubble(
                c_area,
                "navi",
                f"❌ 自動対処エラー: {str(e)}"
            )
    
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
    
    # --------------------------------------------------------------------
    # ダッシュボード更新関数
    # --------------------------------------------------------------------
    def update_health_dashboard():
        """
        SystemHealthMonitorから最新データを取得してGUI更新
        """
        try:
            # ウィンドウが閉じられている場合は更新停止
            if not c_win.winfo_exists():
                return
            
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
            # エラー時も再スケジュール（10秒後）
            try:
                if c_win.winfo_exists():
                    c_win.after(10000, update_health_dashboard)
            except:
                pass  # ウィンドウが既に破棄されている場合
    
    # 初回更新トリガー（1秒後に開始）
    c_win.after(1000, update_health_dashboard)

else:
    # Phase 3モジュールが利用不可の場合
    print("⚠️ Phase 3 Health Panel無効（モジュール初期化失敗）")


# ============================================================================
# 実装手順書（README）
# ============================================================================
"""
【ローカルPCでの実装手順】

1. このファイルをローカルPCにダウンロード
   - ファイル: phase3_gui_integration_code.py
   - 場所: C:\Users\7716n\OneDrive\デスクトップ\naviko\navikoLAB\

2. naviko.pyのバックアップ作成
   - C:\Users\7716n\OneDrive\デスクトップ\naviko\naviko.py
   - バックアップ名: naviko_before_phase3c.py

3. 【セクション1】インポート文を追加
   - 場所: naviko.py 70行目付近（既存インポートの後）
   - コード: 24-35行目をコピー＆ペースト

4. 【セクション2】グローバル変数初期化を追加
   - 場所: naviko.py 8177行目付近（"root = tk.Tk()"の直前）
   - コード: 44-63行目をコピー＆ペースト

5. 【セクション3】health_panel追加
   - 場所: naviko.py 9552行目付近（top_menu.pack()の直後）
   - コード: 75-271行目をコピー＆ペースト

6. 構文チェック
   - PowerShellで実行: python naviko.py
   - エラーが出た場合は行番号を確認

7. Git同期
   - cd C:\Users\7716n\OneDrive\デスクトップ\naviko
   - git add naviko.py
   - git add navikoLAB/phase3_gui_integration_code.py
   - git commit -m "feat: Phase 3-C GUI統合完了（健全性ダッシュボード+自動対処）"
   - git push origin main

8. 動作テスト
   - naviko.pyを起動
   - チャットウィンドウを開く
   - health_panelが表示されることを確認
   - 健全性スコア、CPU、メモリが更新されることを確認
   - 「自動診断・対処」ボタンをクリックして動作確認

9. Workspace同期確認
   - Databricks WorkspaceでGit pullを実行
   - ファイルが反映されていることを確認

【トラブルシューティング】

Q1: インポートエラーが出る
A1: navikoLABディレクトリにPhase 3モジュールがあることを確認
    - system_health_monitor.py
    - naviko_system_controller.py

Q2: health_panelが表示されない
A2: コンソールに「⚠️ Phase 3 Health Panel無効」と表示されていないか確認
    モジュール初期化が失敗している可能性があります

Q3: ダッシュボードが更新されない
A3: コンソールに「❌ ダッシュボード更新エラー」が出ていないか確認
    SystemHealthMonitor.get_dashboard()の動作を確認

Q4: 自動対処ボタンが動作しない
A4: NavikoSystemController.run_safety_check()が正常に動作するか確認
    チャットエリアにエラーメッセージが表示されます
"""
