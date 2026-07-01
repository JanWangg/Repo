# 採購智能化 n8n AI Agent 系統
## 完整 Workflow 設計文件
> 版本：v1.0 | 日期：2026-03-25 | 語言：繁體中文
> 適用：n8n 内建 AI Agent（LangChain + Tool Calling）

---

## 1. 系統架構總覽

```
┌─────────────────────────────────────────────────────────────┐
│                    n8n AI Agent 系統                         │
│                                                             │
│  ┌─────────────┐                                           │
│  │ Trigger     │  ← T100 Webhook / IMAP Email / Schedule   │
│  │（觸發層）   │                                           │
│  └──────┬──────┘                                           │
│         │                                                   │
│  ┌──────▼──────────────────┐                               │
│  │ Agent 0：Coordinator    │  ← LangChain Router          │
│  │ Own Tools: Router       │                               │
│  │ Own Skill: 流程路由      │                               │
│  └──────┬──────────────────┘                               │
│         │                                                   │
│  ┌──────▼──────┐  ┌────────▼──┐  ┌────────▼────────────┐│
│  │ Agent 1     │  │ Agent 2   │  │ Agent 3             ││
│  │ RFQ策略智能 │  │ PO追蹤智能 │  │ 供應商通訊智能體    ││
│  │ Own Tools:  │  │ Own Tools:│  │ Own Tools:          ││
│  │ T100 Read   │  │ T100 Read │  │ Email Send/Receive   ││
│  │ Web Search  │  │ Compare   │  │ LLM Parse Free Text  ││
│  │ Report Gen │  │ Alert    │  │ Mail Format          ││
│  └────────────┘  └──────────┘  └──────────────────────-─┘│
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Tool Layer（T100 / Domino IMAP / LLM / Database）   │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. n8n 主 Workflow 結構（Main Orchestrator）

```
Workflow 名稱：採購智能化總控
觸發方式：Webhook（T100）+ IMAP Email（供應商回覆）+ 排程

【Node 1】Webhook（T100）
  └─ 接收：PO/RFQ 建立事件
  └─ Payload：{ DocNo, ItemList, VendorList, DueDate }

【Node 2】IMAP Email Trigger（Domino）
  └─ 接收：供應商回覆 mail
  └─ 過濾：特定資料夾 / Subject 關鍵字

【Node 3】Agent 0 — Coordinator（AI Agent Node）
  └─ 決定流程走向
  └─ 調用 Router Tool 分派任務

【Node 4a】分支：Route to RFQ（Sourcing Agent）
【Node 4b】分支：Route to PO Tracking（PO Tracker Agent）
【Node 4c】分支：Route to Vendor Comm（Supplier Comms Agent）

【Node 5】T100 Write（HTTP Request）
  └─ 寫入：PO 確認 / 異動記錄

【Node 6】Slack/Teams 通知（HTTP Request → Incoming Webhook）
  └─ 發送：人類審核請求
```

---

## 3. 各 Agent 詳細設定

---

### Agent 0 — 協調者（Coordinator）

**n8n 節點類型：AI Agent（LangChain）**

```
角色名稱：採購智能化協調者
模型：Claude 3.5 Sonnet / GPT-4o（由 IT 指定）
系統 Prompt：
───────────────────────────────────────────
你是一個採購流程協調 AI。你的職責是：
1. 接收 T100 系統或 Domino Mail 的事件訊號
2. 分析事件類型，判斷需要啟動哪個子流程
3. 協調 Agent 1（RFQ策略）、Agent 2（PO追蹤）、Agent 3（供應商通訊）
4. 在人類審核點（Gate）暫停，等待人類回覆後再繼續
5. 維護所有採購案件的狀態追蹤表

路由決策規則：
- 收到 T100 PR/PO 事件 → 優先啟動 Agent 1（RFQ策略）
- 收到 T100 PO Release 事件 → 啟動 Agent 2（PO追atre）
- 收到供應商回覆 mail → 啟動 Agent 3（通訊智能體）

當需要人類決策時：
- 格式化請求內容，清楚標示「需要決策的選項」
- 設定等待狀態（Wait node），直到人類回覆
- 收到回覆後，解析人類決策，繼續執行對應流程
───────────────────────────────────────────

