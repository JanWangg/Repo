# 發票自動化 AI Workflow 設計
## 應付帳款 × T100 aapt110 × AI 智能比對
> 版本：v1.0 | 日期：2026-03-25 | 語言：繁體中文
> 依據：T100 ERP 系統手冊 + 採購循環全景圖 v2.0

---

## 1. 發票自動化全景圖

```
【發票生命周期全流程】

  供應商寄出發票
         │
         ▼
  【AI 接收站】
  ├─ Email（IMAP）→ 自動接收
  ├─ 掃描 PDF → AI OCR 解析
  └─ 手動上傳 → AI OCR 解析
         │
         ▼
  【AI 處理站】
  ├─ 發票解析（LLM 提取欄位）
  ├─ T100 比對（PO/入庫/核價）
  ├─ 異常偵測與分類
  └─ 建議行動
         │
    ┌────┴────┐
    ▼         ▼
  自動通過    需要審核
  → 直接過帳   → Slack/Email
    T100 AP   → 人確認
         │
         ▼
  【付款準備】
  ├─ 沖銷預付款（如有）
  ├─ 產生付款建議
  └─ 對帳完成
```

---

## 2. T100 應付帳款流程回顧（aapt110）

### 2.1 系統原流程

```
【aapt110 對帳作業 — 系統原流程】

Step 1：進貨入庫（asft340）完成
  → 系統自動產生「進貨憑單」

Step 2：供應商寄出發票
  → 發票送到 AP 部門

Step 3：AP 人員手動比對
  ├─ 發票金額 vs PO 單價 × 數量
  ├─ 發票數量 vs 入庫數量
  └─ 是否有預付款需要沖銷

Step 4：比對結果
  ├─ 匹配 → 確認付款
  ├─ 有差異 → 與供應商對帳
  └─ 有問題 → 暫緩付款

Step 5：月底大量付款處理
  → 拋轉至票據系統
  → 出納執行付款

【痛點】：Step 3 全靠人工，沒有系統支援
         發票格式各異（紙本/電子/PDF/Email）
         人為錯誤 → 重複付款 / 溢付
```

### 2.2 AI 自動化切入點

```
【AI 在 aapt110 的價值】

✗ 過去：人對人，速度慢，錯誤多
✓ 現在：AI + T100，速度快，錯誤少

AI 帶來的核心改變：
1. 發票解析自動化（LLM OCR）
2. 比對判斷自動化（不再靠人工核對）
3. 異常預警即時化（付款前就發現問題）
4. 重複付款偵測（AI 比對所有歷史發票）
5. 付款時間優化（維護供應商關係 + 現金流平衡）
```

---

## 3. AI 發票自動化 Workflow

### 3.1 完整 Workflow 設計

```
【觸發點 1】Email 接收發票（IMAP）
  └─ Domino IMAP → n8n Email Trigger
      過濾條件：Subject 含「發票」「Invoice」「送款」

【觸發點 2】PDF 掃描上傳（Webhook）
  └─ AP 人員上傳 PDF → n8n Webhook

【觸發點 3】T100 asft340 入庫完成（Webhook）
  └─ 自動觸發待處理的發票清單

【Node：AI 發票解析師】（Agent 5）
  └─ LLM 讀取發票內容
      提取欄位：發票號、日期、供應商、品名、數量、單價、總金額、稅額

【Node：T100 資料交叉比對】
  ├─ 讀取 apmt500（PO 明細）
  ├─ 讀取 asft340（實際入庫數量）
  ├─ 讀取 aapt110（歷史付款記錄）
  └─ 讀取 axmt421（核價資料）

【Node：異常偵測引擎】
  ├─ 金額異常偵測
  ├─ 數量異常偵測
  ├─ 重複發票偵測
  └─ 預付款沖銷計算

【分支決策】

  ┌─ 正常（綠燈）────────────────┐
  │  AI 自動確認                  │
  │  → 寫入 T100 aapt110         │
  │  → 標記「已驗證」              │
  │  → 通知 AP 準備付款            │
  └────────────────────────────────┘

  ┌─ 小幅差異（黃燈）───────────┐
  │  AI 標註差異原因             │
  │  → 通知 AP 人員              │
  │  → 人確認後執行              │
  └────────────────────────────────┘

  ┌─ 重大異常（紅燈）───────────┐
  │  AI 立刻預警               │
  │  → 通知 AP 主管             │
  │  → 通知採購負責人           │
  │  → 阻斷付款，直到問題解決   │
  └────────────────────────────────┘
```

