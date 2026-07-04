# 🛠️ Skill 備份 · templates/morning-report-v6.md

> **備份日期**：2026-07-04  
> **來源路徑**：`/workspace/skills/semicon-morning-report/templates/morning-report-v6.md`  
> **KB**：🛠️ 技能模板（`JOaEOM5Y`）  
> **管理員**：Aclis 🐉

---

# 💾 半導體晨報模板（v6.1 — skill 化版）

> 此模板由 `/workspace/skills/semicon-morning-report/SKILL.md` 引用  
> Cron payload 應指向此檔（單一真相來源）

## 觸發條件

- 每日 09:00 CST（cron 自動）
- 或手動觸發：「半導體晨報」/「semicon report」

## 執行流程

### Step 1：Web 搜索（5 組並行）

```python
queries = [
    "ASML EUV Q2 2026 orders revenue",
    "TSMC CoWoS capacity 2026 monthly wafer",
    "HBM3e HBM4 SK Hynix Samsung Micron 2026",
    "SEMI equipment market 2026 forecast",
    "NVIDIA Blackwell Rubin supply chain",
]
# batch_web_search
```

### Step 2：Semantic Recall

```bash
POST https://openapi.biji.com/open/api/v1/resource/recall
Body: { "query": "CoWoS HBM ASML 半導體 超級週期", "top_k": 5 }
```

### Step 3：載入 Skill References

- `references/models/M1-Moore-Law.md` ~ `M5-Revenue-Elasticity.md`
- `references/sources/tier1-whitelist.md`
- `references/risk/six-dimensions.md`
- `references/anomaly-detection.md`

### Step 4：異常偵測（v6.1 新增）

- Layer 1：來源矛盾
- Layer 2：時序偏移
- Layer 3：模型一致性

### Step 5：產出 Markdown

```markdown
# 💾 半導體晨報 · {{date}}

> 📅 日期 / 📊 數據基準
> 📡 資料來源：[列表] | v6.1（skill 化版 + 異常偵測）
> 🤖 Aclis 自動產出

## 📌 執行摘要（30秒版）

> **本期核心判斷**

| 主題 | 信號 | 評估 |
|------|------|------|
| 🔴 | ... | ... |

## 🧮 五大模型

### M1｜摩爾定律量化曲線
[從 references/models/M1 載入最新數據]

### M2｜CoWoS 供需缺口
[從 references/models/M2 載入]

### M3｜設備時滯
[從 references/models/M3 載入]

### M4｜HBM 超級循環
[從 references/models/M4 載入]

### M5｜營收彈性
[從 references/models/M5 載入]

## 📰 三大頭條

1. **🔴 ...** (一句話 + 數字 + 來源)
2. **🟡 ...**
3. **🟢 ...**

## ⚖️ 風險六維

| 維度 | 評估 |
|------|------|
| 🌐 宏觀 | ... |
| 🏭 企業 | ... |
| 💹 系統 | ... |
| 📊 估值 | ... |
| 🌍 地緣 | ... |
| ⚡ 供需 | ... |

**Risk Score**: X.X / 3.0

## 🚨 異常警示（v6.1 新增）

| 類型 | 指標 | 異常值 | 預期值 | 處理 |
|------|------|--------|--------|------|
| ... | ... | ... | ... | ... |

## 💡 投資排序

🥇 **HBM / 記憶體** > 🥈 **先進封裝 CoWoS** > 🥉 **設備（ASML/AMAT/Lam）** > **代工（TSMC）** > **晶片設計（NVIDIA）**

## 🔗 資料來源

| # | 來源 | URL |
|---|------|-----|
| 1 | ... | ... |
```

### Step 6：寫入三軌

1. **Get Notes**：topic_id `pn5rkG6Y`（💾 晨報·半導體）
2. **Obsidian Vault**：`/workspace/obsidian/11_AI_Tech/11-2_Semiconductor/Semiconductor_{{date}}.md`
3. **GitHub**：PUT 到 FoxUltimate/Obsidian-Vault

### Step 7：完成回報

- note_id
- GitHub commit SHA
- 異常清單（如有）

---

## 版本記錄

- **v6.0**（2026-05-15）：模型化公式版
- **v6.1**（2026-07-04）：skill 化 + 異常偵測

---

*此模板由 semicon-morning-report skill 管理*  
_Cron 引用方式：見 `/workspace/crons/prompts/INDEX.md`_

---

*Aclis 🐉 自動備份 · 2026-07-04 07:51 UTC*