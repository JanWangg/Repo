# 委外管理 AI 智能體設計方案
## Phase 2 核心模組
> 版本：v1.0 | 日期：2026-03-25 | 語言：繁體中文
> 依據：T100 系統手冊 + 資材總處組織架構 V6 + AOP 實際數據

---

## 1. 委外現況與瓶頸分析

### 1.1 AOP 數據（實際數值）

```
委外 OTD NBD：56%（目標 90%，落後 34pp）🔴
年委外工單數：139,868 件
委外 OTD 落後幅度：最大痛點（比 PO OTD 落後幅度大 10x）

QC 驗退比例：1%（穩定）
PR→PO ≤2天：98.9%（已達標）
Cost Reduction：0.75%（已超標）
```

### 1.2 委外流程全鏈路瓶頸地圖

```
委外 OTD 56% 的根因分解：

  工單建立(asft300)遲
         │
  Vendor 不回覆確認 mail
         │
  交期異動沒人追蹤
         │
  實際完工落後預定日
         │
  入庫延遲 → OTD 未達

【核心問題】：沒有自動追蹤機制，完全靠人工盯
```

---

## 2. 委外 AI Agent（Agent 4）設計

### Agent 4 — 委外管理智能體（Outsourcing Agent）

**n8n 節點類型：AI Agent（LangChain）**

```
角色名稱：委外管理智能體
觸發時機：
  1. axmt421 委外核價單建立
  2. asft300 工單 Release
  3. 供應商回覆 mail（IMAP）
  4. aqct300 QC 結果出爐
  5. aapt110 對帳資料

 Own Skills：
 ├─ 委外交期追蹤器
 ├─ QC 結果解讀師
 ├─ 委外核價助理
 └─ 對帳審核師
```

---

## 3. 委外專用 Workflow（完整設計）

### 3.1 觸發點與流程圖

```
┌─────────────────────────────────────────────────────────────────┐
│                委外管理 AI Workflow                              │
│                                                                 │
│  【觸發點 1】              【觸發點 2】                       │
│  axmt421 核價單建立  ────→  asft300 工單 Release              │
│         │                           │                           │
│         ▼                           ▼                           │
│  AI 帶出歷史核價              AI 發送「加工完成日              │
│  + 建議區間                     確認 mail」                      │
│         │                           │                           │
│         │                      Wait 2 工作天                    │
│         │                           │                           │
│         │              ┌────────────┴────────────┐              │
│         │              ▼                          ▼              │
│         │      【有回覆】                 【無回覆】            │
│         │              │                          │              │
│         │              ▼                          ▼              │
│         │      AI 解析 free text              催供 mail #1     │
│         │      提取：加工完成預定日              ↓               │
│         │              │                   Wait 1 工作天        │
│         │              ▼                          │              │
│         │      比對：加工完成日                   ▼              │
│         │         vs 需求日                催供 mail #2         │
│         │              │                   + 通知主管          │
│         │    ┌────────┴────────┐               │              │
│         │    ▼                 ▼               │              │
│         │  符合              延誤               │              │
│         │  更新T100          AI 異動報告        │              │
│         │                    人決定             │              │
│         │                      │                 │              │
│         └──────────────────────┴─────────────────┘              │
│                              │                                   │
│                              ▼                                   │
│                     【aqct300 QC 結果】                          │
│                              │                                   │
│                    AI 解讀 QC 結果                              │
│                    ├─ 允收 → 更新 T100 完工日                   │
│                    └─ 驗退（1%）→ 重算實際完工日               │
│                              │                                   │
│                              ▼                                   │
│                     【aapt110 對帳】                            │
│                              │                                   │
│                    AI 比對加工費 vs 報價                        │
│                    └─ 異常 → 對帳差異報告                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. 各據點供應商管理設計

### 4.1 獨立供應商名單（按據點）

```
【供應商資料庫設計】

每個據點有獨立的供應商名單（Vendor Master）：

┌──────────────┬──────────────────────────────────────────────┐
│ 據點         │ 委外類型            │ 供應商管理重點        │
├──────────────┼────────────────────┼──────────────────────┤
│ 松江         │ 大機加、鈑金、小機加 │ 機械加工供應商       │
│ 昆山         │ 大機加、鈑金、小機加 │ 電子件/精密加工      │
│ 泰國（RY）   │ 組裝、機構件        │ 當地供應商           │
│ 泰國（CBR）  │ 組裝、包材          │ 當地供應商           │
└──────────────┴────────────────────┴──────────────────────┘

【Vendor Master 資料欄位】