---

## 4. AI 發票解析 Prompt（P-012）

```
【AI 發票解析 Prompt — 通用版】

角色：AP 發票解析師
任務：從發票中提取結構化資訊

【支援格式】
- PDF（掃描或數位）
- 圖片（JPG/PNG）
- Email 內文（直接解析）
- Excel 格式報價單

【Prompt 內容】
───────────────────────────────────────────
請擔任 AP 發票解析師。從以下發票內容中提取結構化資訊。

【注意】發票可能來自不同地區（台灣/中國/泰國），格式各異。
你的任務是準確提取以下欄位，即使格式不規則或語言混雜。

【發票內容】
{invoice_content}

【輸出格式 — 嚴格遵守 JSON】
{
  "invoice_no": "發票號碼",
  "invoice_date": "YYYY/MM/DD 格式",
  "vendor_name": "供應商名稱（完整）",
  "vendor_tax_id": "統一編號/稅號",
  "buyer_name": "買受人名稱",
  "buyer_tax_id": "買受人統一編號",
  "items": [
    {
      "line_no": 項次,
      "item_no": "料號或品名",
      "description": "品名說明",
      "qty": 數量（數字）,
      "unit": "單位",
      "unit_price": 單價（數字）,
      "amount": 金額（數字）,
      "tax_rate": 稅率（如 0.05）
    }
  ],
  "subtotal": 小計,
  "tax_amount": 稅額,
  "total_amount": 總金額,
  "currency": "TWD/USD/CNY/THB",
  "payment_terms": "付款條件（如月結30）",
  "due_date": "發票到期日（YYYY/MM/DD）",
  "notes": "發票上其他重要資訊"
  "confidence_score": 0.0-1.0,
  "uncertain_fields": ["無法識別的欄位清單"]
}

【解析原則】
1. 當發票沒有固定格式時，盡量從上下文推斷
2. 當數字格式不同（如 NT$1,000 或 1000元）時，全部標準化為數字
3. 當發票是英文時，翻譯為中文並保留原文
4. 當 confidence_score < 0.7 時，在 uncertain_fields 中標註
5. 當找不到某個欄位時，該欄位寫 null，不要猜測
───────────────────────────────────────────
```

---

## 5. 發票異常偵測矩陣

```
【AI 發票比對矩陣】

╔══════════════════════╦══════════════════════════════════════════╗
║  比對項目           ║  異常判斷邏輯                          ║
╠══════════════════════╬══════════════════════════════════════════╣
║  發票 vs PO 單價    ║  超出 PO 單價 ± 容差率（通常 5%）   ║
║                     ║  → 標註「單價異常」                    ║
╠══════════════════════╬══════════════════════════════════════════╣
║  發票 vs PO 總金額  ║  超出 PO 總金額 ± 設定門檻          ║
║                     ║  → 標註「金額異常」                    ║
╠══════════════════════╬══════════════════════════════════════════╣
║  發票 vs 入庫數量   ║  發票數量 > 入庫數量                  ║
║                     ║  → 標註「數量異常：可能超前請款」      ║
╠══════════════════════╬══════════════════════════════════════════╣
║  重複發票偵測       ║  同一發票號 60 天內出現兩次          ║
║                     ║  → 🔴 立刻阻斷付款，通知 AP 主管       ║
╠══════════════════════╬══════════════════════════════════════════╣
║  歷史價格比對       ║  與近 3 次平均成交價差異 > 15%       ║
║                     ║  → 🟡 AI 標註「價格偏離」             ║
╠══════════════════════╬══════════════════════════════════════════╣
║  預付款沖銷        ║  有預付款（aapt310）→ 計算沖銷金額  ║
║                     ║  → 顯示「應付金額 = 發票金額 - 已預付」║
╠══════════════════════╬══════════════════════════════════════════╣
║  發票到期日        ║  早於 PO 需求日 → 🟡 提醒            ║
║                     ║  晚於 PO 需求日 30 天以上 → 🔴 警示  ║
╠══════════════════════╬══════════════════════════════════════════╣
║  統一編號驗證       ║  格式錯誤 → 🟠 標註「需人工核實」    ║
║                     ║  正常 → ✅                           ║
╚══════════════════════╩══════════════════════════════════════════╝

【異常燈號分級】

🟢 綠燈（正常）→ AI 自動通過，寫入 T100
   條件：所有比對項目均在容差範圍內

🟡 黃燈（小幅差異）→ 通知 AP 人員確認
   條件：差異金額 < 新台幣 5,000 元
   或：單價差異 < 3%

🔴 紅燈（重大異常）→ 立刻通知 AP 主管，阻斷付款
   條件：重複發票 / 金額差異 > $50,000 / 疑似偽造

🟠 橙燈（需人工核查）→ 標註，進入人工審核流程
   條件：統一編號格式不符 / 發票影本不清楚
```

