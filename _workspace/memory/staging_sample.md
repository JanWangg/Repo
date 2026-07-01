---
date: 2026-03-22
memory_type: long-term
topic: "KB 盤點 + 遷移策略（歷史快照）"
decision: archive_long_term
decision_reason: "已是歷史快照，內容已沉澱進實際架構"
linked_knowledge: ["/workspace/SOUL.md", "/workspace/docs/inventory_pre_2026-06-23.md"]
---

# Staging Sample — 遷移測試樣本
> 生成時間：2026-03-22

---

## 現有 KB 盤點結果

### 有內容的 KB（8個 → 全部保留）
| KB | 現有筆記 | 建議 Topic | 建議 Tags |
|----|---------|-----------|---------|
| 🤖 AI科技 | 138 | Reference | #ai, #technology |
| 📚 學習資料庫 | 103 | Reference | #learning, #education |
| 💼 商業管理 | 46 | Reference | #business, #management |
| 🌏 地緣政治 | 17 | Reference | #geopolitics |
| 📥 筆記資料庫 | 52 | Inbox | #inbox |
| 科学--医药卫生 | 123 | Reference | #health |
| 科学--教育 | 485 | Reference | #education |
| 文化--军事 | 86 | Reference | #culture, #history |

### 空 KB（12個 → 全部 archive）
- 📋 Aclis 開發日誌 / 🏥 健康與醫學 / 📥 收集箱（舊）
- 📰 晨報資料庫 × 4 / 💰 投資資料庫
- 📚 晨報·讀書 × 2（重複）

### 新建晨報 KB（4個 → 全部啟用）
| KB | Tags |
|----|------|
| 💰 晨報·投資（oJO54PgY） | #invest, #morning-report, #wisdom |
| 🤖 晨報·AI前沿科技（EJ9NO92n） | #ai, #morning-report, #wisdom |
| 💾 晨報·半導體（pn5rkG6Y） | #semiconductor, #morning-report, #wisdom |
| 📚 晨報·讀書（eYxvwLmJ） | #reading, #morning-report, #wisdom |

---

## 遷移策略（共識確認後執行）

### Phase 1：Tags 標註（不搬遷內容）
- 對 8個有內容 KB 的筆記補加 Tags
- 目標：每篇筆記 → Reference + [Domain Tags] + [Year] + [Status]

### Phase 2：空 KB Archive（純標記）
- 12個空 KB 改為 archive 狀態
- 標記：不再新增內容到此類 KB

### Phase 3：小批測試（Approve mapping 後執行）
- 從 🤖 AI科技(138) 取 20 筆記
- 測試：tags/add + batch-add
- 驗收標準：success_count ≥ 1

---

## 遷移後最終 Topic 結構
```
Inbox（收集箱）
  └─ 現有：📥 筆記資料庫（52）
  └─ Tags: #inbox

Reference（領域知識）
  ├─ 🤖 AI科技（138）→ Tags: #ai
  ├─ 📚 學習資料庫（103）→ Tags: #learning
  ├─ 💼 商業管理（46）→ Tags: #business
  ├─ 🌏 地緣政治（17）→ Tags: #geopolitics
  ├─ 科学--医药卫生（123）→ Tags: #health
  ├─ 科学--教育（485）→ Tags: #education
  └─ 文化--军事（86）→ Tags: #culture, #history

Archive（歷史歸檔）
  └─ 12個空 KB（純標記，不刪除）

晨報系統
  ├─ 💰 晨報·投資（oJO54PgY）
  ├─ 🤖 晨報·AI前沿科技（EJ9NO92n）
  ├─ 💾 晨報·半導體（pn5rkG6Y）
  └─ 📚 晨報·讀書（eYxvwLmJ）
```