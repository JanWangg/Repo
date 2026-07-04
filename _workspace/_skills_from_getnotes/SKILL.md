# 🛠️ Skill 備份 · SKILL.md

> **備份日期**：2026-07-04
> **來源路徑**：`/workspace/skills/semicon-morning-report/SKILL.md`
> **KB**：🛠️ 技能模板（`JOaEOM5Y`）
> **管理員**：Aclis 🐉

---

---
name: semicon-morning-report
description: |
  半導體晨報 skill — 覆蓋 CoWoS / HBM / 設備 / 代工 / 晶片設計五大領域的每日量化分析報告。
  使用五大模型（M1-M5）+ 六維風險評估框架，產出 8-12 KB Markdown 報告。
  觸發關鍵詞：「半導體晨報」「semicon morning report」「💾 晨報」「半導體分析」「產一份半導體晨報」「幫我跑半導體晨報」。
  支援三種觸發模式：(1) Cron 自動觸發 09:00 CST (2) 手動即時觸發 (3) 增量更新（與昨日對比 + 異常偵測）。
  來源優先 Tier 1：ASML / TSMC / SEMI / TrendForce / Digitimes / Reuters / FT。
---

# 💾 半導體晨報 Skill（v6 模型化公式版 · skill 化）

> 「CoWoS 缺口還有多遠？HBM4 誰能卡位？設備交期是領先指標還是落後指標？」
> — 五大模型 + 六維風險，把半導體超級週期量化到能決策的程度。

## 🎯 Skill 邊界

**這個 Skill 會做：**
- ✅ 每日產出半導體晨報（覆蓋 CoWoS / HBM / 設備 / 代工 / 晶片設計）
- ✅ 五大量化模型（M1-M5）數據更新與對比
- ✅ 六維風險評估（宏觀/企業/系統/估值/地緣/供需）
- ✅ 異常偵測：與昨日對比，數據矛盾警示
- ✅ 來源驗證：Tier 1 官方來源優先
- ✅ 寫入 Get Notes + Obsidian Vault + GitHub

**這個 Skill 不會做：**
- ❌ 投資建議（只給排序，不下 buy/sell call）
- ❌ 個股財報深度分析（用 investment-research-analyst skill）
- ❌ 預測未來股價走勢
- ❌ 評論單一公司治理問題

---

## 🚀 觸發方式

| 觸發模式 | 觸發條件 | 用途 |
|---------|---------|------|
| **Cron 自動** | 每日 09:00 CST（payload 引用此 skill templates） | 標準晨報 |
| **手動即時** | Jan 說「產一份半導體晨報」「幫我跑半導體晨報」 | 臨時查詢/補發 |
| **增量更新** | 「半導體晨報增量版」「與昨日對比」 | 只跑差異部分 |

---

## 🧮 五大量化模型（核心引擎）

> 詳細模型定義見 `references/models/M1-Moore-Law.md` ~ `M5-Revenue-Elasticity.md`

| 模型 | 量化對象 | 核心公式 | 更新頻率 |
|------|---------|---------|---------|
| **M1** 摩爾定律 | 製程密度演進 | $N(t) = N_0 \times 2^{(t-t_0)/18M}$ | 季度 |
| **M2** CoWoS 供需 | 先進封裝缺口 | 缺口% = (需求-實際)/需求 | 月度 |
| **M3** 設備時滯 | 設備市場/交期 | 領先指標 6-12 月 | 月度 |
| **M4** HBM 循環 | 記憶體超級週期 | 市佔率 × ASP × 良率 | 月度 |
| **M5** 營收彈性 | 公司景氣敏感度 | 彈性係數 vs 終端 AI 需求 | 季度 |

---

## ⚖️ 六維風險評估（v2.0 標準）

> 詳細 SOP 見 `references/risk/six-dimensions.md`

```
🌐 宏觀 → 美聯儲 / 利率 / 美元 / 通膨
🏭 企業 → 公司護城河 / 良率爬坡 / 客戶集中
💹 系統 → 估值位階 / 集中度 / 槓桿
📊 估值 → P/E 河流圖 / Forward vs Trailing
🌍 地緣 → 台海 / 美中出口管制 / TSMC 海外佈局
⚡ 供需 → HBM 缺口 / CoWoS 產能 / 設備交期
```

---

## 📋 標準執行流程（7 步）

### Step 1：來源白名單檢查
讀取 `references/sources/tier1-whitelist.md`，確認當前查詢覆蓋 Tier 1 來源。

### Step 2：並行 5 組核心查詢

```python
queries = [
    "ASML EUV Q2 2026 orders revenue",
    "TSMC CoWoS capacity 2026 monthly wafer",
    "HBM3e HBM4 SK Hynix Samsung Micron 2026",
    "SEMI equipment market 2026 forecast",
    "NVIDIA Blackwell Rubin supply chain",
]
# 使用 batch_web_search 執行
```

### Step 3：Semantic Recall（從 Get Notes 取過往洞察）

```bash
POST https://openapi.biji.com/open/api/v1/resource/recall
Body: { "query": "CoWoS HBM ASML 半導體 超級週期", "top_k": 5 }
```

### Step 4：五大模型數據填充
從 references/models/ 讀取最新數據，填入晨報模板。

### Step 5：異常偵測（v6.1 新增）

```python
# 與昨日對比
diff = today_data - yesterday_data
if abs(diff) > threshold:
    flag_anomaly(model_id, metric, diff, source)
```

異常類型：
- 🔴 **數據矛盾**：兩個 Tier 1 來源數字衝突 >5%
- 🟡 **重大偏移**：與昨日比變化 >10%
- 🟢 **預期變化**：與昨日比變化 3-10%（正常）

### Step 6：產出 Markdown 報告（8-12 KB）
使用 `templates/morning-report-v6.md` 模板填充。

### Step 7：寫入三軌
1. Get Notes（雲端攝入）
2. Obsidian Vault（`/workspace/obsidian/11_AI_Tech/11-2_Semiconductor/`）
3. GitHub（FoxUltimate/Obsidian-Vault）

---

## 🔗 與其他 Skill 的關係

| Skill | 關係 | 何時用 |
|-------|------|--------|
| `huashu-nuwa` | 上游 | 想蒸餾某半導體專家的思維框架 |
| `investment-research-analyst` | 平行 | 想做單一個股深度分析 |
| `investment-morning` | 平行 | 投資晨報（更廣的市場觀） |
| `rawmaterials-semi` | 平行 | 半導體原材料晨報（鋁/銅/鎢） |

---

## 📝 版本演化

- **v1.0**（2026-03-23）：初版三大頭條 + 來源列表
- **v6.0**（2026-05-15）：模型化公式版，五大量化模型確立
- **v6.1**（2026-07-04）：**skill 化** + 異常偵測 + 增量模式

---

## 🐉 Aclis 的使用方式

Jan 可以這樣叫我：

> 「跑今天的半導體晨報」
> 「半導體晨報增量版」
> 「幫我看 M2 CoWoS 模型最近怎樣」
> 「半導體晨報異常偵測模式」

我會自動：
1. 判斷觸發模式（標準/增量/異常）
2. 載入對應 references
3. 執行 7 步流程
4. 三軌寫入

---

_此 skill 由 Aclis 🐉 從 `/workspace/crons/prompts/semiconductor_report.md` 升級封裝_
_2026-07-04 啟用 · 與 cron payload 完全相容_

---

_Aclis 🐉 自動備份 · 2026-07-04 07:51 UTC_
