# 採購智能化系統整合規格書
## T100 × n8n × Domino（Lotus Notes）三元整合
> 版本：v1.0 | 日期：2026-03-25 | 語言：繁體中文

---

## 1. 系統整合架構圖

```
┌─────────────────────────────────────────────────────────────────┐
│                    企業內網（Intranet）                          │
│                                                              │
│  ┌─────────────┐     ┌─────────────────┐                   │
│  │  鼎捷 T100  │     │  IBM Domino      │                   │
│  │  ERP 系統   │     │  (Lotus Notes)  │                   │
│  │             │     │                  │                   │
│  │  AIM 模組   │     │  IMAP Server    │                   │
│  │  AP 模組    │     │  SMTP Server    │                   │
│  │  PO 模組    │     │  Mail Database  │                   │
│  └──────┬──────┘     └────────┬────────┘                   │
│         │ HTTP REST / SOAP    │ IMAP / SMTP                │
└─────────┼─────────────────────┼─────────────────────────────┘
          │                     │
          ▼                     ▼
    ┌─────────────────────────────────────────┐
    │              n8n 主機                      │
    │                                          │
    │  ┌──────────────────────────────────┐   │
    │  │         n8n Workflow Engine         │   │
    │  │                                    │   │
    │  │  ┌─────┐ ┌─────┐ ┌─────┐ ┌────┐ │   │
    │  │  │ Ag0 │ │ Ag1 │ │ Ag2 │ │ Ag3│ │   │
    │  │  │Cood.│ │RFQ  │ │ PO  │ │Comms│ │   │
    │  │  └─────┘ └─────┘ └─────┘ └────┘ │   │
    │  │                                    │   │
    │  │  ┌──────────────────────────────┐│   │
    │  │  │  Tool Layer                    ││   │
    │  │  │  HTTP / IMAP / SMTP / LLM    ││   │
    │  │  └──────────────────────────────┘│   │
    │  └──────────────────────────────────┘   │
    │                                          │
    │  ┌──────────────────────────────────┐   │
    │  │  PostgreSQL 資料庫               │   │
    │  │  - 採購案件狀態表               │   │
    │  │  - 供應商通訊日誌               │   │
    │  │  - AI 決策歷史                  │   │
    │  └──────────────────────────────────┘   │
    └─────────────────────────────────────────┘
                      │
                      │ Slack / Teams Webhook
                      ▼
              ┌─────────────────┐
              │  採購團隊       │
              │  (Slack/Teams)  │
              └─────────────────┘
```

---

## 2. T100 整合規格

### 2.1 T100 API 串接方式

**推薦方式：HTTP REST API**

鼎捷 T100 提供以下兩種 API 接口：

| 接口類型 | 說明 | n8n 支援方式 |
|---------|------|------------|
| **REST API（JSON）** | T100 提供的現代 HTTP API，POST/GET JSON | n8n HTTP Request Node ✅ |
| **Web Service（SOAP/XML）** | 較傳統的 SOAP 接口 | n8n HTTP Request + XML 解析 ✅ |
| **DB 直接讀取** | 直接 SQL 查詢 T100 DB | 不建議（風險高）|

**🔑 重要：請向鼎捷原廠確認**
- T100 版本（建議 T100 2020 以上）
- 是否已開通 API 服務模組
- API Server 的 IP / Port / 認證方式

### 2.2 T100 關鍵 API 端點

```
【API 端點對照表】

基礎 URL：https://{T100主機}:{T100_PORT}/t100api/

───────────────────────────────────────────────────────────
查詢功能（n8n HTTP GET）
───────────────────────────────────────────────────────────

AVL 供應商查詢
GET /api/aimm214/query
參數：item_no, site
回應：{ "vendor_list": [...] }

PO 歷史查詢
GET /api/apmt420/query
參數：item_no, vendor_id, period
回應：{ "po_history": [...] }

PO 明細查詢
GET /api/apmt421/query
參數：po_no
回應：{ "po_detail": {...} }

PR 請購單查詢
GET /api/apmt401/query
參數：pr_no
回應：{ "pr_detail": {...} }

───────────────────────────────────────────────────────────
寫入功能（n8n HTTP POST）
───────────────────────────────────────────────────────────

PO 建立
POST /api/apmt421/create
Body：{ "po_no": "...", "vendor_id": "...", "items": [...] }
回應：{ "status": "success", "po_no": "..." }

PO 交期更新
POST /api/apmt421/update
Body：{ "po_no": "...", "update_type": "delivery_date", "new_date": "...", "reason_code": "..." }
回應：{ "status": "success" }

異動記錄寫入
POST /api/apmt421/log
Body：{ "po_no": "...", "log_type": "delay", "content": "...", "handled_by": "AI" }
回應：{ "status": "success" }
```

