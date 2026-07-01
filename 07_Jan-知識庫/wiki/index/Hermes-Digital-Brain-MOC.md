---
title: Hermes Digital Brain v1.0 — 主入口
tags:
  - MOC
  - Hermes核心
  - 系統地圖
type: index
created: 2026-06-22
updated: 2026-06-22
version: 1.0
status: active
---

# Hermes Digital Brain v1.0 🧠

> **最終目標不是讓 Hermes 記住更多文件，而是讓它逐步形成：**
> **「我如何思考、如何學習、如何做決策」的個人作業系統（Personal Operating System）。**

## 主軸：**記憶 → 知識 → 思考 → 洞察 → 決策**

---

## 🏛️ 七層架構全景

```
              ┌─────────────┐
              │   使用者    │  ← Jan（守護者）
              └──────┬──────┘
                     │
              ┌──────▼──────┐
              │  對話與推理 │  ← LLM（模型無關）
              └──────┬──────┘
                     │
   ┌─────────────────┼─────────────────┐
   │                 │                 │
   ▼                 ▼                 ▼
┌────────┐      ┌────────┐        ┌────────┐
│ 記憶宮殿│      │ 知識管理│        │ 系統思維│
│ 第1層  │      │ 第2層  │        │ 第4層  │
└───┬────┘      └───┬────┘        └───┬────┘
    │               │                 │
    └───────────────┼─────────────────┘
                    │
             ┌──────▼──────┐
             │  洞察生成   │  ← 第 5 層
             └──────┬──────┘
                    │
             ┌──────▼──────┐
             │  決策日誌   │  ← 第 6 層
             └──────┬──────┘
                    │
             ┌──────▼──────┐
             │ 個人智慧   │  ← 最終資產
             └─────────────┘
```

---

## 🏛️ 第一層：記憶宮殿（Memory Palace）

> 5→6 座宮殿，每座宮殿獨立目錄

| # | 宮殿 | 內容 | 入口 |
|---|------|------|------|
| 01 | **Identity** | 人生原則、價值觀、信念、長期目標 | [[01-Identity-Palette]] |
| 02 | **Learning** | 書籍、課程、文章、研究 | [[02-Learning-Palette]] |
| 03 | **Experience** | 經驗、案例、失敗、成功 | [[03-Experience-Palette]] |
| 04 | **Decisions** | 重大決策、原因、結果 | [[04-Decisions-Palette]] |
| 05 | **Insights** | 心得、洞察、觀察 | [[05-Insights-Palette]] |
| 06 | **People** | 人物誌（黃仁勳、Sam Altman 等）| [[06-People-Palette]] |

---

## 📚 第二層：知識管理系統（Knowledge Domains）

> 13 大領域分類

**核心（7）：** AI / Technology / Finance / People / History / Philosophy / Methodology
**延伸（6）：** Science / Psychology / Health / Productivity / Life / Events / Geography

→ 完整索引：[[MOC-Knowledge-Domains]]

---

## 🧠 第三層：心智模型庫（Mental Models）

> 12+ 模型，按功能分三群

**決策群：** 第一性原理、機會成本、逆向思考、期望值、貝氏思維
**系統群：** 系統思維、PDCA、OODA、TOC、複利
**風險群：** 反脆弱、風險矩陣、黑天鵝、安全邊際

→ 完整索引：[[MOC-Mental-Models]]

---

## ⚙️ 第四層：系統思維引擎（Systems Engine）

> 6 步推理流：**E → P → S → M → L → A**

```
Event（事件）→ Pattern（模式）→ Structure（結構）
       → Mental Model（心智模式）→ Leverage Point（槓桿點）→ Action（行動）
```

→ 框架詳解：[[Systems-Thinking-Engine]]

---

## 💡 第五層：洞察生成系統（Insight Engine）

> 把知識變智慧

**格式：** 觀察 → 發現 → 關聯 → 啟發 → 下一步

→ 模板與範例：[[Insight-Template]] | [[MOC-Insights]]

---

## 📔 第六層：決策日誌系統（Decision Journal）

> 8 欄位標準格式

**格式：** 日期 / 問題 / 可選方案 / 選擇 / 理由 / 預期結果 / 實際結果 / 學到什麼

**核心信念：** `智慧 = 決策品質`

→ 模板與範例：[[Decision-Template]] | [[MOC-Decisions]]

---

## 🤖 第七層：Hermes AI Agent 群

> 工具層（不是 Wiki 內容）

| Agent | 職責 |
|-------|------|
| **Librarian** | 整理知識、建立索引 |
| **Research** | 整理資料、生成摘要 |
| **Systems** | E→P→S→M→L→A 分析 |
| **Insight** | 產生洞察、建立連結 |
| **Mentor** | 提出問題、挑戰思維 |

---

## 🔄 數據飛輪（Get Notes ↔ Wiki）

```
10,879 篇 Get Notes 素材
        ↓ Tag 化（5 維）
   _raw_getnotes/
        ↓ 蒸餾
   Wiki/Topics/ → Wiki/Entities/ → Wiki/Synthesis/
        ↓ 雙向連結
   Obsidian Graph View
        ↓ 跨 Session 召回
   充實記憶宮殿 + 決策日誌
        ↓
   個人智慧 = 判斷品質提升
```

---

## 📂 知識庫結構（與 Get Notes 對接）

**保留 11 個 KB：**
- 📕 5 個得到 KB（文化-經濟 / 文化-信息 / 文化-社會 / 科學-教育 / 科學-醫藥）
- 🤖 4 個核心 KB（AI科技 / 學習資料庫 / llm-wiki / 晨報-投資）
- 📰 4 個晨報 KB（半導體 / AI前沿 / 讀書 / 投資）
- 🗄️ 4 個空 KB（保留預留）

**KB ↔ 宮殿對應：**
- 學習宮 ← AI科技 / 學習資料庫 / 讀書晨報
- 經驗宮 ← 投資晨報 / 半導體晨報 / AI前沿晨報
- 知識領域 ← 5 個得到 KB

---

## 📌 核心原則

> **「真正有價值的資產仍是您的記憶宮殿、知識關聯網與決策歷史，而不是模型本身。」**

- ✅ 模型無關（Qwen / Hermes / Llama / Mistral 都行）
- ✅ 標準 Markdown（Obsidian 開啟）
- ✅ 雙向連結（Graph View 可視化）
- ✅ Tag 索引（5 維檢索）
- ✅ 蒸餾飛輪（對話 → 事實 → 判斷）

---

## 🗺️ 導航索引

| MOC | 用途 |
|-----|------|
| [[MOC-Hermes-Digital-Brain]] | ← 你在此頁 |
| [[MOC-Memory-Palace]] | 6 座宮殿總覽 |
| [[MOC-Knowledge-Domains]] | 13 大領域索引 |
| [[MOC-Mental-Models]] | 心智模型庫 |
| [[MOC-Insights]] | 洞察集合 |
| [[MOC-Decisions]] | 決策日誌 |
| [[MOC-GetNotes-Tag地圖]] | 5 維 Tag 規範 |

---

**建立日期：** 2026-06-22
**架構版本：** v1.0
**設計者：** Aclis（大 A）+ Jan 共同架構