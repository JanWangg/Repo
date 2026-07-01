# 採購智能化全景圖 v2.0
## T100 × n8n AI 完整流程對照
> 版本：v2.0 | 日期：2026-03-25 | 語言：繁體中文
> 依據：T100 ERP 系統手冊 + 資材總處組織架構 V6 + AOP 數據

---

## v1.0 vs v2.0 差異說明

```
v1.0：僅涵蓋採購 PO + 委外
v2.0：完整覆蓋採購、委外、核價、RFQ、倉庫五大模組

新增內容：
  ├─ 核價流程（axmt420/axmt421）
  ├─ RFQ 流程（axmt410/axmt400/aooi084）
  ├─ 倉庫入庫流程（asft311/asft340/aint302）
  ├─ 全部 T100 API 端點對照
  └─ 全部 AI 介入點對照
```

---

## 1. 完整採購循環全景圖

```
╔════════════════════════════════════════════════════════════════════════╗
║                    T100 採購完整循環（6 大模組）                         ║
║                                                                        ║
║  ┌────────────┐     ┌────────────┐     ┌────────────┐                ║
║  │  模組一    │     │  模組二    │     │  模組三    │                ║
║  │ aimm214   │ ──▶ │ axmt421   │ ──▶ │ axmt410   │                ║
║  │ 採購基礎  │     │ 核價單    │     │ RFQ報價   │                ║
║  │ 資料維護  │     │           │     │           │                ║
║  └────────────┘     └────────────┘     └─────┬──────┘                ║
║                                              │                        ║
║  ┌────────────┐     ┌────────────┐     ┌─────▼──────┐              ║
║  │  模組四    │ ◀── │  模組五    │ ◀── │  模組六    │              ║
║  │ asft340   │     │ aqct300   │     │ apmt500   │              ║
║  │ 進貨入庫  │     │ IQC/FQC   │     │ 採購單PO  │              ║
║  │ 倉庫發收  │     │ 品質檢驗  │     │ 採購維護  │              ║
║  └─────┬──────┘     └─────┬──────┘     └─────┬──────┘              ║
║        │                    │                   │                    ║
║        ▼                    ▼                   ▼                    ║
║  ┌──────────────────────────────────────────────────────┐            ║
║  │  模組七：aapt110 應付帳款（對帳/發票匹配）            │            ║
║  └──────────────────────────────────────────────────────┘            ║
╚════════════════════════════════════════════════════════════════════════╝

【AI 介入點全景圖】

 AI 可全鏈路介入，覆蓋：
   ✓ 核價談判（axmt421）  → AI 歷史比價 + 建議區間
   ✓ RFQ 發送（axmt410） → AI 生成報價單 mail
   ✓ PO 建立（apmt500）   → AI 自動分流 + 發送供應商
   ✓ IQC 結果（aqct300） → AI 入庫預測 + 延誤預警
   ✓ 完工入庫（asft340）  → AI 更新完工日
   ✓ 應付帳款（aapt110）  → AI 發票匹配異常偵測
```

---

## 2. 模組一：採購基礎資料（aimm214）

### 2.1 模組職責

```
目的：定義料件的採購屬性，確保全球據點作業一致
範圍：台灣、中國（松江/昆山）、泰國（RY/CBR）
主要作業：aimm214（據點採購資料維護）

ai 介入點：在建立 PO 前，AI 需讀取此資料
```

### 2.2 T100 API 端點

```
【aimm214 — 據點採購資料查詢】
GET /api/aimm214/query
參數：item_no, site
回應：
{
  "item_no": "料號",
  "item_desc": "品名",
  "site": "據點",
  "buyer": "採購員",
  "purchasing_group": "採購分群碼",   ← AI 用於分流
  "vendor_id": "主要供應商",
  "vendor_name": "供應商名稱",
  "vendor_email": "供應商 Email",       ← AI 直接取用
  "uom": "計價單位",
  "min_order_qty": 最小採購量,
  "vendor_selection_mode": 0/1/2,      ← AI 分流依據
  "price_tolerance": 容差率,
  "lead_time_days": 供貨週期
}

【AI 應用：自動帶出 PO 預設資訊】
當 Agent 1 建立 PO 時：
→ AI 自動讀取 aimm214
→ 帶出：供應商、Email、計價單位、最小採購量
→ 減少採購人員 Key-in 錯誤
```