### 2.3 T100 認證方式

```
【認證方式】（請向鼎捷 IT 確認）

方式 A：Bearer Token（推薦）
Header：Authorization: Bearer {access_token}
取得方式：向 T100 管理員申請 API Token

方式 B：API Key
Header：X-API-Key: {api_key}

方式 C：Basic Auth
Header：Authorization: Basic {base64(username:password)}
```

### 2.4 當 T100 API 文件不完整時的替代方案

**替代方案：SOAP Web Service**

鼎捷 T100 標準配備 SOAP 接口（即使沒有文件，也可以用以下方式探索）：

```
【WSDL 探索】
GET https://{T100主機}:{T100_PORT}/wsdl/t100ws.wsdl

n8n HTTP Request 設定：
- Method：POST
- URL：https://{T100主機}:{T100_PORT}/webservices/t100ws
- Header：Content-Type: text/xml
- Body（SOAP 封包格式）：
```

### 2.5 T100 資料表對照（供 IT 參考）

| 業務功能 | T100 模組 | 主要資料表 | 關鍵欄位 |
|---------|----------|-----------|---------|
| 料件主檔 | AIM | aimm_t | item_no, item_desc, spec |
| AVL 供應商 | AIM | aimm214 | item_no, vendor_id, vendor_name, status |
| 採購單 | APM | apmt410 | po_no, vendor_id, po_date, status |
| PO 明細 | APM | apmt421 | po_no, item_no, qty, unit_price, due_date |
| 歷史成交價 | APM | apmt422 | item_no, vendor_id, po_no, unit_price, po_date |
| 組織基本資料 | AO | aooi_t | site, dept, user |
| 異動記錄 | APM | apmt425 | po_no, change_type, old_value, new_value |

---

## 3. Domino（Lotus Notes）整合規格

### 3.1 Domino IMAP/SMTP 設定

```
【IMAP 設定（用於接收供應商回覆）】
伺服器：{domino主機}
Port：993（SSL）或 143（非 SSL）
認證：Domino 應用程式專用 ID
建議：建立一個「採購機器人專用 Domino ID」

【SMTP 設定（用於發送 mail）】
伺服器：{smtp主機}（可用 Domino SMTP 或公司 mail gateway）
Port：587（STARTTLS）或 465（SSL）
認證：應用程式專用帳號

【 Domino Mail Database 設定】
Database Path：mail\procurement_bot.nsf
視圖（View）：采购待处理（按 PO 號索引）
視圖（View）：供應商回覆（按日期索引）
```

### 3.2 IMAP Filter 規則（n8n 端）

```
【建議的 IMAP 過濾條件】

主題包含：PO / 交期 / 確認 / RFQ / Quotation / 報價
或者：
寄件人：@供應商網域（白名單內的供應商）

【過濾範例】
Subject CONTAINS "PO"
OR Subject CONTAINS "確認"
OR Subject CONTAINS "交期"
OR Subject CONTAINS "RFQ"
```

### 3.3 n8n Email Trigger 設定

```
【n8n IMAP Email Trigger 設定值】

節點參數：
- Mailbox URL：imap://{domino主機}:993
- User：CN=procurement bot/OU=IT/O=YOURCOMPANY
- Password：{應用程式專用密碼}
- SSL：true（Port 993）
- Allowed Labels/Folders：INBOX
- Poll Interval：5 分鐘
- Set Flags：Mark as Read（在成功處理後）
- Download Attachments：true（存放附件）
```