---

## 6. T100 API 端點（aapt110 系列）

```
【aapt110 — 應付帳款對帳查詢】
GET /api/aapt110/query
參數：vendor_id, invoice_no, period, site, status
回應：
{
  "invoices": [{
    "invoice_no": "發票號",
    "vendor_id": "供應商",
    "vendor_name": "供應商名稱",
    "po_no": "PO 號",
    "invoice_date": "發票日期",
    "invoice_amount": 發票金額,
    "matched_amount": 已匹配金額,
    "variance": 差異金額,
    "payment_status": "pending/matched/partially_matched",
    "status": "N/Y",
    "matched_by": "系統比對/人工作業",
    "approval_status": "pending/approved/rejected"
  }]
}

【aapt110 — 發票匹配寫入】
POST /api/aapt110/match
Body：
{
  "invoice_no": "發票號",
  "po_no": "PO 號",
  "match_type": "auto/manual",
  "matched_by": "AI",
  "matched_items": [
    {
      "po_line_no": "PO 項次",
      "invoice_qty": 發票數量,
      "invoice_amount": 發票金額,
      "matched": true/false,
      "variance": 差異金額
    }
  ]
}

【aapt110 — 異常發票清單】
GET /api/aapt110/exceptions
參數：site, period
回應：所有被 AI 標註為異常的發票清單
→ 供 AP 人員審核

【aapt310 — 預付款查詢】
GET /api/aapt310/query
參數：vendor_id, po_no
回應：
{
  "advance_payments": [{
    "advance_no": "預付單號",
    "po_no": "PO 號",
    "vendor_id": "供應商",
    "advance_amount": 預付金額,
    "remaining_amount": 未沖銷餘額,
    "advance_date": 預付日期,
    "status": "active/partially_offset/fully_offset"
  }]
}

【aapt110 — 付款建議產生】
GET /api/aapt110/payment_suggestions
參數：vendor_id, payment_date
回應：建議執行的付款清單
→ AI 計算最佳付款時間（兼顧供應商關係 + 現金流）
```

---

## 7. AI 付款時間優化（進階能力）

```
【付款時間優化演算法】

目標：平衡「準時付款（維護供應商關係）」與「延遲付款（現金流優化）」

AI 輸入資料：
  ├─ 發票到期日
  ├─ 供應商重要程度（依採購金額）
  ├─ 公司現金流狀況（由財務提供）
  └─ 供應商談判力（歷史資料）

AI 輸出：「付款日建議」

╔═══════════════════╦═══════════════════════════════════╗
║  供應商等級     ║  AI 付款建議                      ║
╠═══════════════════╬═══════════════════════════════════╣
║  A 級（戰略）    ║  到期日前 3 天內支付              ║
║  B 級（主要）    ║  到期日當天支付                   ║
║  C 級（一般）    ║  到期日 + 5 天內支付              ║
║  D 級（替換）    ║  到期日 + 10 天內支付             ║
╚═══════════════════╩═══════════════════════════════════╝

付款日計算 Prompt：
───────────────────────────────────────────
你是 AP 付款策略顧問。根據以下資訊，計算最佳付款日期。

【輸入】
- 發票到期日：{due_date}
- 供應商等級：{vendor_tier}（A/B/C/D）
- 付款條件：{payment_terms}
- 公司現金流狀況：{cash_flow_status}（良好/正常/緊張）
- 供應商談判力：{vendor_leverage}（強/中/弱）

【輸出】
{
  "suggested_payment_date": "YYYY/MM/DD",
  "reasoning": "計算邏輯說明",
  "cash_saving": "若延後支付的利息節省金額",
  "relationship_impact": "對供應商關係的影響",
  "risk_level": "低/中/高",
  "alternative_options": [
    { "date": "選項1日期", "pros": "優點", "cons": "缺點" }
  ]
}
───────────────────────────────────────────
```

