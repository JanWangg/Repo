import json, os

d = json.load(open('/workspace/backup/getnotes_backfill_2026-05-15-16.json'))
notes = d['notes']

targets = {
    'AI_qianyan': 'AI 前沿科技晨報',
    'Bandaoti': '半導體晨報',
    'Touzi': '投資晨報',
    'Yiliao': '醫療健康晨報',
    'Dushu': '讀書晨報'
}

found = {}
for n in notes:
    t = n.get('title','')
    for label, kw in targets.items():
        if label in found:
            continue
        if kw in t and '2026-06-19' in t:
            found[label] = n

for label in targets:
    if label not in found:
        for n in notes:
            t = n.get('title','')
            if targets[label] in t:
                found[label] = n
                break

out_dir = '/workspace/daily_notes/morning_samples'
os.makedirs(out_dir, exist_ok=True)
for label, n in found.items():
    date_str = (n.get('created_at') or 'unknown')[:10]
    fname = f"{out_dir}/{label}_{date_str}.md"
    tags = n.get('tags') or []
    tag_str = ', '.join(t.get('name','') if isinstance(t,dict) else str(t) for t in tags)
    content = n.get('content','')
    with open(fname, 'w', encoding='utf-8') as f:
        f.write("# " + str(n.get('title','')) + "\n\n")
        f.write("**note_id:** " + str(n.get('note_id')) + "\n")
        f.write("**created:** " + str(n.get('created_at')) + "\n")
        f.write("**tags:** " + tag_str + "\n")
        f.write("**source:** " + str(n.get('source')) + "\n")
        f.write("**content_len:** " + str(len(content)) + " chars\n\n")
        f.write("---\n\n## 內容\n\n")
        f.write(content)
    print(f"  [OK] {label}: {fname} ({len(content)} chars)")

print("\n總計 " + str(len(found)) + "/5 篇已寫入 " + out_dir)