### 2.3 採購分群碼對照（AI 分流依據）

```
【採購分群碼 → AI 分流邏輯】

分群碼          說明              AI 分流策略
─────────────────────────────────────────────────────────────
PG-RAW        原料              → AVL 供應商優先，AI 快速確認
PG-SEMI       半成品            → 可能涉及委外，AI 轉 Agent 4
PG-ASSY       組裝件            → BOM 比對，AI 檢查 BOM 完整性
PG-MRO        維修件            → 通常緊急，AI 標註「優先處理」
PG- Outs      委外加工件         → 轉 Agent 4（委外管理智能體）
PG-OTHER      其他               → 人員確認後再分流
```

---

## 3. 模組二：核價流程（axmt420 / axmt421）

### 3.1 模組職責

```
目的：與供應商商議核定價格，寫入核價檔
主要作業：
  axmt420：採購核價（針對採購料件）
  axmt421：委外核價（針對委外加工）

AI 介入點：核價談判前 → AI 帶出歷史核價 + 市場行情建議
```

### 3.2 T100 核價狀態機

```
╔═══════════════════════════════════════════════════╗
║           核價單狀態機                            ║
║                                                   ║
║  N（未審核）──【審核】──▶ Y（已審核）           ║
║      │                        │                   ║
║      │【修改】                │【取消審核】        ║
║      ▼                        ▼                   ║
║  N（可改）◀──────【取消審核】─── Y（已寫入）    ║
║                                                   ║
║  X（作廢）                                       ║
╚═══════════════════════════════════════════════════╝

AI 介入點：
  → 狀態 N → AI 計算「建議核價區間」
  → 狀態 Y → AI 記錄談判結果，更新談判歷史資料庫
```

### 3.3 AI 核價助理（新增能力）

```
【核價談判支援工作流】

觸發：AI 發現以下情况時，自動啟動核價支援：

情況 1：上次核價已超過 90 天
  → AI 主動提醒：「料號 XXX 核價即將到期，建議重新議價」

情況 2：市場行情與核價差異 > 10%
  → AI 標註：「市場行情已上漲 12%，建議啟動重新核價」

情況 3：供應商主動提出調漲
  → AI 自動查詢歷史核價 + 近 3 次成交價
  → AI 生成「議價策略建議報告」

【AI 核價建議 Prompt】

輸入：
  料號：{item_no}
  上次核價：{last_price}
  上次核價日期：{last_date}
  近 3 次成交價：{recent_prices[]}
  市場行情參考：{market_price}
 採購數量：{qty}

任務：計算建議核價區間

輸出：
{
  "suggested_price_range": {
    "conservative": 保守價,
    "target": 目標價,
    "stretch": 極限價
  },
  "reasoning": "計算邏輯說明",
  "negotiation_leverage": "談判切入點建議",
  "risk_factors": ["風險因素"]
}
```

### 3.4 T100 API 端點

```
【axmt421 — 委外核價查詢】
GET /api/axmt421/query
參數：mo_no, item_no, vendor_id, site
回應：
{
  "pricing_records": [{
    "pricing_no": "核價單號",
    "item_no": "料號",
    "vendor_id": "供應商",
    "site": "據點",
    "unit_price": 單價,
    "currency": "TWD/USD",
    "effective_date": 生效日,
    "expiry_date": 到期日,
    "status": "N/Y/X",
    "qty_breaks": [
      { "min_qty": 1, "max_qty": 100, "price": 100 },
      { "min_qty": 101, "max_qty": null, "price": 95 }
    ],
    "last_transaction_price": 上次成交價,
    "price_trend": "up/stable/down"
  }]
}

【核價到期預警查詢】
GET /api/axmt421/expiring
參數：site, days_ahead（如 30）
回應：即將到期的核價單清單
→ AI 自動觸發重新議價流程
```

---

## 4. 模組三：RFQ 流程（axmt410 / axmt400 / aooi084）

### 4.1 模組職責

```
目的：供應商報價回來後，轉為核價依據
主要作業：
  axmt400：銷售估價單（引用 BOM 估算成本）
  axmt410：銷售報價單（正式報價給客戶）

AI 介入點（採購端）：
  → 接收供應商 RFQ 回覆（IMAP）
  → AI 解析 free text 報價
  → 寫入 aooi084（採購價格參照表）
  → 進入核價流程（axmt421）
```