### 3.4 Domino 端 Mail Routing 建議

```
【建議：在 Domino 建立專用 Mail-In Database】

建立專用採購機器人資料庫（procurement_bot.nsf）：
- 所有與採購機器人的往來 mail 進入此資料庫
- 與採購團隊的正常 mail 隔離
- 方便日後稽徵和問題排查

設定 Mail-In Database：
1. Domino Administrator 建立新的 Mail-In Database
2. 設定 ACL（存取控制清單）
3. 在 DNS/Mail Gateway 設定 Routing Rules
4. 將供應商回覆導向此資料庫
```

---

## 4. n8n 主機部署選項

| 部署方式 | 優點 | 缺點 | 適用場景 |
|---------|------|------|---------|
| **自 HOST（VM/實體）** | 完全控制、資料不外流 | 需 IT 自行維護 | 適合有 IT 團隊的企業 |
| **Docker 部署** | 快速安裝、易於遷移 | 需要 Docker 知識 | 推薦中小企業 |
| **n8n Cloud（SaaS）** | 免維護、快速上線 | 資料需上雲 | 不建議（採購資料敏感）|

**🔒 安全建議：n8n 部署在企業內網，不對外暴露**
- 若需與外部供應商 mail 往來，使用反向代理
- 所有 API Key / Token 存放在 n8n 環境變數
- 建議启用 n8n 的執行日誌加密功能

---

## 5. 資料流向矩陣

```
┌──────────────────────────────────────────────────────────────────┐
│                       資料流向圖                                  │
│                                                                  │
│  【Phase 1：RFQ 詢價】                                          │
│                                                                  │
│  T100 ──→ AVL 資料 ──→ n8n ──→ RFQ Mail ──→ Domino SMTP ──→ 供應商│
│       │                    │                                      │
│       │              AI 分析                                      │
│       │                    ↓                                      │
│  T100 ──← 歷史 PO ──← 供應商回覆 ──→ Domino IMAP ──→ n8n ──→  比價報告│
│                                                            ↓      │
│                                                      Slack 通知│
│                                                      人審核 ──→│
│                                                            ↓      │
│                                                      T100 PO 建立│
│                                                                  │
│  【Phase 2：PO 追蹤】                                          │
│                                                                  │
│  T100 ──→ PO Release 事件 ──→ n8n ──→ 交期確認 mail ──→ Domino ──→ 供應商│
│                                       ↓                            │
│                                 2 工作天 Wait                      │
│                                       ↓                            │
│  T100 ──← 交期更新 ──→ 供應商回覆 ──→ Domino IMAP ──→ n8n ──→ AI 評估│
│               │                              ↓                      │
│               │                        Slack 通知                   │
│               │                        人決定 ──→                  │
│               ↓                                                   │
│         T100 寫入異動                                            │
└──────────────────────────────────────────────────────────────────┘
```

---

## 6. 安全與權限設計

### 6.1 最小權限原則（Principle of Least Privilege）

```
【T100 API 權限】
- 僅授權 n8n 所需的最小功能（Read on AVL/PO + Write on PO Update）
- 不授權：財務模組、人事模組、系統管理模組
- 建立專用的 API User（不要用 admin 帳號）

【Domino 權限】
- 採購機器人 ID 僅有 mail-sending 權限
- 嚴禁讀取其他部門的 mail
- 定期更換密碼（建議每季）

【Slack/Teams 權限】
- 僅有發送訊息權限
- 無法讀取頻道歷史
- 使用 Incoming Webhook（最小權限）
```

### 6.2 資料安全要點

```
1. 所有 API Key / Token 存放在 n8n 環境變數（不寫入 Workflow）
2. T100 認證資訊定期輪換（建議每季）
3. n8n Workflow 日誌中禁止記錄完整 API 回應（安全原則）
4. 所有採購資料不得離開企業網絡
5. AI 處理過程中如有異常，必須紀錄並通知 IT
```

---

## 7. 先行驗證清單（Pilot 前必須完成）