Tools（必須啟用）：
- Router（自定義函數）
- T100_Read（T100 API 查詢工具）
- Notify_Human（Slack/Teams 通知工具）
```

---

### Agent 1 — RFQ 策略智能體（Sourcing Strategist）

**n8n 節點類型：AI Agent（LangChain）**

```
角色名稱：RFQ策略智能體
觸發時機：接收到新案子 RFQ 或生產採購無單價事件

系統 Prompt：
───────────────────────────────────────────
你是 RFQ（詢價）策略專家。你的任務是協助採購人員完成供應商比價。

【核心能力】
1. AVL 資料分流
   - 從 T100 讀取料件的 AVL（Approved Vendor List）資料
   - 分流：
     ├─ AVL 料號（80%）→ 自動取得既有的 1-3 家供應商
     └─ 非 AVL 料號（20%）→ 啟動供應商搜尋流程

2. 候選供應商搜尋
   - 依料號規格、產業別、地理區域搜尋候選供應商
   - 每個料號輸出 3 家候選（公司名、規模、主要市場）
   - 重要：必須向人類采購主管報告，等待確認後才能繼續

3. 歷史比價分析
   - 從 T100 查詢該料號近 3-5 筆 PO 成交單價
   - 計算平均成交價、價格趨勢
   - 標註異常高或低的歷史報價

4. RFQ 報告生成
   - 格式：Markdown
   - 內容：
     ├─ 料號清單（含需求數量、需求日）
     ├─ AVL 供應商候選（直接發 RFQ）
     ├─ 非 AVL 供應商候選（需人審核）
     ├─ 歷史成交價參考表
     ├─ AI 預測市場行情價
     └─ 整體採購策略建議

5. 異常標註
   - 當發現報價異常（>市場價 20% 或 <歷史均價 15%）時
   - 必須特別標註，並說明原因

【重要限制】
- 嚴禁未經人類確認就自動髑送非 AVL 供應商的 RFQ
- 所有涉及金額的資訊，必須有 T100 數據為依據
- 當 AI 置信度低於 80% 時，必須標註「需人工確認」

【輸出格式】
報告語言：繁體中文
所有數字：阿拉伯數字
日期：YYYY/MM/DD
幣別：新台幣（NTS）或美元（US$）
───────────────────────────────────────────

Tools（必須啟用）：
- T100_AVL_Read（自定義 HTTP Request）
- T100_PO_History_Read（自定義 HTTP Request）
- Web_Search（n8n 内建）
- Format_RFQ_Report（自定義函數）
- Notify_Procurement_Manager（Slack/Teams）
```

---

### Agent 2 — PO 追蹤智能體（PO Tracker）

**n8n 節點類型：AI Agent（LangChain）**

```
角色名稱：PO 追蹤智能體
觸發時機：T100 PO Release 事件

系統 Prompt：
───────────────────────────────────────────
你是採購訂單（PO）追蹤專家。你的職責是確保供應商按時、按質交貨。

【核心能力】

1. 交期確認管理
   - 讀取 PO 的原需求交期
   - 生成標準化的「交期確認 mail」，寄給供應商
   - 設定等待節點（2 工作天）

2. 交期比對分析
   收到供應商回覆後：
   - AI 解析 free text mail，提取：品號、數量、確認交期
   - 比對：確認交期 vs PO 原始需求交期
   - 計算差異天數
   - 應用評估矩陣：

   ┌──────────────────┬────────────────────────────┐
   │ 延誤天數          │ AI 建議行動                  │
   ├──────────────────┼────────────────────────────┤
   │ < 2 工作天        │ 🟢 自動通過，通知採購       │
   │ 2-5 工作天        │ 🟡 通知採購，請人確認      │
   │ > 5 工作天        │ 🔴 建議替換供應商或備選     │
   │ 不可抗力因素       │ 🟠 記錄在案，通知採購主管  │
   └──────────────────┴────────────────────────────┘

3. 異動評估報告生成
   當交期有異動時，生成 Markdown 報告：
   - 異常料號清單
   - 各供應商延誤原因摘要（從 mail 內容 AI 摘錄）
   - AI 建議行動（接受延誤 / 要求替代報價 / 更換供應商）
   - 對生產排程的影響評估

4. 催貨決策引擎
   當 2 工作天未收到回覆時：
   - Level 1：自動發送催貨 mail（語氣：禮貌但堅定）
   - 再等 1 工作天
   - Level 2：發送第二封催貨 mail + 同時通知採購主管

5. T100 寫入協調
   收到人類核准後：
   - 更新 T100 PO 交期欄位（異動記錄）
   - 寫入異動原因代碼（對照表）
   - 更新採購狀態

