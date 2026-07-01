# navikoLAB/decision_engine.py


class DecisionEngine:
    def decide(self, user_text):
        text = user_text.strip()

        if not text:
            return {
                "intent": "empty",
                "risk": "low",
                "action": "ignore",
                "reason": "入力が空です",
            }

        # 計画・実装要求は、記憶や成長という単語より優先する
        if any(word in text for word in ["実装", "作る", "進めて", "設計", "計画", "強化"]):
            return {
                "intent": "plan_request",
                "risk": "low",
                "action": "respond",
                "reason": "作業・実装・計画に関する入力です",
            }

        if any(word in text for word in ["さっき", "前に", "覚えて", "記憶"]):
            return {
                "intent": "memory_check",
                "risk": "low",
                "action": "respond",
                "reason": "記憶確認の入力です",
            }

        if any(word in text for word in ["成長", "AI OS", "次に何", "自己成長"]):
            return {
                "intent": "growth_check",
                "risk": "low",
                "action": "respond",
                "reason": "成長状態確認の入力です",
            }

        if any(word in text for word in ["PC操作", "ネット投稿", "金融解析", "画像生成", "動画生成", "音声生成"]):
            return {
                "intent": "unsafe_or_future",
                "risk": "medium",
                "action": "defer",
                "reason": "現在の優先範囲外または安全確認が必要な機能です",
            }

        return {
            "intent": "chat",
            "risk": "low",
            "action": "respond",
            "reason": "通常会話です",
        }