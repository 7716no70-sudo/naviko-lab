# Naviko LAB 開発者ガイド v1.4.0

## 設計思想

### 最終目的
製作者がPC上で行える作業は、製作者が許可すればナビ子にもできる

### 3層アーキテクチャ
意思決定層（未実装）
  ↓
能力選択層（未実装）
  ↓
実行層（完成）

---

## モジュール構造

| モジュール | 能力 | 行数 |
|----------|------|------|
| UniversalLLMConnector | マルチLLM統合 | 248 |
| EnhancedLLMCache | 高性能キャッシュ | 428 |
| DeepSearchEngine | ディープサーチ | 410 |
| AppProjectBuilder | アプリ生成 | 557 |
| ImprovementManager | コード改善 | 452 |

---

## 開発環境

### セットアップ
pip install -r requirements.txt
ollama pull codellama:7b
ollama serve

### 新しい能力の追加
from navikoLAB.universal_llm_connector import UniversalLLMConnector

class NewCapability:
    def __init__(self, lab_dir, llm_connector):
        self.lab_dir = lab_dir
        self.llm = llm_connector
    
    def execute(self, input_data):
        # 実装
        pass

---

## Phase 6以降

### Phase 6: 能力選択層
ユーザーの意図から能力を自動選択

### Phase 7: 統合層
複数能力の連携実行

### Phase 8: 意思決定層
深い意図理解と最適計画生成

---

バージョン: v1.4.0
設計思想: 自分で考えて成長するAI