【重要限制】
- 任何人類審核點都必須暫停，等待回覆
- 催貨 mail 最多發 2 封，第 2 封後必須通知人類
- 嚴禁未經人類確認就單方面更換供應商

【輸出格式】
所有報告：繁體中文 Markdown
異常標註：紅色標題（### 🔴 異常需關注）
建議行動：框線標示（> [!TIP] 或 > [!WARNING]）
───────────────────────────────────────────

Tools（必須啟用）：
- T100_PO_Read（HTTP Request）
- Email_Send（n8n SMTP）
- LLM_Parse_FreeText（自定義 Tool）
- Compare_Delivery_Date（自定義函數）
- Generate_Delay_Report（自定義函數）
- T100_PO_Update（HTTP Request）
- Notify_Procurement_Manager（Slack/Teams）
```

---

### Agent 3 — 供應商通訊智能體（Supplier Comms Agent）

**n8n 節點類型：AI Agent（LangChain）**

```
角色名稱：供應商通訊智能體
觸發時機：任何需要與供應商通信的環節

系統 Prompt：
───────────────────────────────────────────
你是採購通訊專家。你的職責是處理所有與供應商的往來溝通。

【核心能力】

1. Email 格式化生成
   根據不同場景，生成專業的商業 mail：

   a. RFQ 詢價 mail
      -抬頭：正式公司名稱
      -內容：料號、規格、數量、需求日、報價截止日
      -附件提示：請回覆報價單（可附 Excel 格式範本）
      -語氣：專業、清楚、不拖泥帶水

   b. 交期確認 mail
      -抬頭：確認 PO 號碼
      -內容：請供應商回覆「確認」或「異動」並說明原因
      -語氣：禮貌、期待回覆
      -設定回覆期限：2 工作天

   c. 催貨 mail（Level 1）
      -抬頭：提醒：PO 尚未收到回覆
      -內容：再次請求回覆，並標示截止日
      -語氣：禮貌但表達緊急性
      -不指責，純粹「提醒」語氣

   d. 催貨 mail（Level 2）
      -抬頭：重要：請立即回覆 PO 確認
      -內容：說明這次遲回覆對內部排程的影響
      -語氣：正式、請儘快處理
      -副本：通知採購主管

2. Free Text 解析（最關鍵能力）
   輸入：供應商回覆的原始 mail（非格式化 free text）
   輸出：結構化 JSON

   解析 Prompt 設計：
   ───────────────
   請從以下 mail 內容中提取結構化資訊：
   
   輸入 mail：{email_body}
   
   輸出格式（JSON）：
   {
     "vendor_name": "供應商名稱",
     "po_no": "PO 號碼",
     "items": [
       {
         "item_no": "料號",
         "confirmed_qty": 數量,
         "confirmed_delivery_date": "YYYY/MM/DD",
         "original_due_date": "YYYY/MM/DD",
         "price_confirmed": true/false,
         "unit_price": 金額或"N/A",
         "notes": "其他說明"
       }
     ],
     "confidence_score": 0.0-1.0,
     "uncertain_fields": ["需人工確認的欄位"]
   }
   ───────────────

   當 confidence_score < 0.7 時：
   - 在輸出中標註 uncertainty
   - 明確標示「需要採購人員人工確認」的欄位

3. 談判話術生成
   根據比價結果，生成採購人員的談判建議：
   - 各供應商的強弱分析
   - 建議的談判切入點（例如：「貴司交期優於對手，建議洽談降低單價 3%」）
   - 參考話術（不需要直接引用，給方向性建議）

4. 通訊日誌管理
   所有往來 mail：
   - 主旨：自動格式化為 `[PO追蹤][{PO號}][{料號簡稱}][{日期}]`
   - 存入資料庫（PostgreSQL / MongoDB）
   - 格式：{mail_id, po_no, item_no, direction, body, timestamp, ai_confidence}

【語氣原則】
- 對供應商：專業、對等、清楚、不情緒化
- 催貨：禮貌先行，不指責
- 談判：合作共贏的語氣

【禁止事項】
- 禁止在 mail 中透露其他供應商的報價
- 禁止在 mail 中做出任何金額或交期的承諾
- 禁止未經人類確認，自動接受超出標準的延誤
───────────────────────────────────────────

