# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

### Telegram Bot
- **Bot:** @Kyonwang_bot
- **Token:** `8682239959:***`
- **狀態：** 已配置，測試中

### Get 筆記 API（✅ 2026-05-15 已修復）

> 2026-05-15 確診：之前用截斷 key 導致 401。現在用**完整 key**（73字）✅
> 完整 key 存於 `/root/.credentials/getnotes_api_token.txt` + `/root/.credentials/getnotes_client_id.txt`

| 項目 | 值 |
|------|-----|
| API Key | `gk_live_6e9c2b820bf9af89.c618dd498d40262aee4d90fe9cea8a75ffe5807801baa278` |
| Client ID | `cli_3802f9db08b811f197679c63c078bacc` |
| Base URL | `https://openapi.biji.com/open/api/v1` |
| 認證方式 | `Authorization: {API_KEY}` + `X-Client-ID: {Client_ID}`（無 Bearer） |
| 配額 | 20000/day (今日已用 5) |

#### API 端點速查

| 功能 | Method | Path |
|------|--------|------|
| 知識庫列表 | GET | `/resource/knowledge/list?page=1` |
| 知識庫筆記列表 | GET | `/resource/knowledge/notes?topic_id={id}&page=1` |
| 全域語義召回 | POST | `/resource/recall` |
| KB內語義召回 | POST | `/resource/recall/knowledge` |
| 新增筆記標籤 | POST | `/resource/note/tags/add` |
| 刪除筆記標籤 | POST | `/resource/note/tags/delete` |
| 添加筆記到KB | POST | `/resource/knowledge/note/batch-add` |
| 從KB移除筆記 | POST | `/resource/knowledge/note/remove` |
| 配額查詢 | GET | `/resource/rate-limit/quota` |

### 數據安全規範（🔐 請遵守）

```
嚴禁寫入 Log / Session 歷史：
  ❌ API 回應的原始內容
  ❌ 筆記正文
  ❌ 完整 API Key（Token、Client ID）
  ✅ 允許：成功/失敗狀態、數量統計、時間戳

API 配額警戒線（2026-03-26 更新）：
  讀取：黃線 60%（600/1000）| 紅線 80%（800）
  寫入：黃線 60%（300/500）| 紅線 80%（400）
  寫入筆記：黃線 60%（30/50）| 紅線 80%（40）
  → 紅線觸發：立刻告知 Jan

配額查詢端點（主動監控用）：
  GET https://openapi.biji.com/open/api/v1/resource/rate-limit/quota
  Headers: X-Client-ID + Authorization

觸發 429 時的 reason 判斷：
  not_member               → 非會員，無權限
  qps_global_exceeded      → 全域頻率超限（短暫等待後重試）
  qps_bucket_exceeded      → 桶級頻率超限（等待後重試）
  quota_daily_exceeded     → 日配額用盡（等 reset_at 時間戳）
  quota_monthly_exceeded   → 月配額用盡（等 reset_at 時間戳）
  quota_write_note_daily_exceeded  → 寫筆記日配額用盡
  quota_write_note_monthly_exceeded → 寫筆記月配額用盡

憑證輪換：每季（90天）檢查一次
```

### GitHub 同步

- **腳本位置**: `/workspace/tools/github_sync.py`
- **腳本位置（Obsidian）**: `/workspace/tools/obsidian_github_sync.py`
- **PAT 獲取**: https://github.com/settings/tokens
- **權限**: 需要 `repo` 範圍才能访问私有庫
- **Jan Vault PAT**: `ghp_nV...tHSp`

```bash
# 同步公開倉庫（無需 Token）
python3 /workspace/tools/github_sync.py owner repo path/

# 同步私有倉庫
GITHUB_TOKEN=*** python3 /workspace/tools/github_sync.py owner repo path/

# 指定分支
python3 /workspace/tools/github_sync.py owner repo path/ -r main
```

---

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.


## Get Notes API（2026-05-15 重置）
GETNOTE_API_KEY=gk_liv...7d77
GETNOTE_CLIENT_ID=cli_a1b2c3d4e5f6789012345678abcdef90