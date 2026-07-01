# Tag 索引 — 知識宮殿的地圖

> 這是整個 02_Knowledge 的入口索引。
> 每個 Tag 都是一條「快速通道」，直達相應領域的精華沉澱。
> 更新頻率：隨著新筆記建立即時更新。

---

## Domain Tags（按領域分層）

### #AI — 人工智慧

| Tag | 說明 | 精華筆記 |
|-----|------|---------|
| `#AI/LLM` | 大型語言模型 | [[../011_AI_Tech/2026/DeepSeek-V3_MLA架构分析]] |
| `#AI/Agent` | AI Agent / 代理人 | （陸續建立） |
| `#AI/Physical` | 實體 AI / 機器人 | （陸續建立） |
| `#AI/Hardware` | AI 硬體加速 | [[00_Evergreen/Memory-Wall]] [[00_Evergreen/HBM]] [[00_Evergreen/CoWoS]] [[00_Evergreen/Blackwell]] |

### #Semiconductor — 半導體

| Tag | 說明 | 精華筆記 |
|-----|------|---------|
| `#Semi/Fab` | 晶圓製造 | （陸續建立） |
| `#Semi/Equipment` | 半導體設備 | （陸續建立） |
| `#Semi/Packaging` | 先進封裝（CoWoS / SoIC） | [[00_Evergreen/CoWoS]] |
| `#Semi/Memory` | 記憶體（HBM / DRAM） | [[00_Evergreen/HBM]] |
| `#Semi/Design` | IC 設計 | （陸續建立） |

### #Investment — 投資

| Tag | 說明 | 精華筆記 |
|-----|------|---------|
| `#Invest/Valuation` | 估值方法論 | [[00_Evergreen/Moat]] [[00_Evergreen/Memory-Wall]] |
| `#Invest/Risk` | 風險管理 | （見 [[../013_Investment/README]]） |
| `#Invest/Macro` | 宏觀投資 | （見每日晨報） |
| `#Invest/Portfolio` | 組合管理 | （見每日晨報） |

### #Macro — 宏觀經濟

| Tag | 說明 | 精華筆記 |
|-----|------|---------|
| `#Macro/Fed` | 美聯準政策 | （見每日晨報） |
| `#Macro/China` | 中國經濟 | （見每日晨報） |
| `#Macro/Geopolitics` | 地緣政治 | （見每日晨報） |
| `#Macro/RawMaterials` | 原物料 | [[../014_Raw_Materials/README]] |

### #Reading — 閱讀沉澱

| Tag | 說明 | 精華筆記 |
|-----|------|---------|
| `#Reading/Wisdom` | 智慧/哲學 | （見 [[../015_Reading/README]]） |
| `#Reading/Business` | 商業/管理 | （見 [[../015_Reading/README]]） |
| `#Reading/Investment` | 投資相關 | （見 [[../015_Reading/README]]） |

### #Meta — 後設（關於學習本身）

| Tag | 說明 | 精華筆記 |
|-----|------|---------|
| `#Meta/Learning` | PKM 方法論 | （本文件） |
| `#Meta/Writing` | 寫作心法 | （陸續建立） |

---

## Concept Tags（跨領域，無階層）

這些 Tag 跨越所有領域，出現在任何相關筆記中：

| Tag | 說明 | 核心筆記 |
|-----|------|---------|
| `#Concept` | 概念（抽象原則） | [[00_Evergreen/Memory-Wall]] [[00_Evergreen/HBM]] [[00_Evergreen/CoWoS]] [[00_Evergreen/Moat]] |
| `#Entity` | 實體（公司/人/產品） | [[00_Evergreen/NVIDIA]] |
| `#Topic` | 主題（多維度深度分析） | （陸續建立） |

### 技術概念

```
#CoWoS  #HBM  #HBM3E  #HBM3  #Blackwell  #GB300  #GB200
#EUV  #High-NA-EUV  #ASIC  #CUDA  #CUDA-Ecosystem  #Foundational-Model
#MLA  #MoE  #Transformer  #Memory-Wall  #Advanced-Packaging
```

### 投資概念

```
#Moat  #ROI  #Margin-of-Safety  #Second-Order  #First-Principles
#Compounding  #Snowball  #Position-Sizing
```

### 心智模型

```
#Inversion  #Second-Order  #First-Principles  #Probabilistic
#Wisdom  #Compounding  #Edge
```

---

## 使用方式

**快速查找**：在 Obsidian 中輸入 `#Semi/Memory`，即可找到所有記憶體相關筆記。

**建立新筆記時**：在 frontmatter 中加入 `tags: [ #Domain/X, #Concept ]`，自動匯入此索引。

**跨域連結**：一篇筆記可以同時有多個 Domain Tags，例如：
- [[00_Evergreen/Memory-Wall]] → `#Semi/Memory` + `#AI/Hardware` + `#Concept`

---

## Tag 生產規則

1. 每篇新 Evergreen 筆記必須標記至少一個 Domain Tag + 一個 Concept Tag
2. 每季檢查一次此索引，移除閒置 Tag，更新連結
3. Concept Tags 保持精簡，原則上不新增已有概念的變體

---

*最後更新：2026-05-02 by Aclis（大A）*