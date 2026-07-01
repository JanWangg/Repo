import json, os
from collections import Counter, defaultdict

d = json.load(open('/workspace/backup/getnotes_backfill_2026-05-15-16.json'))
notes = d['notes']

# 反查：tag → notes
tag_to_notes = defaultdict(list)
for n in notes:
    tags = n.get('tags') or []
    for t in tags:
        name = t.get('name','') if isinstance(t,dict) else str(t)
        tag_to_notes[name].append(n)

# 索引目錄
idx_dir = '/workspace/obsidian/raw/2026-06-19/_index'
os.makedirs(idx_dir, exist_ok=True)

# === A: 總覽頁 ===
with open(idx_dir + '/_README.md', 'w', encoding='utf-8') as f:
    f.write("# 2026-06-19 Get Notes 備份總覽\n\n")
    f.write("> 600 篇備份原始素材 · 抓取時間 2026-06-19 18:34\n")
    f.write("> 原始檔：`/workspace/backup/getnotes_backfill_2026-05-15-16.json` (4.0MB)\n\n")
    f.write("## 統計\n")
    f.write("- 總計：**600 篇**\n")
    f.write("- 已鏡像至 obsidian/raw/2026-06-19/：550 篇\n")
    f.write("- 優先目錄 _priority_acls/：**50 篇**（你親自標記 aclis 的）\n")
    f.write("- Unique tags：**155 個**\n\n")
    f.write("## 按來源分布\n")
    src_count = Counter(n.get('source','?') for n in notes)
    for s,c in src_count.most_common():
        f.write("- " + s + ": " + str(c) + " 篇\n")
    f.write("\n## 按類型分布\n")
    nt = Counter(n.get('note_type','?') for n in notes)
    for t,c in nt.most_common():
        f.write("- " + t + ": " + str(c) + " 篇\n")

print("[OK] _README.md")

# === B: 各 tag 的索引頁 ===
# 只處理有 ≥3 篇的 tag
top_tags = [(t,c) for t,c in Counter(t for notes_tags in [n.get('tags') or [] for n in notes] for t in ([tt.get('name','') if isinstance(tt,dict) else str(tt) for tt in notes_tags])).most_common() if c >= 3]
print(f"Top tags (≥3 篇): {len(top_tags)} 個")

# 直接做 for top 30 tags
for tag, count in top_tags[:30]:
    safe_tag = tag.replace('/', '-').replace(' ', '_').replace('·','_')
    fpath = idx_dir + '/tag_' + safe_tag + '.md'
    tag_notes = tag_to_notes[tag]
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write("# Tag: " + tag + "\n\n")
        f.write("> 共 " + str(count) + " 篇 · 標籤 " + tag + "\n\n")
        f.write("## 列表\n\n")
        # 按日期排序
        sorted_notes = sorted(tag_notes, key=lambda x: x.get('created_at',''), reverse=True)
        for n in sorted_notes[:30]:
            title = n.get('title','(無標題)')
            created = (n.get('created_at','') or '')[:10]
            note_id = n.get('note_id','')
            short_id = note_id[:8] if note_id else ''
            safe_title = title.replace('/', '-').replace(':', '-').replace(' ','_')[:50]
            src = n.get('source','')
            # 連結到實際 obsidian 檔案
            link_name = created + '_' + short_id + '_' + safe_title + '.md'
            is_acls = 'aclis' in [t.get('name','') if isinstance(t,dict) else str(t) for t in (n.get('tags') or [])]
            f.write("- " + created + " | [" + title[:50] + "](../" + link_name + ") | " + src + (" ⭐**acls**" if is_acls else "") + "\n")

print(f"[OK] tag 索引頁面: {min(30, len(top_tags))} 個")