### 4.2 AI 在 RFQ 流程中的角色

```
【AI 輔助的 RFQ 完整工作流】

Step 1：需求建立
  ├─ 來源 1：Sales 接單 → 觸發採購需求
  ├─ 來源 2：MRP 計劃 → 自動產生 PR
  └─ 來源 3：庫存低於安全量 → 自動觸發請購

Step 2：AI 分流（Agent 1）
  ├─ 讀取 aimm214 → AVL 供應商？
  ├─ AVL 料（80%）→ 直接進 RFQ 流程
  └─ 非 AVL（20%）→ AI 搜尋候選供應商 → 人確認

Step 3：AI 生成詢價 mail
  ├─ 讀取 aooi084（採購價格參照表）
  ├─ 讀取 axmt421 歷史核價
  ├─ AI 生成 RFQ mail（含料號、規格、数量、截止日）
  └─ n8n Email 髑送（控制頻率：每批 20-30 封）

Step 4：供應商回覆（IMAP）
  ├─ AI 解析 free text（提取：品號、單價、交期、條件）
  └─ 結構化寫入 aooi084

Step 5：進入核價（axmt421）
  ├─ AI 自動帶出入圍供應商及報價
  ├─ AI 生成比價報告
  └─ 人確認 → 核價單審核（Y）

Step 6：核價確認 → 建立 PO（apmt500）
  └─ AI 自動填充 PO 欄位（料號、數量、單價、交期）
```

### 4.3 T100 API 端點

```
【aooi084 — 採購價格參照表（供應商報價寫入）】

寫入（POST）：
POST /api/aooi084/update
Body：
{
  "item_no": "料號",
  "vendor_id": "供應商",
  "site": "據點",
  "quoted_price": 報價單價,
  "quoted_date": 報價日期,
  "valid_until": 有效截止日,
  "payment_terms": "付款條件",
  "currency": "TWD/USD",
  "source": "RFQ",             ← AI 填入
  "rfq_no": "RFQ單號",
  "entered_by": "AI",
  "confidence_score": 0.85      ← AI 置信度
}

讀取（GET）：
GET /api/aooi084/query
參數：item_no, vendor_id, site
回應：該料件的供應商協議價格清單
→ AI 在生成比價報告時讀取此資料
```

---

## 5. 模組四：採購單維護（apmt500）

### 5.1 模組職責

```
目的：採購單是整個採購循環的核心單據
主要作業：apmt500（採購單維護）
AI 介入點：
  → PO 建立時：AI 自動填充預設資訊
  → PO Release 時：AI 自動發送供應商確認 mail
```

### 5.2 AI 在 PO 建立時的自動化

```
【AI 在 apmt500 的輔助能力】

觸發時機：apmt500 單據建立或修改時（Webhook）

AI 動作：
1. 自動填充
   ├─ aimm214 → 帶出供應商資訊
   ├─ aooi084 → 帶入最新協議價格
   ├─ axmt421 → 帶入核價
   └─ aimm211 → 帶入最近採購單價（imai021）

2. 異常標註
   ├─ 單價偏離核價 > 容差率 → 🔴 標註「價格異常」
   ├─ 數量低於最小採購量 → 🟡 標註「低於MOQ」
   └─ 交期不符合供應商承諾 → 🟡 標註「交期需確認」

3. PO Release 觸發
   └─ PO 狀態改為「已確認」→ 自動發送供應商確認 mail
```

### 5.3 T100 API 端點

```
【apmt500 — 採購單查詢】
GET /api/apmt500/query
參數：po_no, vendor_id, site, status, date_from, date_to
回應：
{
  "po_list": [{
    "po_no": "PO 號",
    "vendor_id": "供應商",
    "vendor_name": "供應商名稱",
    "vendor_email": "供應商Email",      ← AI 直接取用
    "site": "據點",
    "buyer": "採購員",
    "po_date": "PO 日期",
    "status": "confirmed/released/closed",
    "items": [{
      "line_no": 項次,
      "item_no": "料號",
      "item_desc": "品名",
      "qty": 數量,
      "unit": "單位",
      "unit_price": 單價,
      "delivery_date": "需求交期",
      "confirmed_date": "供應商確認交期",
      "status": "open/partial/closed"
    }],
    "payment_terms": "付款條件",
    "total_amount": 總金額
  }]
}

【apmt500 — PO 建立（寫入）】
POST /api/apmt500/create
Body：{ po_no, vendor_id, items[], ... }
→ AI 自動建立 PO 時使用

【apmt500 — PO Release】
POST /api/apmt500/release
Body：{ po_no }
→ 觸發 Agent 2（PO 追蹤智能體）啟動

【apmt500 — PO 狀態更新】
POST /api/apmt500/update_status
Body：{ po_no, status, updated_by: "AI" }
```

