# 🤖 Multi-Agent 規劃 SOP — Aclis 操作手冊

> 建立時間：2026-03-23
> 版本：v2.0
> 維護人：Aclis 🐉

---

## 一、核心定位：何時用 Sub-Agent

### 該用 Sub-Agent 的四個維度

| 維度 | 標準 | 範例 |
|------|------|------|
| **時間** | 任務需要 >5 分鐘 | Research、數據處理、批次寫入 |
| **並行** | 多個獨立任務可同時執行 | 4 個晨報同時並行 |
| **等待** | 主流程需要等待外部 API 回應 | Get Notes 讀取 |
| **隔離** | 失敗不能影響主流程 | Cron Job 內部處理 |

### 不該用的情況

```
❌ 簡單問題（<1 分鐘可完成）→ 直接做
❌ 需要大量上下文（session 歷史傳遞成本高）→ 直接做
❌ 有順序依賴（串聯比並聯更簡單）→ 用 Cron 排程
❌ 風險高的外部操作（郵件、公開發布）→ 我自己做
```

---

## 二、四種 Agent 角色與文本要求

### 角色矩陣

| 角色 | 責任 | 輸入 | 輸出 | 語言風格 |
|------|------|------|------|---------|
| **Research Agent** | 數據蒐集、網頁爬取、API 讀取 | Prompt 中的具體指令 | 原始素材文件（**含來源備註**）| 客觀、事實導向 |
| **Report Writer** | 蒸餾、結構化、洞察提煉 | Research Agent 產出的 md 文件 | 進化版晨報 | 結構化、有觀點 |
| **Verify Agent** | 事實核查、邏輯檢驗、數據校正 | Report Writer 產出 | 驗證報告 | 懷疑、嚴謹 |
| **Master** | 整合、決策、分配任務 | 全部 Agent 產出 | 最終交付 | 俯瞰、負責 |

### 數據來源分級標準（必備欄位）

| 等級 | 定義 | 範例 |
|------|------|------|
| **T1** | 官方公告、監管文件、年報、SEC/EDGAR | Federal Reserve、SEC、World Bank |
| **T2** | 頂級財經媒體、權威機構研究 | Bloomberg、Reuters、FT、頂級投行 |
| **T3** | 行業數據庫、協會報告 | IBISWorld、Statista、ICET |
| **T4** | 公司公告、知名咨詢公司 | 瑞銀、高盛、麥肯錫研究 |
| **T5** | 新聞媒體、社交媒體 | WSJ、微博、巴隆氏 |

> **來源備註強制格式：** 每筆記錄必須包含
> `來源等級 | 來源名稱 | URL（可點擊）| 抓取時間 | 可靠性評級`

---

## 三、不同 Agent 之間的溝通方式

### 溝通方式總覽

| 溝通方式 | 用途 | 穩定性 | 適用場景 |
|---------|------|--------|---------|
| **檔案交換** | 素材傳遞（md/json） | ⭐⭐⭐⭐⭐ | 絕大部分場景 |
| **progress.json** | 狀態追蹤 | ⭐⭐⭐⭐ | 多 Agent 協作協調 |
| **subagent_announce** | 完成通知 | ⭐⭐⭐⭐⭐ | 主從之間 |
| **Session History** | 歷史上下文傳遞 | ⭐⭐ | 不得已時 |
| **Memory File** | 長期知識共享 | ⭐⭐⭐⭐ | 家族共有知識 |

### 檔案交換：核心規範

```
輸入檔案：給出具體路徑，不要模糊描述
輸出檔案：Prompt 中明確指定路徑 + 檔名格式

命名格式：
  research/[類型]_raw.md      → 素材
  outputs/[類型]_YYYY-MM-DD.md → 進化版晨報
  verify/[類型]_YYYY-MM-DD.md → 驗證報告
  progress.json                → 狀態追蹤
```

---

## 四、標準 Prompt 模板庫

