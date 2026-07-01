# 採購智能化 n8n AI 系統 — 文件索引
> 版本：v1.0 | 日期：2026-03-25 | 語言：繁體中文

---

## 📁 文件結構

```
/workspace/docs/n8n_procurement_ai/
├── 00_INDEX.md                              ← 本文件索引
├── 01_n8n_Workflow_Design.md              ← n8n Workflow 設計（Agent 0-4）
├── 02_Agent_Prompt_Library.md             ← AI Agent Prompt 函式庫（14 個 Prompt）
├── 03_System_Integration_Spec.md           ← T100 × n8n × Domino 整合規格書
├── 04_ROI_Analysis.md                    ← ROI 評估報告（已用 AOP 實際數值）
├── 05_Outsourcing_Workflow.md            ← 委外AI Workflow（Agent 4）
├── 06_Procurement_Cycle_Complete_Map.md ← 採購全景圖 v2.0（T100 七大模組）
├── 07_Invoice_Automation.md              ← 發票自動化 Workflow（Agent 5，aapt110）
└── 08_系統分析開發報告_完整版.md        ← 完整系統分析與開發報告（可交付版）
```

---

## 📋 各文件用途

| 文件 | 主要內容 | 交付對象 |
|------|---------|---------|
| 01_n8n_Workflow_Design.md | n8n 節點圖 + JSON Workflow + Agent 定義 | n8n 開發者 |
| 02_Agent_Prompt_Library.md | 10 個完整中文 Prompt | n8n 開發者 / AI 維護者 |
| 03_System_Integration_Spec.md | API 端點 / 先行驗證清單 / 時程規劃 | IT 團隊 |

---

## 🎯 使用方式

### 第一步：給 n8n 開發者的文件
→ 請 IT 同事閱讀 `03_System_Integration_Spec.md` 第 1-2 節
→ 進行 T100 API / Domino IMAP 的環境驗證

### 第二步：建立 n8n Workflow
→ n8n 開發者根據 `01_n8n_Workflow_Design.md` 的 JSON 結構建立 Workflow
→ 逐一設定 Agent 0-3

### 第三步：設定 AI Prompt
→ 將 `02_Agent_Prompt_Library.md` 中的 Prompt 貼入各 Agent 節點
→ 根據實際使用的 LLM（Claude / GPT-4o / MiniMax）調整格式

### 第四步：Pilot 測試
→ 依據 `03_System_Integration_Spec.md` 第 7 節的「先行驗證清單」執行

---

## 🔑 核心設計共識（來自 Jan 的輸入）

- **n8n AI Agent**：使用 n8n 內建 AI Agent（LangChain + Tool Calling）
- **Prompt 語言**：全中文
- **T100**：鼎捷 ERP，HTTP REST API 為主要串接方式
- **Domino**：IMAP/SMTP，採購機器人專用 ID
- **Agent 數量**：4 個（0 協調者 + 1 RFQ + 2 PO追蹤 + 3 通訊）
- **Gate 數量**：3 個（人類審核點）
- **最後輸出**：T100 寫入（由人確認後執行）

---

*最後更新：2026-03-25*