```
【IT 環境確認清單】

□ 1. T100 API Server 已啟動（IP:Port 已確認）
□ 2. T100 API 文件已取得（至少基本的 Read/Write API）
□ 3. T100 API User 已建立，權限已設定
□ 4. T100 API Token / Key 已取得
□ 5. Domino IMAP Server 已啟動
□ 6. Domino 採購機器人專用 ID 已建立
□ 7. Domino IMAP 可從 n8n 主機連線（Firewall 確認）
□ 8. SMTP Server 已設定（允許採購機器人寄信）
□ 9. Slack / Teams Incoming Webhook URL 已建立
□ 10. PostgreSQL 資料庫已建立（狀態追蹤用）
□ 11. n8n 主機已安裝，版本 >= 1.0
□ 12. n8n HTTP 可達 T100 API（網絡確認）
□ 13. LLM API Key 已設定（Claude / OpenAI / MiniMax）

【Pilot 測試清單】

□ 1. 手動觸發一筆測試 PR/PRO 事件，確認 n8n Webhook 接收正常
□ 2. IMAP Trigger 接收測試 mail，確認解析正常
□ 3. T100 AVL 查詢正確回傳資料
□ 4. AI Agent 生成 RFQ Mail 格式正確
□ 5. Free Text 解析置信度達標（> 70%）
□ 6. Slack 通知正常發送
□ 7. 人類審核 Gate 流程正常運作
□ 8. T100 Write Back 成功寫入
□ 9. End-to-End 完整流程測試（從 PR 到 PO 建立）
□ 10. 催貨流程測試（超時未回覆情境）
```

---

## 8. IT 維護手冊（日常）

```
【日常維護】
- 每週檢查 n8n Workflow 日誌（錯誤數量、成功率）
- 每月檢查 T100 API 使用量
- 每季檢查 Domino ID 密碼到期日
- 每季檢查 LLM API 配額

【常見錯誤處理】
1. T100 API 403 Forbidden
   → 原因：Token 過期或權限不足
   → 處理：重新產生 Token 或調整 T100 權限

2. IMAP 無法連線
   → 原因：Domino ID 密碼過期 / Firewall 阻擋
   → 處理：更新密碼 / 確認 Firewall 規則

3. AI 回覆品質下降（幻覺）
   → 原因：LLM Temperature 過高或 Prompt 有漏洞
   → 處理：調低 Temperature 至 0.3，加強 Prompt 中的限制條件

4. Slack 通知發送失敗
   → 原因：Webhook URL 過期
   → 處理：重新建立 Incoming Webhook

【n8n 緊急停止流程】
若系統出現異常：
1. 在 n8n UI 中停用所有採購 Workflow（Active: OFF）
2. 通知採購團隊手動處理（暫時回到舊流程）
3. 檢查 n8n 日誌找出問題原因
4. 修復後重新啟用 Workflow
```

---

## 9. 預估時程與里程碑

```
【Phase 1：Pilot（4-6 週）】

第 1 週：環境建置 + API 串接
  □ T100 API 串接驗證
  □ Domino IMAP 串接驗證
  □ n8n 主機架設
  □ n8n 基本 Workflow 建立

第 2 週：AI Agent 設定
  □ Agent 0-3 Prompt 設定
  □ Tool Layer 設定
  □ LLM 串接
  □ 單 Agent 測試

第 3 週：整合測試
  □ End-to-End 流程測試
  □ Free Text 解析測試（真實 mail）
  □ Gate 流程測試

第 4 週：Pilot 上線
  □ Pilot 對象：1-2 個採購員 + 1 個類別料件
  □ 觀察 2 週
  □ 收集 Feedback
  □ 調整 Prompt 和流程

【Phase 2：擴大範圍（6-8 週）】
- 擴大到所有料件類別
- 建立完整的供應商資料庫
- 與 T100 深度整合（自動 PO 建立）

【Phase 3：AI 智能化深化（8-12 週）】
- 預測性備料（結合歷史數據）
- 供應商風險評估模型
- 與 T100 BOM 整合（MRP 驅動）
```

---

*文件版本：v1.0 | 維護者：採購智能化 IT 團隊*
*最後更新：2026-03-25*