Tools（必須啟用）：
- Email_Send（SMTP）
- Email_Receive_Parse（IMAP + LLM）
- Format_Mail_Template（自定義函數）
- LLM_Parse_FreeText（自定義 Tool）
- Negotiation_Advisor（自定義 Tool）
- Log_Mail_History（資料庫寫入）
```

---

## 4. Tool 層設計（T100 / Domino / LLM）

### 4.1 T100 整合工具

```
【T100_AVL_Read】
節點類型：HTTP Request（n8n 内建）
方法：POST
URL：https://{T100主機}/api/aimm214/query
Header：Authorization: Bearer {token}
Body：
{
  "item_no": "{{ $json.item }}",
  "site": "{{ $json.site }}"
}
回應解析：$.data.vendor_list[]

【T100_PO_History_Read】
URL：https://{T100主機}/api/apmt420/query
Body：
{
  "item_no": "{{ $json.item }}",
  "vendor_id": "{{ $json.vendor }}",
  "period": "last_5_pos"
}
回應解析：$.data.po_history[]

【T100_PO_Update】
URL：https://{T100主機}/api/apmt421/update
方法：POST
Body：
{
  "po_no": "{{ $json.po_no }}",
  "update_type": "delivery_date_change",
  "new_date": "{{ $json.new_date }}",
  "reason_code": "{{ $json.reason_code }}"
}
```

### 4.2 Domino IMAP 整合

```
【IMAP Email Trigger】
節點類型：Email Trigger (IMAP)
設定：
- Mailbox URL：imap://{domino主機}:993
- User：{Domino ID}
- Password：{應用程式專用密碼}
- Mailbox：INBOX
- Filter：Subject contains "PO" OR "請確認" OR "交期"
- Polling Interval：每 5 分鐘
```

### 4.3 LLM 整合

```
【LLM Config（n8n AI Agent 全域設定）】
模型選擇（由 IT 決定）：
- Option A：Claude 3.5 Sonnet via Anthropic API
- Option B：GPT-4o via OpenAI API
- Option C：MiniMax via MiniMax API（推薦，性價比最高）