---

## 6. 模組五：IQC / FQC 品質檢驗（aqct300）

### 6.1 模組職責

```
目的：進貨品質控管，確保只有合格的物料入庫
主要作業：aqct300（品質檢驗記錄維護）
AI 介入點：
  → IQC 結果出爐 → AI 更新入庫預測日
  → 驗退 → AI 立刻通知採購 + 重新計算交期
```

### 6.2 AI 在 QC 流程中的角色

```
【aqct300 AI 介入工作流】

IQC/FQC 結果出爐（Webhook 或 DB Polling）
        │
        ▼
AI 讀取檢驗記錄（aqct300）
        │
   ┌────┴────┐
   │          │
  允收        驗退（1%）
   │          │
   ▼          ▼
AI 更新 T100   AI 立刻執行：
完工日預測     ├─ 計算「實際完工/入庫日」
通知採購       ├─ 若影響交期 → 即時預警
（更新 ai   ├─ 通知採購（aqct300+Vendor mail）
mm210)       ├─ 自動發送「驗退通知 mail」
              │  給供應商（LLM 生成格式）
              ├─ 更新供應商品質評分
              └─ 記錄重工成本
```

### 6.3 AI 驗退處理 Prompt

```
【驗退處理 Prompt（P-011）】

觸發：aqct300 結果 = "rejected"

AI 任務：
1. 讀取驗退記錄（aqct300）
   - 料號、批號、驗退數量、驗退原因代碼

2. 計算實際影響
   - 驗退數量 / 總數量 = 驗退比例
   - 對應 PO 的需求交期是否受影響

3. 生成「驗退處理建議」報告
   - 驗退原因摘要
   - AI 建議：退貨 / 讓步接受 / 特采
   - 對供應商品質評分的影響

4. 通知動作
   - 立即通知採購負責人（Slack）
   - 自動生成驗退 mail（給供應商）

5. 更新供應商評分
   - Quality Score 往下調
   - 若連續 3 次驗退 → 建議降級或更換供應商
```

### 6.4 T100 API 端點

```
【aqct300 — QC 檢驗記錄查詢】
GET /api/aqct300/query
參數：mo_no, inspection_date_from, inspection_date_to, site, status
回應：
{
  "inspection_records": [{
    "inspection_no": "檢驗單號",
    "mo_no": "工單/PO 號",
    "po_no": "PO 號",
    "item_no": "料號",
    "site": "據點",
    "qty_submitted": 送驗數量,
    "qty_accepted": 允收數量,
    "qty_rejected": 驗退數量,
    "rejection_rate": 驗退率,
    "result": "accept/reject/partial/concession",
    "rejection_reason_code": "驗退原因碼",
    "inspector": "檢驗員",
    "inspection_date": "檢驗日期",
    "fqc_required": true/false
  }]
}

【aqct300 — 緊急催料標記】
GET /api/aqct300/urgent
參數：site, days_ahead（如 3）
回應：即將到期的 IQC 檢驗清單
→ AI 主動催促進度落後的 QC
```

---

## 7. 模組六：進貨入庫與完工入庫（asft340）

### 7.1 模組職責

```
目的：完成物料正式入庫過帳
主要作業：
  asft340：工單完工/採購收貨入庫
  asft311：工單成套發料
  aint302：雜項入庫

AI 介入點：
  → asft340 入庫完成 → AI 更新 PO 狀態 + 通知採購
  → asft311 發料延遲 → AI 預警生產
```

### 7.2 T100 API 端點

