---
title: 5 維 Tag 規範 + Obsidian 連結規則
tags:
  - MOC
  - Tag
  - 連結規則
type: index
created: 2026-06-22
version: 1.0
---

# 5 維 Tag 規範 + Obsidian 連結規則 🏷️

> Tag 是**機器的語言**，連結是**人類的語言**
> 兩者並用，Wiki 才能被 AI 和人都高效運用

---

## 🏷️ 5 維 Tag 系統

### 第 1 維：宮殿（必填）
```
#宮殿/Identity       → 身份、價值觀
#宮殿/Learning       → 學習、知識
#宮殿/Experience     → 經驗、案例
#宮殿/Decisions      → 決策日誌
#宮殿/Insights       → 洞察、心得
#宮殿/People         → 人物誌
```

### 第 2 維：領域（必填）
```
#AI                  → 人工智慧
#Technology          → 半導體、SaaS
#Finance             → 投資、經濟
#People              → 人物
#History             → 歷史
#Philosophy          → 哲學、佛學
#Methodology         → 方法論
#Science             → 自然科學
#Psychology          → 心理學
#Health              → 健康
#Productivity        → 生產力
#Life                → 生活
#Events              → 事件
#Geography           → 地理、地緣
```

### 第 3 維：心智模型（選填）
```
#心智模型/決策群     → 第一性原理、期望值
#心智模型/系統群     → 系統思維、PDCA
#心智模型/風險群     → 反脆弱、安全邊際
```

### 第 4 維：素材來源（必填）
```
#來源/Get-Notes     → 來自得到筆記
#來源/晨報          → 來自每日晨報
#來源/書            → 來自書籍
#來源/對話          → 來自與 Aclis 對話
#來源/網路          → 來自網路
#來源/原創          → 個人原創
```

### 第 5 維：狀態（必填）
```
#狀態/seed          → 種子（剛萌發）
#狀態/sprouting     → 成長中
#狀態/blooming      → 已驗證
#狀態/evergreen     → 恆綠（跨時空）
#狀態/archived      → 已封存
```

---

## 🎯 Tag 組合範例

```markdown
---
title: 巴菲特的「安全邊際」原則
tags:
  - 宮殿/Learning
  - 宮殿/Insights
  - Finance
  - 心智模型/風險群
  - 來源/書
  - 狀態/evergreen
---
```

### 對應人類解讀
這是個 evergreen 級洞察，源於書籍，屬於 Finance 領域，跨 Learning 與 Insights 宮殿，與風險決策相關。

---

## 📐 Tag 使用紀律

### ✅ 必填
- 第 1 維（宮殿）
- 第 2 維（領域）
- 第 4 維（來源）
- 第 5 維（狀態）

### 🔄 選填
- 第 3 維（心智模型）：只有與特定模型相關才加

### ⚠️ 注意事項
- 一個 Tag 只屬於一個維度（避免 `#Finance/Investment` 這種混亂）
- Tag 命名駝峰式（PascalCase）
- 避免過度細分（最多 3 層）

---

## 🔗 Obsidian 連結規則

### 連結類型

| 語法 | 意義 | 範例 |
|------|------|------|
| `[[Page]]` | 同目錄連結 | `[[MM-01-First-Principles]]` |
| `[[Page\|顯示文字]]` | 自訂顯示文字 | `[[MM-01-First-Principles\|第一性原理]]` |
| `[[#Heading]]` | 連結到頁面內標題 | `[[MOC-Mental-Models#決策群]]` |
| `[[Page#Heading]]` | 連結到指定頁面標題 | `[[MM-01-First-Principles#操作步驟]]` |
| `![[Page]]` | 嵌入頁面 | `![[Insight-Template]]` |

### 連結策略

```
1. 入口頁（Palette / MOC）→ 卡片頁 → 內容
2. 雙向連結：每個卡片頁都應連結回入口
3. 跨宮殿連結：[[Related]]
4. 失效連結：每月檢查 + 修補
```

### 連結密度原則

```
太稀疏（< 3 連結/頁）：
  → 知識孤島，無法發揮 Graph View

太密集（> 30 連結/頁）：
  → 連結噪音，難以閱讀

理想（5-15 連結/頁）：
  → 形成有意義的知識節點
```

---

## 📂 目錄結構與命名

```
wiki/
├── index/                  ← 所有 MOC/入口頁
│   ├── Hermes-Digital-Brain-MOC.md
│   ├── MOC-Memory-Palace.md
│   ├── MOC-Knowledge-Domains.md
│   ├── MOC-Mental-Models.md
│   ├── MOC-Tag-Guide.md
│   ├── MOC-Insights.md
│   ├── MOC-Decisions.md
│   └── MOC-GetNotes-Tag地圖.md
│
├── entities/               ← 具體知識卡片
│   ├── memory-palace/      ← 6 座宮殿的 Palette
│   ├── mental-models/      ← 14 個心智模型
│   ├── people/             ← 人物誌
│   └── topics/             ← 主題卡片
│
├── synthesis/              ← 綜合產出
│   ├── frameworks/         ← 思維框架
│   ├── insights/           ← 洞察集合
│   └── decisions/          ← 決策日誌
│
├── templates/              ← 空白模板
│   ├── Insight-Template.md
│   └── Decision-Template.md
│
└── _raw_getnotes/          ← 待消化素材
    └── YYYY-MM-DD/         ← 每日素材
```

---

## 🔄 工作流整合

```
1. 攝入（Ingestion）
   ↓ Get Notes 進來
   ↓ 標記 #來源/Get-Notes + 5 維 Tag
2. 蒸餾（Distillation）
   ↓ 抽出可複用觀念
   ↓ 寫入 entities/topics/
3. 連結（Connection）
   ↓ 雙向連結到相關宮殿/模型/洞察
4. 沉澱（Sedimentation）
   ↓ 跨多個素材 → 形成 Insight → MOC-Insights
5. 決策（Decision）
   ↓ 重大決策 → 寫入 Decision 日誌 → MOC-Decisions
6. 應用（Application）
   ↓ 在對話中引用，閉環到日常
```

---

## 🤖 給 Aclis 的指令

```
1. 攝入新素材時，自動標記 5 維 Tag
2. 發現兩個卡片有邏輯關聯，自動加 [[link]]
3. 每月心跳時，review 所有 Tag 規範
4. 提醒：任何卡片缺 Tag 或缺連結 → 補齊
5. 每季：清理過時卡片（archived）
```

---

## 📌 Tag 演進規則

```
V1.0（2026-06-22）：5 維 Tag + 駝峰式命名
V1.1（規劃中）：增加 #優先級 維度
V2.0（未來）：連結機器學習 → 自動推薦 Tag
```

---

## 🔗 相關頁面

- [[Hermes-Digital-Brain-MOC]] — 主入口
- [[MOC-Memory-Palace]] — 宮殿索引
- [[MOC-Knowledge-Domains]] — 領域索引
- [[Insight-Template]] — 洞察模板
- [[Decision-Template]] — 決策模板

---

**建立日期：** 2026-06-22
**版本：** v1.0
**規範遵守：** Aclis 自動監測 + Jan 最終決定
