# Python Script File Editing - 成功例

**作成日**: 2026-07-08
**問題**: editAssetでのホワイトスペース敏感性により編集失敗
**解決法**: Pythonスクリプトによる直接ファイル操作

---

## 成功したケース: naviko.py 95-96行削除

### 問題の詳細
- 対象: `/Workspace/Users/7716no70@gmail.com/naviko-lab/naviko.py`
- 削除対象: 95-96行目（重複した import end コメントと空行）
- 失敗した方法: editAsset（複数回試行）

### 編集前の状態
```
94:     SelfGrowthEngine = None
95: # === Brain Layer import end ===
96: 
97: # === Brain Layer import ===
98: try:
```

### 編集後の状態
```
94:     SelfGrowthEngine = None
95: # === Brain Layer import ===
96: try:
```

---

## 成功したPythonコード

```python
import os

# ファイルパス
file_path = "/Workspace/Users/7716no70@gmail.com/naviko-lab/naviko.py"

# ファイルを読み込む
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 削除前の確認（オプション）
print(f"元の総行数: {len(lines)}")
for i in range(89, min(100, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')

# 95-96行目を削除（0-indexedなので94-95）
del lines[94:96]

# 削除後の確認（オプション）
print(f"\n削除後の総行数: {len(lines)}")
for i in range(89, min(100, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')

# ファイルに書き戻す
with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\n✅ 編集完了")
```

---

## 手順の要点

### 1. ファイル読み込み
```python
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
```
- `readlines()` で全行をリストとして取得
- UTF-8エンコーディング指定

### 2. 行削除
```python
del lines[94:96]  # 95-96行目 (0-indexed)
```
- Pythonのリストは0-indexed
- 95-96行目 = インデックス94-95
- スライス `[94:96]` で該当行を削除

### 3. ファイル書き込み
```python
with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
```
- `writelines()` でリストを一括書き込み
- 元のファイルを上書き

---

## 他の操作パターン

### 特定行の置換
```python
lines[94] = "# 新しい内容\n"
```

### 特定行の挿入
```python
lines.insert(94, "# 挿入する行\n")
```

### 複数箇所の編集
```python
# 94行目を削除、100行目に挿入
del lines[94]
lines.insert(100, "# 新しい行\n")
```

---

## 注意事項

1. **バックアップ不要**: Gitで管理されているため、失敗しても復元可能
2. **行番号の確認**: readAssetByIdで事前確認推奨
3. **0-indexed**: Pythonリストは0から開始（表示上の95行目 = インデックス94）
4. **改行保持**: `readlines()` は改行文字を保持するため、そのまま書き戻せる

---

## 使用タイミング

### Pythonスクリプトを使うべき時
- ✅ editAssetが複数回失敗
- ✅ ホワイトスペースが敏感な編集
- ✅ 複数行の一括削除・挿入
- ✅ 行番号ベースの正確な編集

### editAssetを使うべき時
- ✅ 通常のコード変更
- ✅ テキストベースの置換
- ✅ 複数箇所の同時編集

---

**記録者**: Genie Code
**検証済み**: ✅ 2026-07-08
