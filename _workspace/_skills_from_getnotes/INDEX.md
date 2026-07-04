---
type: skill_index
created: 2026-07-02
source: getnotes://🛠️ 技能模板 (JOaEOM5Y)
extracted_count: 17 skill files
---

# 🛠️ 技能模板索引 — 從 Get Notes 取得

> **取得時間：** 2026-07-02
> **來源 KB：** Get Notes「🛠️ 技能模板」(JOaEOM5Y)
> **總檔案：** 17 個 skill 模板
> **原始備份日：** 2026-07-04（雲端）
> **下載路徑：** `/workspace/jan-vault/_workspace/_skills_from_getnotes/`

---

## 🎯 取得原因

Jan：「🛠️ 技能模板（檔案夾）在 Get Notes 上取得」

Aclis 直接執行：
1. 用 Get Notes API 撈 KB JOaEOM5Y 全部 20 篇 notes
2. 篩選「Skill 備份」標籤的 17 篇
3. 存到 vault `_workspace/_skills_from_getnotes/`
4. 建立本索引

---

## 📦 取得清單（17 個檔案）

### 🚀 核心 Skills（2 個）

| Skill | 檔案 | 用途 |
|-------|------|------|
| **semicon-morning-report** | `SKILL.md` (3785 chars) | 半導體晨報 — 五大量化模型（M1-M5）+ 六維風險 |
| **huashu-nuwa** | `huashu-nuwa_SKILL.md` (6638 chars) | 女媧造人 — 自動生成人物思維框架 Skill |

### 🧮 M1-M5 量化模型（5 個心智模型）

| 模型 | 檔案 | 核心公式 |
|------|------|---------|
| **M1** Moore's Law | `M1-Moore-Law.md` | 摩爾定律：製程密度每 18 個月翻倍 |
| **M2** CoWoS 供需 | `M2-CoWoS-Supply-Demand.md` | 缺口% = (需求-實際)/需求 |
| **M3** 設備時滯 | `M3-Equipment-Lag.md` | 領先指標 6-12 月 |
| **M4** HBM 超級週期 | `M4-HBM-Supercycle.md` | 市佔 × ASP × 良率 |
| **M5** 營收彈性 | `M5-Revenue-Elasticity.md` | 終端 AI 需求敏感度 |

### 📋 References（5 個輔助文件）

| 檔案 | 用途 |
|------|------|
| `anomaly-detection.md` | 異常偵測 SOP（與昨日對比） |
| `six-dimensions.md` | 六維風險評估（宏觀/企業/系統/估值/地緣/供需） |
| `tier1-whitelist.md` | Tier 1 來源白名單（ASML/TSMC/SEMI/Reuters...） |
| `templates_morning-report-v6.md` | 晨報 v6 模板 |
| `semiconductor_report.md-(cron-prompt)` | Cron 觸發 prompt |

### 🛠️ huashu-nuwa 完整包（5 個檔案）

| 檔案 | 用途 |
|------|------|
| `huashu-nuwa_references_extraction-framework.md` | Phase 2 提取框架（心智模型/反模式/表達 DNA）|
| `huashu-nuwa_references_templates_skill-template.md` | SKILL.md 模板 |
| `huashu-nuwa_references_README.md` | 使用說明 |
| `huashu-nuwa_scripts_README.md` | 腳本說明 |

---

## 🔍 與本地對比

**本地已存在的 skills（~/.hermes/skills/）：**
- `tech-analyzer-hermes` ← 可能用這些模板生成
- `tech-analyzer`
- `invest-analyzer`
- `industry-expert`
- `daily-morning-distill` / `morning-report-distill`
- `reading-morning-report`
- ...（共 20+ 個）

**從 Get Notes 取回的 17 個 = 模板 + 參考檔**，可能比本地版更詳細或更新。

---

## ⚡ 接下來可以做的

1. [ ] 比對 Get Notes 模板 vs 本地 skill，找出差異
2. [ ] 用 huashu-nuwa 框架重新生成 / 更新本地 skill
3. [ ] 跑一次 semicon-morning-report skill 驗證模板有效
4. [ ] 把 17 個檔案 commit 到 GitHub

---

## 🔗 連結

- Get Notes KB：🛠️ 技能模板 (JOaEOM5Y)
- 本地 skills：`~/.hermes/skills/`
- 今日日誌：`_workspace/memory/2026-07-02.md`

---

*由 Aclis (小A) 取得 · 2026-07-02*
*方法：直接呼叫 Get Notes API + 自動分類*
*響應：Jan「日日新，又日新」*