### 模板 A：Research Agent（數據蒐集型）

```markdown
# [領域] Research Agent 工作日誌

## 任務
[一句話目標]

## 背景
Jan 需要：[使用場景]
截止時間：[如需要]

## 步驟

### Step 1：[數據來源]
[Python 指令 / API 呼叫]
每次操作後 sleep [X] 秒

### Step 2：[素材整理]
對每筆數據：
- 標題：[如實記錄]
- 來源：[URL]
- 一句話摘要：[提煉]

### Step 3：寫入素材文件
路徑：`/workspace/multi_agent/research/[領域]_raw.md`

## 溝通約定
- 找不到數據：標記「[未知]」，不要中斷
- API 429：sleep 5秒後重試，最多3次
- 任何錯誤：記錄到 stderr，不終止流程

## 輸出
路徑：`/workspace/multi_agent/research/[領域]_raw.md`
格式：Markdown
成功標準：處理 N 筆，寫入 M 行
```

### 模板 B：Report Writer（蒸餾進化型）

```markdown
# [領域] Report Writer 工作日誌

## 任務
將 research 素材蒸餾成進化版[領域]晨報

## 輸入文件（全部讀取）
[具體路徑列表]

## 步驟

### Step 1：讀取全部輸入
[Python 指令]

### Step 2：蒸餾與結構化
根據輸入素材，提煉：
1. 當頭棒喝（一針見血的觀察）
2. 三個事實（最重要的數據點）
3. 洞察與連結（與 Jan 投資系統的關聯）
4. ⚖️ 風險紀律
5. 🕯️ 空的智慧（佛學視角）

### Step 3：寫入輸出文件
路徑：`/workspace/multi_agent/outputs/[領域]_YYYY-MM-DD.md`

## 溝通約定
- 如果素材不足：明確標記「素材缺口：[具體領域]」
- 不要捏造數據
- 格式偏少：增加框架說明

## 輸出
路徑：`/workspace/multi_agent/outputs/[領域]_YYYY-MM-DD.md`
格式：Markdown（包含 ⚖️ 🕯️ 等 emoji 標記）
```

### 模板 C：Verify Agent（核查型）

```markdown
# [領域] Verify Agent 工作日誌

## 任務
對 Report Writer 產出進行事實核查

## 輸入文件
`/workspace/multi_agent/outputs/[領域]_YYYY-MM-DD.md`

## 核查維度

### 1. 數據準確性
- [ ] 每個數據點是否有來源？
- [ ] 來源是否為可信賴來源（T1/T2）？
- [ ] 數值是否在合理範圍內？

### 2. 邏輯一致性
- [ ] 事實與結論是否一致？
- [ ] 是否存在邏輯跳躍？

### 3. 完整性
- [ ] 是否涵蓋主要維度？
- [ ] 是否有遺漏的重要觀點？

## 輸出
路徑：`/workspace/multi_agent/verify/[領域]_YYYY-MM-DD_verified.md`
格式：清單 + 備註
```

---

## 五、Jan 晨報流水線：最佳實踐

### 完整流程圖

```
[06:00] Cron Job 觸發
         │
         ├──→ Invest Agent（並行，2m40s）
         │         ↓ research/invest_raw.md
         ├──→ Tech Agent（並行，3m14s）
         │         ↓ research/tech_raw.md
         ├──→ Semiconductor Agent（並行）
         │         ↓ research/semiconductor_raw.md
         └──→ Learning Agent（並行，9m58s）
                   ↓ research/learning_raw.md
                      ↓（subagent_announce）
              [Master 接收全部]
                    ↓
              讀取全部 research 檔案
                    ↓
         ┌────────┴────────┐
         ↓  💰 蒸餾投資晨報  ↓
         ↓  🤖 蒸餾AI晨報   ↓
         ↓  💾 蒸餾半導體晨報↓
         ↓  📚 蒸餾讀書晨報  ↓
         └────────┬────────┘
                  ↓
         ┌────────┴────────┐
         ↓ GitHub 備份      ↓ Get Notes 寫入
         └────────┬────────┘
                  ↓
            progress.json 更新
                  ↓
              [完成]
```