{
  "vendor_id": "V001",
  "vendor_name": "○○機械有限公司",
  "site": "松江",              ← 必填，區分據點
  "type": "大機加",            ← 大機加/鈑金/小機加/組裝
  "contact_email": "xxx@xxx.com",
  "payment_terms": "月結30",
  "otd_score": 0.85,           ← AI 計算的 OTD 分數
  "quality_score": 0.99,        ← AI 計算的良品率分數
  "avg_lead_time_days": 7,      ← 平均加工交期
  "total_orders_2025": 342,
  "total_amount_2025": 12500000,
  "notes": "擅長鋁件加工，交期穩定"
}

【AI 供應商評分機制】

OTD 分數 = 準時完工件數 / 總件數
品質分數 = 良品件數 / 送驗件數
綜合分數 = OTD分數×60% + 品質分數×40%

分級：
  A級（≥90分）：優先发单，配合意願高
  B級（70-89分）：正常发单
  C級（<70分）：列入觀察，減少订单
  D級（<50分）：建議更換供應商
```

---

## 5. T100 委外模組串接設計

### 5.1 T100 委外 API 端點

```
【委外專用 API 端點】

基礎 URL：https://{T100主機}:{T100_PORT}/t100api/

─────────────────────────────────────────────────────────────
核價資料查詢（axmt421）
GET /api/axmt421/query
參數：mo_no, item_no, vendor_id, site
回應：{ "pricing_records": [...], "last_price": ..., "price_trend": "up/down/stable" }

─────────────────────────────────────────────────────────────
工單資料查詢（asft300）
GET /api/asft300/query
參數：mo_no, status, site, release_date_from, release_date_to
回應：{
  "mo_list": [{
    "mo_no": "工單號",
    "item_no": "料號",
    "item_desc": "品名",
    "qty": 數量,
    "site": "據點",
    "vendor_id": "供應商代碼",
    "vendor_name": "供應商名稱",
    "vendor_email": "供應商Email",
    "release_date": "Release 日期",
    "required_completion_date": "需求完工日",
    "current_status": "released/in_progress/completed"
  }]
}

─────────────────────────────────────────────────────────────
QC 結果查詢（aqct300）
GET /api/aqct300/query
參數：mo_no, inspection_date_from, inspection_date_to
回應：{
  "inspection_records": [{
    "mo_no": "工單號",
    "item_no": "料號",
    "qty_submitted": 送驗數量,
    "qty_accepted": 允收數量,
    "qty_rejected": 驗退數量,
    "rejection_rate": 0.01,
    "result": "accept/reject/partial",
    "inspection_date": "檢驗日期",
    "inspector": "檢驗員"
  }]
}

─────────────────────────────────────────────────────────────
完工入庫資料（asft340）
GET /api/asft340/query
參數：mo_no, completion_date
回應：{
  "completion_records": [{
    "mo_no": "工單號",
    "actual_completion_date": "實際完工日",
    "qty_completed": 完工數量,
    "warehouse": "入庫倉庫"
  }]
}

─────────────────────────────────────────────────────────────
對帳資料（aapt110）
GET /api/aapt110/query
參數：vendor_id, period, site
回應：{
  "invoices": [{
    "invoice_no": "發票號",
    "mo_no": "工單號",
    "vendor_id": "供應商代碼",
    "invoice_amount": 發票金額,
    "po_amount": PO 金額,
    "variance": 差異金額,
    "status": "matched/mismatched/pending"
  }]
}

