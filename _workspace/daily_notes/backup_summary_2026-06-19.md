# 昨天備份資料摘要 (2026-06-19)

來源：`/workspace/backup/getnotes_backfill_2026-05-15-16.json` (4.0MB)

## 基本資訊
- cutoff (備份截止日): 2026-05-15
- fetched_at (抓取時間): 2026-06-19T18:34:29
- 規模: 600 篇全部為「新增」(already_synced=0)
- 抓取當下: 600/600 都還沒分類（unclassified_count=600）

## source 分布（這才是真正的「來源分類」）
| source      | 數量 | 說明 |
|-------------|------|------|
| dedao       | 355  | 得到 App 內容（主力）|
| openapi     | 87   | 透過 openapi 抓取（晨報系）|
| yoda        | 73   | 有道雲筆記來源 |
| getnote_bu  | 51   | Get Notes 用戶手動備份 |
| app         | 26   | App 端直接抓取 |
| web         | 5    | 網頁剪藏 |
| knowledge   | 3    | 知識庫內建立 |

## note_type 分布
- plain_text: 574 (95.7%)
- link: 19
- img_text: 5
- audio: 2

## 晨報系（在 openapi 87 篇中）
- 半導體晨報: 26
- 讀書晨報: 18
- AI 前沿科技晨報: 16
- 投資晨報: 15
- 醫療健康晨報: 8

## 熱門 tags Top 10
1. 得到 (355) — 來源標記
2. wisdom (65) — wisdom 知識庫分類
3. aclis (50) — 你自己標的
4. 快刀广播站 (33)
5. 吴军·财商训练40讲 (30)
6. 卓克·科技参考5 (30)
7. 赵金刚·王阳明60讲 (28)
8. 万维钢·现代思维工具100讲 (28)
9. 刘润·商业报告解读 (27)
10. 得到头条 (24)

→ 得到 6 大日更專欄都有抓到。

## 另一個檔案
`a4_a6_summary_2026-06-19.json` (270 bytes) — **這是 6/19 的分類統計摘要**
- 顯示那時有 246 篇處理過
- classified: 26 (5+7+3+7+1+3+0)
- unclassified_count: 220
- sync_state_updated: true

## 我的觀察
1. 備份的 600 篇都還沒分類 — 等同於「原始素材庫」
2. 得到課程為主力（355/600 = 59%）
3. 晨報系集中在 87 篇 openapi 抓取
4. tags 已預打標（aclis, wisdom, 得到, semiconductor 等），可以直接做 topic 萃取
5. by_kb 欄位是空的（備份時結構有 bug），實際 KB 需從 source + tags 反推

## 這份備份能用來做什麼？
- ✅ 直接蒸餾 600 篇 → 寫入 wiki/topics（這就是 Todo #4 的目標）
- ✅ tags 已分類好，可批次處理（按 tag group 蒸餾）
- ✅ 50 篇 aclis-tagged = 你親自標記的，優先處理
- ✅ 65 篇 wisdom-tagged = 智慧相關，可獨立成「金句/思維模型」主題

## 與「昨天的對話」差別
你問的「昨天備份資料（談話）」 — 但這份檔案是「昨天的 Get Notes 抓取備份」，
不是對話日誌。如果你要找的是昨天的對話紀錄（chat history），
要看 `/workspace/.matrix-chat-history/` 或是 `memory/2026-06-21.md`。
