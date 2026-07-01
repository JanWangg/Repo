---
title: 記憶宮殿總覽
tags:
  - MOC
  - 記憶宮殿
  - 系統架構
type: index
created: 2026-06-22
updated: 2026-06-22
version: 1.0
---

# 記憶宮殿總覽 🏛️

> 靈感來自「記憶宮殿」(Method of Loci)，但從地點記憶轉為**主題型索引系統**
> 每座宮殿是 Jan 內在某個面向的「永久知識錨點」

## 為什麼是 6 座？

- **5 座**源自原始設計：Identity / Learning / Experience / Decisions / Insights
- **+1 座「人物」**：因 Hermes 的獨特價值在於對人類智慧的詮釋（如黃仁勳、Sam Altman、Karpathy 的思考框架）

---

## 🏛️ 6 座宮殿索引

| # | 宮殿 | 核心問題 | 主入口 |
|---|------|---------|--------|
| 01 | **Identity** | 我是誰？我相信什麼？ | [[01-Identity-Palette]] |
| 02 | **Learning** | 我學了什麼？如何學習？ | [[02-Learning-Palette]] |
| 03 | **Experience** | 我經歷了什麼？有何教訓？ | [[03-Experience-Palette]] |
| 04 | **Decisions** | 我做了什麼決定？結果如何？ | [[04-Decisions-Palette]] |
| 05 | **Insights** | 我洞察了什麼？ | [[05-Insights-Palette]] |
| 06 | **People** | 我景仰誰？想成為誰？ | [[06-People-Palette]] |

---

## 📂 宮殿存放規則

```
wiki/entities/memory-palace/
├── 01-Identity-Palette.md
├── 02-Learning-Palette.md
├── 03-Experience-Palette.md
├── 04-Decisions-Palette.md
├── 05-Insights-Palette.md
└── 06-People-Palette.md
```

每個 Palette 頁面包含：
1. 宮殿說明（核心問題、為何存在）
2. 內容卡片（具體筆記入口）
3. 跨宮殿連結（雙向連結圖譜）
4. Tag 索引（5 維分類）

---

## 🔄 宮殿間的流動

```
    ┌──────────┐
    │ Identity │ ← 信念源頭
    └─────┬────┘
          │ 指導
          ▼
    ┌──────────┐
    │ Learning │ ← 知識輸入
    └─────┬────┘
          │ 實踐
          ▼
    ┌──────────┐
    │Experience│ ← 經驗積累
    └─────┬────┘
          │ 萃取
          ▼
    ┌──────────┐
    │ Insights │ ← 模式提煉
    └─────┬────┘
          │ 行動
          ▼
    ┌──────────┐
    │Decisions │ ← 行動決策
    └─────┬────┘
          │ 累積
          └─────► 回到 Identity
```

---

## 🎯 跨宮殿檢索路徑

| 場景 | 起點 | 路徑 |
|------|------|------|
| 想確認某個價值觀 | 問題 → | Identity → 相關 Decisions |
| 想學習新領域 | 問題 → | Learning → 相關 Mental Models |
| 想複盤失敗 | 問題 → | Experience → Insights → Decisions |
| 想理解某人物 | 人物 → | People → 相關 Insights |
| 想驗證決策 | 問題 → | Decisions → 結果 → Insights |

---

## 📌 設計原則

- ✅ **宮殿是「容器」，不是「分類」** — 每座宮殿有自己的內在邏輯
- ✅ **雙向連結優先** — 同一件事可屬於多個宮殿（如「失戀」是 Experience 也是 Insights）
- ✅ **入口頁 vs 卡片** — Palette 是索引，具體卡片存在 `/cards/` 子目錄
- ✅ **時間軸並列** — 每座宮殿都有時間軸視角（過去/現在/未來）

---

**設計日期：** 2026-06-22
**架構版本：** v1.0
**協作：** Aclis + Jan