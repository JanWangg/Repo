---
type: pending_tasks
created: 2026-07-01
last_review: 2026-07-01
staleness_threshold_days: 7
---

# TODO - L3 主動推進清單

> 這是 L3 等級的待辦。Aclis 自動追蹤，不需要 Jan 下命令。
> 規則：超過 7 天沒動 → 下次 session 自動 raise 給 Jan 看。
> 觸發機制：每次 session 啟動 → 讀本檔 → 檢查 staleness → 主動推進。

---

## 🔴 P0 - 阻塞中 / 必須先解

（目前無 P0）

---

## 🟡 P1 - 進行中

### T1. daily_notes/ 跟 memory/ 歸屬決策
- **建立日期：** 2026-06-22
- **最後動：** 2026-06-22
- **staleness:** 9 天 🔴
- **問題：**
  - `daily_notes/`（5 篇 sample + 3 個 scripts）放 vault 還是工作區？
  - `memory/2026-06-19.md`（昨日工作日誌）推 vault 還是本地存？
  - `/workspace` 4 個本地 commit（Aclis 工作區歷史）推哪個 repo？
- **需要決策：**
  - [ ] daily_notes → vault / 工作區 / 兩個都？
  - [ ] memory/ → 推 vault 還是只本地？
  - [ ] 工作區 commit → `JanWangg/hermes-agent-workspace` 新 repo 還是別處？
- [x] ~~給 Jan 3 個選項 + 我的建議，等他一句話決定~~
- [x] ~~Jan 決策：「知識統一」~~

---

### T2. /root/Documents/Jan-知識庫/ 併入 vault
- **建立日期：** 2026-06-22
- **最後動：** 2026-06-22
- **staleness:** 9 天 🔴
- **問題：** 兩個知識庫結構差異未確認，merge 策略未定
- **需要做的：**
  - [ ] 列出 `/root/Documents/Jan-知識庫/` 結構
  - [ ] 列出 vault 結構
  - [ ] diff 出衝突點
  - [ ] 決定 merge 策略（鏡像 / 雙向同步 / 分區存放）
- **下一步：** ~~跑一次 diff，產出報告~~（已整合進 vault 07_Jan-知識庫/）

---

### T3. Aclis 工作區 repo 規劃
- **建立日期：** 2026-06-22
- **最後動：** 2026-06-22
- **staleness:** 9 天 🔴
- **問題：** Aclis 工作區放哪個 repo？`JanWangg/hermes-agent-workspace` 還是別的？
- **候選方案：**
  - A. 新建 `JanWangg/hermes-agent-workspace` repo
  - B. 用現有 `JanWangg/Repo`（會跟 vault 混）
  - C. 用 `/workspace/.git` 維持本地，不推
- **下一步：** ~~給 Jan 3 個選項 + 利弊~~（已統一進 vault）

## 🟢 P2 - 排隊中

### T4. Push 失敗重試（網路恢復後）
- **建立日期：** 2026-07-01
- **最後動：** 2026-07-01
- **問題：** commit aad3783 push 失敗（403 → GnuTLS TLS error）
- **狀態：** 本地 commit 安全，遠端落後
- **下一步：** 等網路穩定後重試 push
- **保留：** 備份在 `/workspace/backup/before_unify_20260701_120752/`

---

## 📝 歷史（已完成 / 取消）

- ✅ 2026-06-22 GitHub 設定修正（token + repo URL）
- ✅ 2026-06-22 Vault 同步遠端
- ✅ 2026-06-22 600 篇 Get Notes 備份 + 30 個 tag 索引
- ✅ 2026-06-22 5 篇晨報 sample 提取
- ✅ 2026-07-01 建 TODO.md 機制（L3 防爛尾）
- ✅ 2026-07-01 建 SCHEDULE.md（L1/L2/L3 完整日程表）
- ✅ 2026-07-01 全量備份（6 個來源，80M）
- ✅ 2026-07-01 合併兩個 .git（單一 repo）
- ✅ 2026-07-01 整合 4 個來源進 vault（知識統一）
- ✅ 2026-07-01 更新 INDEX.md（v2.0 → v3.0）
- ✅ 2026-07-01 本地 commit aad3783
- ⏸️ 2026-07-01 Push 失敗（網路問題，網好重試）

---

## 🔧 機制說明

**為什麼這份檔存在：**
避免「明天繼續」變成「永遠不繼續」。每次 session 啟動：
1. 自動讀本檔
2. 檢查 staleness（最後動日期）
3. > 7 天 → raise 給 Jan
4. 有 P0 → 立刻處理
5. 有 P1 → 主動推進或 raise

**Jan 的角色：**
看 raise → 給決策 → 我執行。**不需要記得叫我。**