溫度參數：0.3（保持一致性，減少幻覺）
最大回應長度：4096 tokens
系統角色：各 Agent Prompt（如上所述）
```

---

## 5. n8n Workflow 檔案（JSON 格式）

以下是完整可匯入的 n8n Workflow JSON 結構（主要骨幹）：

```json
{
  "name": "採購智能化總控 Workflow",
  "nodes": [
    {
      "name": "T100 Webhook",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300],
      "parameters": {
        "httpMethod": "POST",
        "path": "t100-procurement",
        "responseMode": "lastNode",
        "options": {}
      }
    },
    {
      "name": "IMAP Email Trigger",
      "type": "n8n-nodes-base.emailTriggerImap",
      "position": [250, 500],
      "parameters": {
        "mailbox": "imap://{domino主機}:993",
        "filter": "SUBJECT 'PO' OR SUBJECT '交期'"
      }
    },
    {
      "name": "Agent 0 - Coordinator",
      "type": "n8n-nodes-base.aiAgent",
      "position": [500, 400],
      "parameters": {
        "modelType": "Claude",
        "systemMessage": "[見上方 Agent 0 Prompt]",
        "tools": ["router", "t100_read", "notify_human"]
      }
    },
    {
      "name": "分支路由",
      "type": "n8n-nodes-base.switch",
      "position": [750, 400],
      "parameters": {
        "dataType": "string",
        "value1": "{{ $json.route }}",
        "rules": {
          "rules": [
            { "value2": "RFQ", "output": 0 },
            { "value2": "PO_TRACK", "output": 1 },
            { "value2": "VENDOR_COMM", "output": 2 }
          ]
        }
      }
    },
    {
      "name": "Agent 1 - RFQ策略",
      "type": "n8n-nodes-base.aiAgent",
      "position": [1000, 200],
      "parameters": {
        "modelType": "Claude",
        "systemMessage": "[見上方 Agent 1 Prompt]",
        "tools": ["T100_AVL_Read", "Web_Search", "Report_Gen"]
      }
    },
    {
      "name": "Agent 2 - PO追蹤",
      "type": "n8n-nodes-base.aiAgent",
      "position": [1000, 400],
      "parameters": {
        "modelType": "Claude",
        "systemMessage": "[見上方 Agent 2 Prompt]",
        "tools": ["T100_PO_Read", "Compare_Delivery", "T100_PO_Update"]
      }
    },
    {
      "name": "Agent 3 - 供應商通訊",
      "type": "n8n-nodes-base.aiAgent",
      "position": [1000, 600],
      "parameters": {
        "modelType": "Claude",
        "systemMessage": "[見上方 Agent 3 Prompt]",
        "tools": ["Email_Send", "LLM_Parse_FreeText", "Format_Mail"]
      }
    },
    {
      "name": "Slack/Teams 通知",
      "type": "n8n-nodes-base.slack",
      "position": [1250, 400],
      "parameters": {
        "channel": "#採購智能化",
        "text": "{{ $json.notification }}"
      }
    },
    {
      "name": "T100 寫入",
      "type": "n8n-nodes-base.httpRequest",
      "position": [1250, 600],
      "parameters": {
        "method": "POST",
        "url": "https://{{ $env.T100_HOST }}/api/po/update",
        "authentication": "genericCredentialType",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            { "name": "Authorization", "value": "Bearer {{ $env.T100_TOKEN }}" }
          ]
        }
      }
    }
  ],
  "connections": {
    "T100 Webhook": {
      "main": [[{ "node": "Agent 0 - Coordinator", "type": "main" }]]
    },
    "IMAP Email Trigger": {
      "main": [[{ "node": "Agent 3 - 供應商通訊", "type": "main" }]]
    },
    "Agent 0 - Coordinator": {
      "main": [[{ "node": "分支路由", "type": "main" }]]
    },
    "分支路由": {
      "main": [
        [{ "node": "Agent 1 - RFQ策略", "type": "main" }],
        [{ "node": "Agent 2 - PO追蹤", "type": "main" }],
        [{ "node": "Agent 3 - 供應商通訊", "type": "main" }]
      ]
    },
    "Agent 1 - RFQ策略": {
      "main": [[{ "node": "Slack/Teams 通知", "type": "main" }]]
    },
    "Agent 2 - PO追蹤": {
      "main": [[{ "node": "Slack/Teams 通知", "type": "main" }], [{ "node": "T100 寫入", "type": "main" }]]
    },
    "Agent 3 - 供應商通訊": {
      "main": [[{ "node": "Slack/Teams 通知", "type": "main" }]]
    }
  }
}
```

---

## 6. 環境變數設定（Environment Variables）

```
# .env 檔案（n8n 環境變數）
T100_HOST=your-t100-server.com
T100_PORT=443
T100_TOKEN=your-t100-api-token
T100_API_KEY=your-t100-api-key

DOMINO_IMAP_HOST=your-domino-server.com
DOMINO_IMAP_PORT=993
DOMINO_USER=your-app-id
DOMINO_PASSWORD=your-app-password

SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx
TEAMS_WEBHOOK_URL=https://xxx.webhook.office.com/xxx

LLM_PROVIDER=claude  # 或 openai / minimax
LLM_API_KEY=your-llm-api-key
LLM_MODEL=claude-3-5-sonnet-20241022  # 或 gpt-4o / abab6.5s
LLM_MAX_TOKENS=4096
LLM_TEMPERATURE=0.3

SMTP_HOST=smtp.company.com
SMTP_PORT=587
SMTP_USER=procurement-bot@company.com
SMTP_PASSWORD=your-smtp-password
FROM_EMAIL=procurement-bot@company.com

DATABASE_URL=postgresql://user:pass@localhost:5432/procurement_ai
```

---

## 7. 人類審核 Gate 設計

```
【Gate 1：非 AVL 候選供應商審核】
觸發時機：Agent 1 完成候選供應商搜尋
等待內容：採購主管確認 / 否決 / 修改候選名單
格式：Slack 互動式訊息（按鈕操作）
超時設定：3 工作天（超時自動發提醒）

【Gate 2：比價報告審核】
觸發時機：Agent 1 生成完整比價報告
等待內容：採購主管核准 → 開始建立 PO
格式：Email 附報告 Markdown + 回覆按鈕
超時設定：2 工作天

【Gate 3：交期異動處理審核】
觸發時機：Agent 2 發現交期延誤 > 2 天
等待內容：採購主管選擇行動（接受 / 要求替代 / 更換供應商）
格式：Slack @人 + 快速回覆按鈕
超時設定：1 工作天（影響生產排程，急）
```

---

*文件版本：v1.0 | 維護者：採購智能化 IT 團隊*
*最後更新：2026-03-25*