```
【asft340 — 完工/採購入庫查詢】
GET /api/asft340/query
參數：mo_no, po_no, completion_date_from, completion_date_to, site
回應：
{
  "completion_records": [{
    "mo_no": "工單/PO 號",
    "po_no": "PO 號",
    "item_no": "料號",
    "site": "據點",
    "warehouse": "倉庫",
    "qty_completed": 完工數量,
    "actual_completion_date": "實際完工日",
    "planned_completion_date": "預計完工日",
    "delay_days": 延誤天數,
    "fqc_passed": true/false,
    "qc_inspection_no": "QC 單號",
    "status": "completed/partial/in_progress"
  }]
}

【asft311 — 工單發料記錄查詢】
GET /api/asft311/query
參數：mo_no, issue_date_from, issue_date_to
回應：
{
  "issue_records": [{
    "mo_no": "工單號",
    "item_no": "料號",
    "qty_issued": 發料數量,
    "issue_date": "發料日期",
    "warehouse": "倉庫",
    "status": "issued/pending/partial"
  }]
}
```

---

## 8. 模組七：應付帳款（aapt110）

### 8.1 AI 在 AP 的角色

```
【AI 應付帳款異常偵測】

定時執行（每日排程）：
  ├─ 讀取 aapt110 最新對帳資料
  ├─ AI 比對：發票金額 vs PO 金額 vs 入庫數量
  └─ 發現異常 → 立刻通知採購 + 財務

異常類型：
  ├─ 發票金額 > PO 金額 → 🔴 多算
  ├─ 發票數量 < 入庫數量 → 🟡 少算
  ├─ 重複請款             → 🔴 立刻預警
  └─ 核銷金額不符         → 🟡 需人工核查
```

---

## 9. 完整 T100 API 端點總表

```
【一、採購基礎資料】
GET  /api/aimm214/query            據點採購資料維護
GET  /api/aimm214/expiring          即將到期核價查詢

【二、核價流程】
GET  /api/axmt420/query            採購核價查詢
GET  /api/axmt421/query            委外核價查詢
GET  /api/axmt421/expiring         委外核價到期預警

【三、RFQ / 報價】
GET  /api/axmt400/query            銷售估價單查詢
GET  /api/axmt410/query            銷售報價單查詢
GET  /api/aooi084/query            採購價格參照表查詢
POST /api/aooi084/update           採購價格參照表寫入

【四、採購單】
GET  /api/apmt500/query            採購單查詢
POST /api/apmt500/create           採購單建立
POST /api/apmt500/release          採購單 Release
POST /api/apmt500/update_status    採購單狀態更新
GET  /api/apmt421/query            PO 歷史成交價查詢

【五、IQC / FQC】
GET  /api/aqct300/query            QC 檢驗記錄查詢
GET  /api/aqct300/urgent           緊急 QC 催辦

【六、入庫 / 發料】
GET  /api/asft340/query            完工/採購入庫查詢
GET  /api/asft311/query            工單發料記錄查詢
POST /api/asft311/issue            工單發料確認

【七、應付帳款】
GET  /api/aapt110/query            對帳資料查詢
GET  /api/aapt110/mismatch         發票金額異常清單
```

---

## 10. AI 全鏈路介入矩陣

```
╔═══════════════════════════════════════════════════════════════════╗
║         AI 介入矩陣（6 大模組 × 4 個 Agent）                     ║
║                                                                   ║
║          │ Agent0  │ Agent1   │ Agent2   │ Agent3   │ Agent4    ║
║  模組    │ 協調者  │ RFQ策略  │ PO追蹤   │ 通訊     │ 委外管理  ║
║  ───────┼────────┼─────────┼─────────┼─────────┼─────────  ║
║  aimm214 │         │ ✅讀取   │          │          │ ✅讀取     ║
║  axmt421 │         │ ✅建議   │          │          │ ✅建議     ║
║  axmt410 │         │ ✅生成   │          │ ✅解析   │           ║
║  aooi084 │         │ ✅比價   │          │ ✅寫入   │           ║
║  apmt500 │ ✅分流  │ ✅建立   │ ✅追蹤   │ ✅確認   │ ✅更新     ║
║  aqct300 │         │         │ ✅解讀   │ ✅通知   │ ✅解讀     ║
║  asft340 │         │         │ ✅更新   │          │ ✅更新     ║
║  aapt110 │         │         │ ✅比對   │          │           ║
╚═══════════════════════════════════════════════════════════════════╝

圖例：✅ = AI 主要負責該環節
```

---

*版本：v2.0 | 維護者：採購智能化專案團隊*
*最後更新：2026-03-25*
