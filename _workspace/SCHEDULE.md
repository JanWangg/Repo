---
type: execution_schedule
created: 2026-07-01
last_review: 2026-07-01
hermes_version: v0.9.0
---

# SCHEDULE - Aclis 三層執行日程表

> L1 / L2 / L3 三層架構 + 完整日程。不需要 Jan 下命令也能運作。

---

## 🔵 L1 - 被動響應（即時）

**觸發：** Jan 說話 / 提問 / 下命令
**動作：** 回應
**日程：** 隨時
**靜音規則：** 無（Jan 開口就回）

**負責項目：**
- 問答
- 任務執行
- 知識查詢
- 任何 Jan 直接說要做的事

---

## 🟢 L2 - 主動巡查（Heartbeat 週期）

**觸發：** 定時（heartbeat 週期）+ Jan 沒說話時
**動作：** 背景巡查 + 必要時打擾
**日程：** 見下方排程

### 巡查頻率

| 時段 | 頻率 | 說明 |
|------|------|------|
| 08:00 - 23:00 | 每 2 小時 | 主動巡查 |
| 23:00 - 08:00 | 每 4 小時（且不打擾） | 背景掃，不通知 |

### 巡查項目（輪替）

**每日必掃：**
- [ ] Get Notes 新筆記 → 觸發 daily-knowledge-ingestion
- [ ] GitHub repo 同步狀態
- [ ] TODO.md staleness 檢查

**每週掃：**
- [ ] /root/Documents/Jan-知識庫/ 健康度
- [ ] Obsidian vault 完整性
- [ ] llm-wiki 雙向連結檢查

**每月掃：**
- [ ] 知識庫合併狀態
- [ ] 工作區 commit 清理
- [ ] API token 過期檢查

### 打擾規則（何時通知 Jan）

**立刻打擾：**
- 緊急安全事件（P0）
- TODO 爛尾 > 7 天
- 同步失敗 / token 過期
- Jan 主動設的提醒時間到

**不打擾（靜默記錄）：**
- 例行巡查無新發現
- 時段在 23:00 - 08:00
- 只是更新內部狀態

---

## 🟡 L3 - 主動推進（TODO 驅動）

**觸發：** TODO.md 有待辦
**動作：** 自動執行 / raise 給 Jan
**日程：** 持續 + 每次 session 啟動時檢查

### 推進優先級

| 優先 | 條件 | 動作 |
|------|------|------|
| P0 | 阻塞中 | 立刻處理 + 通知 |
| P1 | 進行中 | 主動推進，若卡決策 → raise 給 Jan |
| P2 | 排隊中 | 等 P1 清完才動 |

### 爛尾檢測

```
if (today - todo.last_review > 7 days):
    raise_to_jan(todo)
    status = "stale"
```

### Session 啟動流程（自動）

每次 Aclis 醒來：
1. 讀 SOUL.md / USER.md（必讀）
2. 讀 MEMORY.md（主 session 才讀）
3. **讀 TODO.md** ← 新增
4. **讀 SCHEDULE.md** ← 新增
5. 檢查 staleness → 有 raise 的就 raise
6. 檢查 L2 巡查 → 有新發現就主動告知
7. 檢查 L1 → 等 Jan 開口

---

## 🚨 緊急通道

**Jan 可以隨時用：**
- 「緊急」/ 「立刻」/ 「現在」 → 跳過所有排程，立刻響應
- 「靜音」/ 「別吵」 → L2 暫停 N 小時
- 「繼續 T1」 → 直接執行 TODO 裡的 T1

---

## 📊 當前狀態（2026-07-01）

| 層 | 狀態 | 下一個動作 |
|----|------|-----------|
| L1 | 🟢 待命 | 等 Jan 開口 |
| L2 | 🟢 待命 | 下次 heartbeat 啟動 |
| L3 | 🔴 有 3 個 stale 待辦 | raise 給 Jan |

---

## 🔗 相關檔案

- `TODO.md` — L3 待辦清單
- `SOUL.md` — 進化基因 + 心法
- `MEMORY.md` — 長程記憶（主 session）
- `USER.md` — Jan 個人資料
- `AGENTS.md` — 工作區規範
- `HEARTBEAT.md` — 心跳設定

---

## 🛠️ 待辦：技術補丁

（這些是給 Aclis 自己跑、不需要 Jan 同意的）

- [ ] 把 session 啟動讀 TODO 寫進 boot 流程（patch AGENTS.md）
- [ ] heartbeat hook 加 staleness 檢查
- [ ] 在 `~/.hermes/` 建 TODO 軟連結，跨 workspace 共享