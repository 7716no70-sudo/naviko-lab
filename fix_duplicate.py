# ファイル読み込み
with open('naviko.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 重複箇所を検索して削除
new_lines = []
skip_next_comment_pass = False

for i, line in enumerate(lines):
    # LABカテゴリの最初のpassを見つけたら、次のコメント+passをスキップ
    if i > 0 and 'elif name == "LAB":' in lines[i-1] and '# LABカテゴリは現在' in lines[i] and not skip_next_comment_pass:
        new_lines.append(line)
        skip_next_comment_pass = True
    elif skip_next_comment_pass and ('# LABカテゴリは現在' in line or (line.strip() == 'pass' and i > 0 and '# LABカテゴリは現在' in lines[i-1])):
        # 重複をスキップ
        print(f'スキップ（行{i+1}）: {line.strip()}')
        if line.strip() == 'pass':
            skip_next_comment_pass = False
    else:
        new_lines.append(line)

# ファイル保存
with open('naviko.py', 'w', encoding='utf-8', newline='\n') as f:
    f.writelines(new_lines)

print(f'\n✅ 修正完了')
print(f'元の行数: {len(lines)}')
print(f'新しい行数: {len(new_lines)}')
print(f'削除: {len(lines) - len(new_lines)} 行')