─────────────────────────────────────────────────────────────
工單交期更新（寫入）
POST /api/asft300/update_delivery
Body：{
  "mo_no": "工單號",
  "new_completion_date": "新完工日",
  "reason_code": "D01/D02/D03...",
  "updated_by": "AI",
  "update_timestamp": "ISO8601"
}
```

---

## 6. n8n 委外 Workflow JSON（骨幹）

```json
{
  "name": "委外管理 AI Workflow",
  "nodes": [
    {
      "name": "Trigger 1: axmt421 核價單 Webhook",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 100],
      "parameters": {
        "path": "t100-outsourcing-pricing",
        "httpMethod": "POST"
      }
    },
    {
      "name": "Trigger 2: asft300 工單 Release Webhook",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 250],
      "parameters": {
        "path": "t100-outsourcing-mo",
        "httpMethod": "POST"
      }
    },
    {
      "name": "Trigger 3: IMAP Vendor 回覆",
      "type": "n8n-nodes-base.emailTriggerImap",
      "position": [250, 400],
      "parameters": {
        "mailbox": "imap://{domino主機}:993",
        "filter": "SUBJECT '加工' OR SUBJECT '完成' OR SUBJECT '委外'"
      }
    },
    {
      "name": "Trigger 4: aqct300 QC 結果（排程）",
      "type": "n8n-nodes-base.scheduleTrigger",
      "position": [250, 550],
      "parameters": {
        "rule": {"interval": [{"field": "minutes", "intervals": [30]}]}
      }
    },
    {
      "name": "Agent 4: 委外管理智能體",
      "type": "n8n-nodes-base.aiAgent",
      "position": [500, 300],
      "parameters": {
        "modelType": "Claude",
        "systemMessage": "你是委外管理智能體。收到 T100 事件或 Vendor 回覆 mail 時：\n1. axmt421 觸發 → 查歷史核價 + 給建議區間\n2. asft300 觸發 → 立刻發送加工完成日確認 mail\n3. Vendor 回覆 → 解析 free text → 比對需求日\n4. QC 結果 → 更新完工日預測\n5. 對帳 → 比對金額差異\n\n所有異常（延誤/驗退/差異）必須立刻通知採購主管。",
        "tools": [
          "T100_Outsourcing_Read",
          "T100_MO_Update",
          "T100_QC_Read",
          "Email_Send_Vendor",
          "LLM_Parse_FreeText",
          "Vendor_DB_Read",
          "Vendor_DB_Write",
          "Notify_Procurement_Manager"
        ]
      }
    },
    {
      "name": "Vendor Mail Send",
      "type": "n8n-nodes-base.sendEmail",
      "position": [750, 200],
      "parameters": {
        "to": "{{ $json.vendor_email }}",
        "subject": "請確認委外加工完成日【{{ $json.mo_no }}】- {{ $json.site }}據點",
        "body": "{{ $json.mail_body }}"
      }
    },
    {
      "name": "催供 Mail Level 1",
      "type": "n8n-nodes-base.sendEmail",
      "position": [750, 350],
      "parameters": {
        "subject": "【提醒】尚未收到加工完成日回覆【{{ $json.mo_no }}】"
      }
    },
    {
      "name": "催供 Mail Level 2 + 通知主管",
      "type": "n8n-nodes-base.sendEmail",
      "position": [750, 500],
      "parameters": {
        "subject": "【重要】請立即回覆加工完成日【{{ $json.mo_no }}】",
        "cc": "{{ $json.buyer_email }}"
      }
    },
    {
      "name": "Slack 異動通知",
      "type": "n8n-nodes-base.slack",
      "position": [1000, 300],
      "parameters": {
        "channel": "#委外管理",
        "text": "{{ $json.alert_message }}"
      }
    },
    {
      "name": "T100 完工日更新",
      "type": "n8n-nodes-base.httpRequest",
      "position": [1000, 450],
      "parameters": {
        "method": "POST",
        "url": "https://{{ $env.T100_HOST }}/api/asft300/update_delivery"
      }
    },
    {
      "name": "Vendor 評分更新",
      "type": "n8n-nodes-base.n8nNodesBaseMongoDb",
      "position": [1000, 600],
      "parameters": {
        "operation": "update",
        "collection": "vendor_master",
        "filter": "{ vendor_id: '{{ $json.vendor_id }}' }",
        "update": "{{ $json.vendor_score_update }}"
      }
    }
  ],
  "connections": {
    "Trigger 1: axmt421 核價單 Webhook": {
      "main": [[{ "node": "Agent 4: 委外管理智能體", "type": "main" }]]
    },
    "Trigger 2: asft300 工單 Release Webhook": {
      "main": [[{ "node": "Agent 4: 委外管理智能體", "type": "main" }], [{ "node": "Vendor Mail Send", "type": "main" }]]
    },
    "Trigger 3: IMAP Vendor 回覆": {
      "main": [[{ "node": "Agent 4: 委外管理智能體", "type": "main" }]]
    },
    "Trigger 4: aqct300 QC 結果（排程）": {
      "main": [[{ "node": "Agent 4: 委外管理智能體", "type": "main" }]]
    },
    "Agent 4: 委外管理智能體": {
      "main": [[{ "node": "Slack 異動通知", "type": "main" }], [{ "node": "T100 完工日更新", "type": "main" }], [{ "node": "Vendor 評分更新", "type": "main" }]]
    }
  }
}
```

---

## 7. 委外交期異動判斷矩陣（新增）

```
【委外專用交期異動矩陣】

委外 OTD 的「交期」定義：加工完成日（不是入庫日）