---

## 8. 預付款沖銷自動化（aapt310）

```
【預付款沖銷工作流】

背景：當公司支付預付款（訂金）給供應商時
      → 發票來了之後，需要把預付款沖掉

AI 自動化流程：

Step 1：PO 建立時，檢查是否有預付款（aapt310）
  └─ AI 查詢該 PO 的預付記錄

Step 2：發票到達
  └─ AI 計算：
      應付金額 = 發票總金額 - 已預付金額

Step 3：發票匹配（aapt110）
  └─ AI 自動執行預付款沖銷

Step 4：沖銷結果通知
  └─ AI 產生沖銷憑單，通知 AP + 採購

【預付款沖銷 Prompt（P-013）】

輸入：
  發票號：{invoice_no}
  發票金額：{invoice_amount}
  供應商：{vendor_id}
  PO 號：{po_no}
  預付單清單：{advance_payments[]}
    - 預付單號、預付日期、預付金額、已沖銷金額、餘額

任務：計算預付款沖銷

輸出：
{
  "invoice_amount": 發票總金額,
  "total_advance_paid": 預付款總金額,
  "already_offset": 已沖銷金額,
  "remaining_advance": 剩餘可用預付款,
  "amount_to_pay": 本次應付金額,
  "offset_records": [
    {
      "advance_no": "預付單號",
      "offset_amount": 沖銷金額,
      "remaining_after_offset": 沖銷後餘額
    }
  ],
  "ai_recommendation": "AI 建議"
}
```

---

## 9. 重複發票偵測（專門預防）

```
【重複發票偵測演算法】

這是 AP 工作中最貴的錯誤之一。
AI 可以比對所有歷史發票，確保不重複付款。

【AI 重複發票偵測 Prompt（P-014）】

任務：檢查這張發票是否與歷史發票重複

輸入：
  發票號：{invoice_no}
  供應商：{vendor_id}
  發票日期：{invoice_date}
  發票金額：{invoice_amount}
  料號清單：{items[]}

歷史比對清單（近 180 天）：
  {historical_invoices[]}

輸出：
{
  "is_duplicate": true/false,
  "confidence": 0.0-1.0,
  "duplicate_type": "exact/suspicious/similar",
  "duplicate_details": {
    "matched_invoice_no": "相似/重複的歷史發票號",
    "matched_invoice_date": "該發票日期",
    "matched_amount": "該發票金額",
    "days_apart": "相隔天數",
    "matching_fields": ["匹配的欄位"]
  },
  "action": "block_payment" | "manual_review" | "proceed"
}
```

---

## 10. AI 發票 Workflow JSON（n8n）

