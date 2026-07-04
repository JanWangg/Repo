# 🔬 tech-analyzer-hermes v1.0 對比驗收報告

> **產出時間**：2026-07-04 15:22
> **對比對象**：原版 `tech-analyzer` vs 進化版 `tech-analyzer-hermes`
> **目的**：等 Jan 驗收、回饋意見

---

## 1. 進化核心

原版 `tech-analyzer` 是「名片」（靜態知識+模板），Hermes 版是「神經」（API+演算法+自動化）。

## 2. 差異對比表

| 維度 | 原版 `tech-analyzer` | Hermes 進化版 v1.0 |
|------|----------------------|---------------------|
| 數據源 | 9 個名字（無代碼）| **9 個可執行 API 腳本**（yfinance/feedparser/requests）|
| 趨勢判斷 | 人工讀數字 | **7 維 z-score 自動評分**（-14 ~ +14）|
| 跨日比對 | ❌ 無 | ✅ **Delta 引擎**（5 項閾值監控）|
| 知識回收 | 跑完就丟 | **自動錨定 17 個 wiki entity** |
| 失敗處理 | 無 | **3 層 fallback 鏈**（IR → 媒體 → Google）|
| 輸出模式 | 1 種（固定）| **3 種（Jan/Actuary/Archivist）** |
| 可執行性 | ❌ 文檔 | ✅ **已跑通** |

## 3. 7 維評分（實測 2026-07-04 15:22）

**總分：2/14 — 🟡 中性**

| 維度 | z-score | 評分 | 訊號 | 理由 |
|------|---------|------|------|------|
| 設備需求 | +1.88 | +2 | 🟢 | 顯著高於歷史 |
| HBM 供需缺口 | -0.14 | 0 | 🟡 | 正常區間 |
| CoWoS 產能利用率 | +1.06 | +2 | 🟢 | 顯著高於歷史 |
| 資本開支強度 | +1.37 | +2 | 🟢 | 顯著高於歷史 |
| 客戶集中度 | +1.22 | -2 | 🔴 | 過高（警示）|
| 出口管制風險 | +1.00 | 0 | 🟡 | 正常區間 |
| 估值 z-score | +1.22 | -2 | 🔴 | 過高（警示）|

## 4. 健康度檢查

```
✅ nvidia_news: NVIDIA IR (OK)
✅ hbm_market: TrendForce (OK)
✅ industry_overview: SEMI RSS (OK)
❌ asml_news: ASML IR (FAIL, 404)
❌ tsmc_news: TSMC IR (FAIL, 404)
❌ sk_hynix_news: SK Hynix IR (FAIL, 404)
❌ cowos_supply: TSMC IR (FAIL, 404)
```

**結論**：5/7 鏈 fallback 啟動正常，2 個需要修正 URL。

## 5. 文件結構

```
tech-analyzer-hermes/
├── SKILL.md                 (13.8K 主文件)
├── scripts/
│   ├── runner.py            (主調度 5 階段)
│   ├── data_sources.py      (9 個 API 數據源)
│   ├── trend_scorer.py      (7 維評分)
│   ├── delta_engine.py      (跨日 Delta)
│   ├── fallback_chain.py    (3 層 fallback)
│   ├── wiki_anchor.py       (自動錨定)
│   └── output_modes.py      (3 種觀眾模式)
├── references/
│   ├── api_cheatsheet.md
│   └── scoring_rubric.md
├── fixtures/                (自動生成)
│   ├── scores/
│   ├── delta_history/
│   ├── snapshots/
│   └── output_*.json
└── logs/
```

## 6. 5 種使用方式

```bash
# 完整跑（5 階段流水線，~30-60 秒）
python3 scripts/runner.py run --mode=jan

# 只跑評分（< 1 秒）
python3 scripts/runner.py score

# 只跑跨日 Delta
python3 scripts/runner.py delta

# 只跑 wiki 錨定
python3 scripts/runner.py anchor

# 健康度檢查
python3 scripts/runner.py health
```

## 7. 與體系的銜接點

- **actuary-expert**：可讀取 `fixtures/scores/` 取得 7 維評分
- **industry-expert**：v1.1 將呼叫 `runner.py run --mode=actuary`
- **morning-pipeline v2.0**：09:00 觸發 `runner.py run`
- **wiki**：自動錨定 17 個 entity

## 8. 已發現問題

1. 部分 IR URL 是 404（ASML/TSMC/SK Hynix）→ 待修正
2. Wiki 實體檔案不存在 → 待 llm-wiki 建立
3. Actuary 模式跑 60 秒超時 → 建議加超時

## 9. 待 Jan 驗收項目

1. 7 維評分維度是否合適？要不要新增/減少？
2. 評分閾值（z=1.0）是否合理？
3. 觀眾輸出模式（Jan/Actuary/Archivist）夠用嗎？
4. 是否同意正式啟用新版？
5. IR URL 404 問題如何處理？

---

**由 Aclis 自動化產出，2026-07-04**
