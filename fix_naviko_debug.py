import re
import sys

print('=' * 60)
print('📊 Naviko.py GUIボタン削除スクリプト（デバッグ強化版）')
print('=' * 60)
print()

# ファイル読み込み
print('Step 1: ファイル読み込み中...')
try:
    with open('naviko.py', 'r', encoding='utf-8') as f:
        content = f.read()
    print(f'✅ 読み込み成功: {len(content):,} bytes')
except Exception as e:
    print(f'❌ 読み込みエラー: {e}')
    sys.exit(1)

print()

# 元のコンテンツをバックアップ
original_content = content

# LABカテゴリの検索
print('Step 2: LABカテゴリボタン検索中...')
lab_pattern = r'        elif name == \"LAB\":'
if re.search(lab_pattern, content):
    print('✅ LABカテゴリ発見')
    # 該当箇所を表示（デバッグ用）
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'elif name == \"LAB\":' in line:
            print(f'  行{i+1}: {line}')
            for j in range(1, 8):
                if i+j < len(lines):
                    print(f'  行{i+j+1}: {lines[i+j][:80]}...')
            break
else:
    print('❌ LABカテゴリが見つかりません')

print()

# LABカテゴリのボタンを削除
print('Step 3: LABカテゴリボタン削除中...')
# より単純なパターンで行単位削除
lines = content.split('\n')
new_lines = []
skip_mode = False
skip_count = 0

for i, line in enumerate(lines):
    if 'elif name == \"LAB\":' in line and not skip_mode:
        # LABカテゴリ開始
        new_lines.append(line)
        new_lines.append('            # LABカテゴリは現在Phase 3システムで管理されています')
        new_lines.append('            pass')
        skip_mode = True
        skip_count = 0
        print(f'  ✅ LABカテゴリ発見（行{i+1}）、7行のボタンをスキップします')
    elif skip_mode and skip_count < 7:
        # 7行のボタンをスキップ
        if 'add_menu_button' in line:
            skip_count += 1
            print(f'    スキップ: {line.strip()[:60]}...')
        else:
            # add_menu_buttonでない行が来たらスキップモード終了
            skip_mode = False
            new_lines.append(line)
    else:
        skip_mode = False
        new_lines.append(line)

content = '\n'.join(new_lines)
print(f'✅ LABカテゴリ処理完了（{skip_count}行スキップ）')

print()

# Dashboard v1.2ボタンの削除
print('Step 4: Dashboard v1.2ボタン削除中...')
v12_count = 0
lines = content.split('\n')
new_lines = []

for line in lines:
    if 'add_menu_button(body, \"v1.2' in line:
        v12_count += 1
        print(f'  スキップ: {line.strip()[:60]}...')
    else:
        new_lines.append(line)

content = '\n'.join(new_lines)
print(f'✅ v1.2ボタン削除完了（{v12_count}行削除）')

print()

# 変更確認
print('Step 5: 変更サイズ確認...')
original_size = len(original_content)
new_size = len(content)
diff = original_size - new_size
print(f'  元のサイズ: {original_size:,} bytes')
print(f'  新しいサイズ: {new_size:,} bytes')
print(f'  削減: {diff:,} bytes')

if diff == 0:
    print('⚠️  警告: サイズが変更されていません。パターンマッチに失敗している可能性があります。')
    print()
    print('デバッグ情報: LABカテゴリ付近の内容を表示します')
    for i, line in enumerate(content.split('\n')):
        if 'elif name == \"LAB\":' in line:
            print(f'行{i+1}: {line}')
            for j in range(1, 10):
                if i+j < len(content.split('\n')):
                    print(f'行{i+j+1}: {content.split(chr(10))[i+j]}')
            break
    sys.exit(1)

print()

# ファイル保存
print('Step 6: ファイル保存中...')
try:
    with open('naviko.py', 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
        f.flush()
    print('✅ ファイル書き込み成功')
except Exception as e:
    print(f'❌ ファイル書き込みエラー: {e}')
    sys.exit(1)

print()

# 最終確認
import os
final_size = os.path.getsize('naviko.py')
print('=' * 60)
print('✅ 処理完了')
print('=' * 60)
print(f'最終ファイルサイズ: {final_size:,} bytes')
print(f'行数: {len(content.split(chr(10))):,} 行')
print()