### 並行優化原理

```
串聯：4個 Agent × 平均5分鐘 = 20分鐘
並行：4個 Agent 同時 = 最多 10分鐘（含 Master 蒸餾）

節省：50% 時間
代價：API 頻率負載增加（需要 delay 控制）
```

### API 頻率控制策略

```
Research Agent（對外 API）：
  Get Notes 讀取：每頁 之後 sleep 2s
  網頁抓取：每個 URL 之後 sleep 1s

蒸餾（Master，不對外 API）：
  無頻率限制，直接讀取本地檔案

寫入（Master + Get Notes）：
  每篇 之後 sleep 1.5s
  寫入筆記 之後 sleep 2s
```

---

## 六、異常處理矩陣（完整版）

| 異常 | 等級 | 處理方式 | 預防 |
|------|------|---------|------|
| Sub-agent timeout | P1 | 檢查 partial output，重跑 | 設 timeout = 預期×1.5 |
| API 429 | P1 | sleep 5s 重試3次 | 控制頻率，設定 delay |
| API 500/502/503 | P1 | sleep 10s 重試3次 | — |
| Output 檔案不存在 | P2 | 檢查路徑，正確則重跑 | Prompt 中明確路徑 |
| 數據不足 | P2 | 標記缺口，繼續執行 | — |
| 格式錯誤 | P2 | 補正後繼續 | Prompt 中給格式範例 |
| 磁碟空間不足 | P0 | 立刻告知 Jan | 定期清理 /tmp |

---

## 七、Lesson Learned 清單

```
1. Timeout 要長不設短
   短了：強行終止，數據丢失
   長了：可主動結束，不浪費

2. API delay 是必備，不是可選
   子 agent 對外呼叫也需要安全延遲
   否則 429 會中斷整個流程

3. 路徑要具體，不要模糊
   ✅ /workspace/multi_agent/research/invest_raw.md
   ❌ 寫到那個資料夾

4. 不要假設，要驗收
   收到 announce → 讀取 output 檔案 → 確認內容

5. progress.json 是事實標準
   檔案存在 = 步驟完成，不是「有在跑」
```

---

## 八、溝通方式使用場景

### 檔案交換（主要方式）

```
Jan / Master → Research Agent：
  Prompt 中指定輸入/輸出路徑

Research Agent → Master：
  寫入 research/*.md，subagent_announce 通知

Master → Verify Agent：
  Prompt 指定驗證目標檔案

Verify Agent → Master：
  寫入 verify/*.md
```

### Session History（不得已才用）

```
適用場景：Research Agent 需要延續上一個 sub-session 的對話

代價：
  - 歷史傳遞有 token 限制
  - 每次傳遞增加成本

原則：優先用檔案交換替代
```

### Memory File（長期知識）

```
適用場景：
  - 家族設定（USER.md、MEMORY.md）
  - 技術參數（TOOLS.md）
  - 運行狀態（HEARTBEAT.md）

不適用場景：
  - 一次性任務數據
  - Agent 間的短期協調
```

---

## 九、快速啟動清單

```
□ 任務觸發：Jan 下指令
□ 確認角色：Research / Report Writer / Verify / Master
□ 選擇模式：run（一次性）/ session（持續對話）
□ 設定 timeout：預期時間 × 1.5
□ 準備 Prompt：使用模板（見第二章）
□ 告知 Jan：任務開始，預計時間
□ 等待 announce：不主動 poll
□ 驗收結果：讀取 output，檢查數量/格式
□ 整合蒸餾：Master 環節
□ 完成交付：GitHub + Get Notes + 告知 Jan
```

---

*本 SOP 由 Aclis 維護，每季審查一次。*
*最後更新：2026-03-23 v2.0 by Aclis 🐉*