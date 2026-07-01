class AbstractionEngine:

    def __init__(self):
        self.memory = []

    def abstract(self, data):
        """
        データを簡易的に抽象化する（軽量版）
        """

        self.memory.append(data)

        # 単純な特徴抽出
        if isinstance(data, dict):
            keys = list(data.keys())
        else:
            keys = str(data)[:30]

        return {
            "abstracted": True,
            "features": keys,
            "size": len(self.memory)
        }