```json
{
  "name": "發票自動化 AI Workflow",
  "nodes": [
    {
      "name": "Trigger: IMAP 接收發票",
      "type": "n8n-nodes-base.emailTriggerImap",
      "position": [250, 200],
      "parameters": {
        "mailbox": "imap://{domino主機}:993",
        "filter": "SUBJECT '發票' OR SUBJECT 'Invoice' OR SUBJECT '送款'"
      }
    },
    {
      "name": "Trigger: PDF 上傳",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 350],
      "parameters": { "path": "invoice-upload" }
    },
    {
      "name": "Agent 5: 發票解析智能體",
      "type": "n8n-nodes-base.aiAgent",
      "position": [500, 275],
      "parameters": {
        "modelType": "Claude",
        "systemMessage": "你是發票解析專家。接收發票內容（PDF/Email/Image）後：\n1. LLM 解析發票欄位（P-012 Prompt）\n2. 結構化輸出 JSON\n3. 標註置信度低的欄位\n4. 對異常發票（如金額過大、格式不符）額外標註",
        "tools": ["LLM_Parse_Invoice", "OCR_PDF"]
      }
    },
    {
      "name": "T100 交叉比對",
      "type": "n8n-nodes-base.httpRequest",
      "position": [750, 275],
      "parameters": {
        "method": "POST",
        "url": "https://{{ $env.T100_HOST }}/api/aapt110/match",
        "authentication": "genericCredentialType"
      }
    },
    {
      "name": "AI 異常偵測引擎",
      "type": "n8n-nodes-base.aiAgent",
      "position": [1000, 275],
      "parameters": {
        "modelType": "Claude",
        "systemMessage": "你是發票異常偵測專家。根據比對結果，判斷：\n\n🟢 綠燈：所有比對正常 → 自動通過\n🟡 黃燈：小幅差異 < $5,000 → 通知 AP 人員\n🔴 紅燈：重複發票/重大異常 → 立刻阻斷，通知 AP 主管\n🟠 橙燈：格式不符 → 標註，需人工核查",
        "tools": ["T100_Invoice_Read", "Duplicate_Check"]
      }
    },
    {
      "name": "分支：燈號分級",
      "type": "n8n-nodes-base.switch",
      "position": [1250, 275],
      "parameters": {
        "dataType": "string",
        "value1": "{{ $json.alert_level }}",
        "rules": {
          "rules": [
            { "value2": "green", "output": 0 },
            { "value2": "yellow", "output": 1 },
            { "value2": "red", "output": 2 },
            { "value2": "orange", "output": 3 }
          ]
        }
      }
    },
    {
      "name": "自動通過 → 寫入 T100",
      "type": "n8n-nodes-base.httpRequest",
      "position": [1500, 100],
      "parameters": {
        "method": "POST",
        "url": "https://{{ $env.T100_HOST }}/api/aapt110/match",
        "body": "{{ $json.match_result }}"
      }
    },
    {
      "name": "Slack 通知 AP 人員（黃燈）",
      "type": "n8n-nodes-base.slack",
      "position": [1500, 250],
      "parameters": {
        "channel": "#ap-發票審核",
        "text": "🟡 發票需確認：{{ $json.invoice_no }} / {{ $json.vendor_name }} / 金額：{{ $json.total_amount }}"
      }
    },
    {
      "name": "Slack 緊急通知 AP 主管（紅燈）",
      "type": "n8n-nodes-base.slack",
      "position": [1500, 400],
      "parameters": {
        "channel": "#ap-緊急",
        "text": "🚨 緊急：發票異常，請立即處理！\n發票號：{{ $json.invoice_no }}\n供應商：{{ $json.vendor_name }}\n異常原因：{{ $json.exception_reason }}\n建議：阻斷付款，等待確認"
      }
    },
    {
      "name": "付款建議報告",
      "type": "n8n-nodes-base.slack",
      "position": [1750, 100],
      "parameters": {
        "channel": "#ap-付款",
        "text": "✅ 發票已驗證，待付款清單已更新\n- 發票號：{{ $json.invoice_no }}\n- 供應商：{{ $json.vendor_name }}\n- 金額：{{ $json.total_amount }}\n- 建議付款日：{{ $json.suggested_payment_date }}"
      }
    }
  ],
  "connections": {
    "Trigger: IMAP 接收發票": {
      "main": [[{ "node": "Agent 5: 發票解析智能體", "type": "main" }]]
    },
    "Trigger: PDF 上傳": {
      "main": [[{ "node": "Agent 5: 發票解析智能體", "type": "main" }]]
    },
    "Agent 5: 發票解析智能體": {
      "main": [[{ "node": "T100 交叉比對", "type": "main" }]]
    },
    "T100 交叉比對": {
      "main": [[{ "node": "AI 異常偵測引擎", "type": "main" }]]
    },
    "AI 異常偵測引擎": {
      "main": [[{ "node": "分支：燈號分級", "type": "main" }]]
    },
    "分支：燈號分級": {
      "main": [
        [{ "node": "自動通過 → 寫入 T100", "type": "main" }],
        [{ "node": "Slack 通知 AP 人員（黃燈）", "type": "main" }],
        [{ "node": "Slack 緊急通知 AP 主管（紅燈）", "type": "main" }],
        [{ "node": "Slack 通知 AP 人員（黃燈）", "type": "main" }]
      ]
    },
    "自動通過 → 寫入 T100": {
      "main": [[{ "node": "付款建議報告", "type": "main" }]]
    }
  }
}
```

