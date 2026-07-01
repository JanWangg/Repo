import json, os
from collections import Counter

d = json.load(open('/workspace/backup/getnotes_backfill_2026-05-15-16.json'))
notes = d['notes']

raw_dir = '/workspace/obsidian/raw/2026-06-19'
acls_dir = '/workspace/obsidian/raw/2026-06-19/_priority_acls'
os.makedirs(acls_dir, exist_ok=True)

acls_count = 0
total_written = 0

for n in notes:
    note_id = n.get('note_id','')
    title = n.get('title','')
    content = n.get('content','')
    tags = n.get('tags') or []
    tag_names = [t.get('name','') if isinstance(t,dict) else str(t) for t in tags]
    created = n.get('created_at','')

    safe_title = title.replace('/', '-').replace(':', '-').replace(' ', '_')[:50]
    date_short = created[:10] if created else 'unknown'
    fname = f"{date_short}_{note_id[:8]}_{safe_title}.md"

    is_acls = 'aclis' in tag_names or 'acls' in tag_names
    target_dir = acls_dir if is_acls else raw_dir
    fpath = os.path.join(target_dir, fname)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("note_id: " + note_id + "\n")
        f.write("created: " + created + "\n")
        f.write("source: " + str(n.get('source','')) + "\n")
        f.write("note_type: " + str(n.get('note_type','')) + "\n")
        f.write("tags: [" + ', '.join(tag_names) + "]\n")
        f.write("is_priority_acls: " + str(is_acls) + "\n")
        f.write("---\n\n")
        f.write("# " + title + "\n\n")
        f.write(content)
        if n.get('ref_content'):
            f.write("\n\n## 引用內容\n\n")
            f.write(n['ref_content'])

    total_written += 1
    if is_acls:
        acls_count += 1

print("=== Mirror 完成 ===")
print("總計: " + str(total_written) + "/600 篇已寫入")
print("  /workspace/obsidian/raw/2026-06-19/ : " + str(total_written - acls_count) + " 篇")
print("  /workspace/obsidian/raw/2026-06-19/_priority_acls/ : " + str(acls_count) + " 篇")

# tag 統計
all_tags = []
for n in notes:
    tags = n.get('tags') or []
    for t in tags:
        if isinstance(t, dict):
            all_tags.append(t.get('name',''))
        else:
            all_tags.append(str(t))

tc = Counter(all_tags)
print("\n=== Tag 總覽: " + str(len(tc)) + " 個 unique, " + str(sum(tc.values())) + " 總標記 ===")
print("Top 20 tags:")
for t,c in tc.most_common(20):
    print("  [" + str(c) + "] " + t)