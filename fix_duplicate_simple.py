# ファイル読み込み
with open('naviko.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 連続する同一行を削除
new_lines = []
prev_line = None

for line in lines:
    # 前の行と全く同じ内容の行はスキップ
    if line == prev_line:
        print(f'重複削除: {line.strip()}')
        continue
    new_lines.append(line)
    prev_line = line

# ファイル保存
with open('naviko.py', 'w', encoding='utf-8', newline='\n') as f:
    f.writelines(new_lines)

print(f'\n✅ 修正完了')
print(f'元の行数: {len(lines)}')
print(f'新しい行数: {len(new_lines)}')
print(f'削除: {len(lines) - len(new_lines)} 行')
