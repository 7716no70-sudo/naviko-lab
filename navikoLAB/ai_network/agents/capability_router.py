class CapabilityRouter:
    def route(self, purpose):
        text = str(purpose).lower()
        agents = ["planner"]

        if (
            "アプリ" in str(purpose)
            or "コード" in str(purpose)
            or "python" in text
            or "todo" in text
        ):
            agents.append("coder")
            agents.append("file")

        if "画像" in str(purpose) or "イラスト" in str(purpose):
            agents.append("image")

        if "動画" in str(purpose) or "youtube" in text:
            agents.append("video")

        if "調査" in str(purpose) or "調べ" in str(purpose) or "research" in text:
            agents.append("research")

        if "web" in text or "ブラウザ" in str(purpose):
            agents.append("browser")

        if "音声" in str(purpose) or "読み上げ" in str(purpose):
            agents.append("voice")

        if "pc操作" in text or "デスクトップ操作" in str(purpose):
            agents.append("desktop")

        return list(dict.fromkeys(agents))