---

## 11. 發票自動化年度效益估算

```
【發票自動化年度效益】

基於 AP 人工處理時間 + 錯誤成本：

╔═══════════════════════════╦═══════════╦═══════════════╗
║  效益項目               ║  年度效益   ║  說明          ║
╠═══════════════════════════╬═══════════╬═══════════════╣
║  人工 Key-in 時間節省  ║           ║               ║
║  （每張發票省 20 分鐘）║  $2.0M    ║  6,000張/年    ║
║  × $350/小時 × 20分   ║           ║  × 20分/張     ║
╠═══════════════════════════╬═══════════╬═══════════════╣
║  減少重複付款          ║           ║               ║
║  （AI 預防）           ║  $1.5M    ║  每年約3-5件   ║
║  每件平均 $300,000     ║           ║  × $300,000    ║
╠═══════════════════════════╬═══════════╬═══════════════╣
║  異常提前發現          ║           ║               ║
║  （減少對帳來回時間）  ║  $0.8M    ║  每月節省 80小時 ║
╠═══════════════════════════╬═══════════╬═══════════════╣
║  付款時間優化          ║           ║               ║
║  （現金流管理）         ║  $0.5M    ║  延後支付利息    ║
║                          ║           ║  節省           ║
╠═══════════════════════════╬═══════════╬═══════════════╣
║  年度總效益             ║  $4.8M    ║               ║
╚═══════════════════════════╩═══════════╩═══════════════╝

建置成本：Pilot 約 $200,000（獨立 Workflow，快速上線）
回收期：不到 2 個月
```

---

## 12. Agent 5 完整 Prompt 定義

```
【Agent 5 — 發票自動化智能體（AP Automation Agent）】

角色名稱：AP 發票自動化智能體
觸發時機：
  1. IMAP 接收到供應商發票 Email
  2. AP 人員上傳 PDF 發票
  3. T100 asft340 入庫完成（自動觸發待處理清單）

Own Skills：
├─ 發票解析（P-012）
├─ 預付款沖銷計算（P-013）
├─ 重複發票偵測（P-014）
├─ 付款時間優化
└─ 異常偵測與分類

系統 Prompt：
───────────────────────────────────────────
你是 AP 發票自動化智能體。你的工作是確保每一張發票都精準無誤。

【核心能力】

1. 發票解析
   - 接收任何格式的發票（PDF/Email/圖片/Excel）
   - LLM 解析後結構化輸出
   - 標註解析不確定的欄位

2. T100 交叉比對
   - 讀取 PO（apmt500）取得原始單價與數量
   - 讀取入庫（asft340）取得實際入庫數量
   - 讀取核價（axmt421）取得協議價格
   - 計算差異，判斷是否在容差範圍內

3. 預付款沖銷
   - 查詢 aapt310 該 PO 的預付款記錄
   - 計算：應付金額 = 發票金額 - 預付款沖銷

4. 重複發票偵測
   - 比對近 180 天所有歷史發票
   - 發現重複 → 立刻阻斷，通知 AP 主管

5. 異常分類與行動
   - 🟢 綠燈：自動通過，寫入 T100
   - 🟡 黃燈：通知 AP 人員，附上差異說明
   - 🔴 紅燈：立刻通知 AP 主管（電話 + Slack）
   - 🟠 橙燈：標註，需 AP 主管親自確認

6. 付款時間建議
   - 依據供應商等級給出付款日建議
   - 兼顧供應商關係 + 公司現金流

【禁止事項】
- 不得在未完成所有比對之前寫入 T100
- 不得對 🔴 紅燈發票執行任何付款動作
- 不得刪除任何歷史發票記錄
- 不得向外部透露任何供應商財務資訊
───────────────────────────────────────────
```

---

*文件版本：v1.0 | 維護者：AP 自動化專案團隊*
*最後更新：2026-03-25*
