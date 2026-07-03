---
name: token-usage-monitor
description: 監控 Get Notes API + LLM Token 耗用情況。自動記錄每次 API 呼叫，達到黃線（60%）提醒、紅線（80%）立刻中斷。觸發詞：「token 監控」、「配額查詢」、「API 用量」。
---

# Token Usage Monitor — API 配額監控

## 用途

主動追蹤 Get Notes API 的 token 耗用，避免超過配額警戒線（60% 黃、80% 紅）。

**Get Notes API 限制（依 SECURITY_SOP.md）：**
- 讀取：1,000/天
- 寫入：500/天
- 寫入筆記：50/天

## 工作流程

### Step 1：API 呼叫計數（本地追蹤）

由於 Get Notes API **沒有提供 quota 端點**，採用本地計數：

```python
import json
from datetime import datetime
import os

# 監控檔案
MONITOR_DIR = '/workspace/jan-vault/_workspace/monitoring'
os.makedirs(MONITOR_DIR, exist_ok=True)
USAGE_FILE = f"{MONITOR_DIR}/token_usage_{datetime.now().strftime('%Y%m%d')}.json"

def load_usage():
    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, 'r') as f:
            return json.load(f)
    return {
        "date": datetime.now().strftime('%Y-%m-%d'),
        "session_start": datetime.now().strftime('%H:%M'),
        "read_calls": 0,
        "write_calls": 0,
        "write_note_calls": 0,
        "calls_log": []
    }

def record_call(call_type, purpose=""):
    """每次 API 呼叫都記錄"""
    usage = load_usage()
    key = f"{call_type}_calls"
    if key not in usage:
        usage[key] = 0
    usage[key] += 1
    usage["calls_log"].append({
        "time": datetime.now().strftime('%H:%M:%S'),
        "type": call_type,
        "purpose": purpose
    })
    with open(USAGE_FILE, 'w') as f:
        json.dump(usage, f, ensure_ascii=False, indent=2)
    
    # 自動檢查警戒線
    check_thresholds(usage)
    return usage[key]

def check_thresholds(usage):
    read = usage.get('read_calls', 0)
    write = usage.get('write_calls', 0)
    write_note = usage.get('write_note_calls', 0)
    
    limits = {"read": 1000, "write": 500, "write_note": 50}
    used = {"read": read, "write": write, "write_note": write_note}
    
    for name, val in used.items():
        limit = limits[name]
        pct = val / limit * 100
        if pct >= 80:
            print(f"🔴 {name} 達紅線 {val}/{limit} ({pct:.1f}%)！立刻停止非必要呼叫")
            # 可加 raise 機制
        elif pct >= 60:
            print(f"🟡 {name} 達黃線 {val}/{limit} ({pct:.1f}%)，應減量")

def get_status():
    """回傳當前狀態"""
    usage = load_usage()
    read = usage.get('read_calls', 0)
    write = usage.get('write_calls', 0)
    write_note = usage.get('write_note_calls', 0)
    return {
        "read": f"{read}/1000 ({read/10:.1f}%)",
        "write": f"{write}/500 ({write/5:.1f}%)",
        "write_note": f"{write_note}/50 ({write_note/0.5:.1f}%)"
    }
```

### Step 2：包裝現有 API 呼叫

把所有 Get Notes API 呼叫改用 `record_call()` 包裝：

```python
# 之前
r = subprocess.run(['curl', '-s', ..., 'recall', ...])

# 之後
record_call('read', purpose='找今早 7/3 post')
r = subprocess.run(['curl', '-s', ..., 'recall', ...])
```

### Step 3：Heartbeat 自動報告

在 HEARTBEAT.md 加 token 監控點：

```markdown
## Token 監控
- [ ] 每日 09:00 / 13:00 / 17:00 檢查配額
- [ ] 黃線（60%）→ 記錄，不中斷
- [ ] 紅線（80%）→ 立刻告知 Jan
```

## 警戒線

| 配額 | 限制 | 黃線 (60%) | 紅線 (80%) | 行動 |
|------|------|----------|----------|------|
| 讀取 | 1,000/天 | 600 | 800 | 立刻停止非必要讀取 |
| 寫入 | 500/天 | 300 | 400 | 批次排程化 |
| 寫入筆記 | 50/天 | 30 | 40 | 合併寫入 |

## 已知限制

1. **本地計數 vs 後端計數可能不一致** — 後端可能有快取或批次計費
2. **沒有 quota 端點** — 無法即時校驗
3. **每次呼叫的「成本」不一** — recall top_k=1 vs top_k=50 不同

## 演化記錄

- **v1.0** (2026-07-03)：初版，從今日監控需求建立