╔═══════════════════╦═══════════════════════════════════╗
║  延誤天數         ║  AI 行動                          ║
╠═══════════════════╬═══════════════════════════════════╣
║  < 2 工作天        ║  🟢 自動通過，更新 T100          ║
║  2-5 工作天        ║  🟡 AI 標註，通知採購，請確認   ║
║  5-10 工作天       ║  🔴 通知採購主管，建議聯繫工廠  ║
║  > 10 工作天       ║  🚨 建議評估替代供應商，列入 C/D ║
║  不可抗力          ║  🟠 記錄在案，計算實際完工日     ║
╚═══════════════════╩═══════════════════════════════════╝

【QC 驗退（1%）處理流程】

aqct300 結果為「驗退」時：
Step 1：AI 讀取 aqct300 驗退記錄
Step 2：AI 計算「實際完工日」= 驗退日 + 重工天數估算
Step 3：若影響客户交期 → 即時通知採購
Step 4：重工完成後，重新跑一次這個 Workflow
Step 5：更新該供應商的「品質分數」
```

---

## 8. 各據點據點隔離設計

```
【據點隔離原則】

每個據點（松江/昆山/泰國 RY/泰國 CBR）的：
  - 供應商名單 → 各自獨立，互不影響
  - 工單 → 按 site 區分
  - 催供 Mail → 分別發給各自據點的採購窗口

【各據點專屬參數】

{
  "site_configs": {
    "松江": {
      "site_code": "SJ",
      "vendor_list": "vendor_master_sj",
      "buyer_email": "buyer-sj@company.com",
      "mo_prefix": "SJM",
      "timezone": "Asia/Shanghai",
      "working_days": [1,2,3,4,5]  // 中國工作日
    },
    "昆山": {
      "site_code": "KS",
      "vendor_list": "vendor_master_ks",
      "buyer_email": "buyer-ks@company.com",
      "mo_prefix": "KSM",
      "timezone": "Asia/Shanghai",
      "working_days": [1,2,3,4,5]
    },
    "泰國_RY": {
      "site_code": "RY",
      "vendor_list": "vendor_master_ry",
      "buyer_email": "buyer-ry@company.com",
      "mo_prefix": "RYM",
      "timezone": "Asia/Bangkok",
      "working_days": [1,2,3,4,5,6]  // 泰國六工
    },
    "泰國_CBR": {
      "site_code": "CBR",
      "vendor_list": "vendor_master_cbr",
      "buyer_email": "buyer-cbr@company.com",
      "mo_prefix": "CBRM",
      "timezone": "Asia/Bangkok",
      "working_days": [1,2,3,4,5,6]
    }
  }
}
```

---

## 9. 委外 AI 年度效益估算（更新版）

```
【委外 AI 年度總效益】

基於 AOP 數據（委外 OTD 56%，目標 90%）+ QC 驗退 1%：

╔═══════════════════════════╦═══════════╦═══════════╗
║  效益項目                 ║  基準     ║  說明    ║
╠═══════════════════════════╬═══════════╬═══════════╣
║  委外 OTD 改善            ║           ║          ║
║  （56%→70%，改善14pp）    ║  $97.9M  ║  19,581件  ║
║  每件委外延誤成本 $5,000   ║           ║  × $5,000 ║
╠═══════════════════════════╬═══════════╬═══════════╣
║  QC 驗退提前發現           ║           ║          ║
║  （1%×139,868=1,399件）   ║  $1.4M   ║  每件節省  ║
║  提前 1 天發現並重工        ║           ║  $1,000   ║
╠═══════════════════════════╬═══════════╬═══════════╣
║  委外核價談判支持          ║           ║          ║
║  Cost Reduction 0.75→0.9%║  $11.8M  ║  +0.15%×  ║
║                            ║           ║  $7.87B   ║
╠═══════════════════════════╬═══════════╬═══════════╣
║  AI 節省人工處理時間       ║           ║          ║
║  （工單追蹤+催供+對帳）    ║  $3.5M   ║  1,000小時║
║                            ║           ║  × $3,500 ║
╠═══════════════════════════╬═══════════╬═══════════╣
║  年度總效益               ║  $114.6M  ║  基準     ║
║  保守（50%）              ║  $57.3M   ║  打五折   ║
║  樂觀                    ║  $171.9M  ║          ║
╚═══════════════════════════╩═══════════╩═══════════╝

委外 OTD 是最大單一效益（84%），遠超其他三項。
```

---

*文件版本：v1.0 | 維護者：委外管理 AI 專案團隊*
*最後更新：2026-03-25*
