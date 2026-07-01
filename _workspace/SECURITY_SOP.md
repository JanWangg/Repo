# 🔐 數據安全 SOP — Aclis 操作手冊

> 建立時間：2026-03-23
> 版本：v1.1
> 維護人：Aclis 🐉
> 最後更新：2026-07-01（新增「Commit 前 Secrets 掃描」）

---

## 一、敏感憑證管理

### 存放位置
所有敏感憑證**只存放於**：
- `/workspace/TOOLS.md`（主要）
- `/workspace/skills/credentials/`（子目錄，嚴格隔離）

### 嚴禁事項
```
❌ 嚴禁將憑證寫入 Log、Session 歷史、筆記正文
❌ 嚴禁通過 API 將憑證發送到外部服務
❌ 嚴禁在 GitHub 提交中包含真實 API Key
❌ 嚴禁將憑證寫入 multi_agent/*.md 研究文件
❌ 嚴禁將 Get Notes 原始素材（_raw_getnotes/*.json）commit 進 git
```

### Commit 前 Secrets 掃描（v1.1 新增）

**自動觸發：** 每次 `git commit` 前
**掃描範圍：** staged files
**Pattern 清單：**
```python
SECRET_PATTERNS = [
    r'ghp_[A-Za-z0-9]{20,}',              # GitHub PAT (classic)
    r'github_pat_[A-Za-z0-9_]{20,}',      # GitHub PAT (fine-grained)
    r'AIza[0-9A-Za-z_\-]{30,}',           # Google API Key
    r'[0-9]+-[0-9A-Za-z_\-]{20,}\.apps\.googleusercontent\.com',  # Google Client ID
    r'GOCSPX-[A-Za-z0-9_\-]{20,}',        # Google Client Secret
]
```

**處理流程：**
1. 掃描命中 → 拒絕 commit，列出位置
2. Aclis 自動 sanitize（用 `***REDACTED***` 取代）
3. 重新 commit
4. 仍失敗 → raise 給 Jan 人工處理

**事故案例（2026-07-01）：**
第一次 push v3.0 → 被 GitHub Push Protection 擋下
原因：`_workspace/memory/2026-04-05.md` 含 Google OAuth Client Secret
+ `_workspace/TOOLS.md` 含舊 PAT
+ `07_Jan-知識庫/_raw_getnotes/*.json` 含別人分享的 credentials

教訓：
- 凡 `_raw_getnotes/` 不進 git（已加 .gitignore）
- 凡 .md 引用 secrets 用 placeholder（已加 SECURITY.md）
- 凡 commit 前必掃

### 輪換週期
| 憑證 | 週期 | 負責人 |
|------|------|--------|
| Get Notes API Key | 每季（90天） | Aclis 主動提醒 |
| GitHub PAT | 每季（90天） | Jan 手動更新 |
| Telegram Bot Token | 每半年 | Jan 手動更新 |

---

## 二、API 配額管理

### 警戒線設定
| API | 限額 | 黃線 | 紅線 | 行動 |
|-----|------|------|------|------|
| Get Notes 讀取 | 1,000/天 | 60% → 600 | 80% → 800 | 立刻停止非必要讀取 |
| Get Notes 寫入 | 500/天 | 60% → 300 | 80% → 400 | 批次排程化 |
| Get Notes 寫入筆記 | 50/天 | 60% → 30 | 80% → 40 | 合併寫入，禁止單篇分散 |

### 配額檢查頻率
- 每 4 小時一次（通過 HEARTBEAT）
- 黃線觸發：記錄，不中斷
- **紅線觸發：立刻告知 Jan**

---

## 三、日誌與敏感資料規範

### 允許寫入日誌的內容
```
✅ 成功/失敗狀態（不含內容）
✅ 處理的筆記數量統計
✅ 時間戳和執行時長
✅ 錯誤代碼和類型
```

### 嚴禁寫入日誌的內容
```
❌ API 回應的原始內容（包含用戶數據）
❌ 筆記正文內容
❌ note_id 列表（隱私）
❌ API Key、Token、Client ID（任何完整憑證）
```

### 指令日誌輸出格式
```python
# 正確示範
print(f"✅ 寫入成功 | nid={note_id} | title=讀書晨報")

# 錯誤示範（嚴禁）
print(f"✅ 寫入成功 | content={note['content']}")
print(f"✅ API回應: {response}")
```

---

## 四、跨平台數據流動

### 允許的數據流動
```
Get Notes → GitHub（晨報備份）
Get Notes → Obsidian Vault（知識沉澱）
Cron Job 產出 → Get Notes 收集箱
GitHub → 本地 Vault（雙向同步）
```

### 需要 Jan 確認的數據流動
```
飛書 Wiki → OpenClaw（涉及第三方數據）
企業微信 → OpenClaw（涉及企業數據）
任何外部服務的主動推送
```

---

## 五、突發安全事故應變

### 等級分類

| 等級 | 定義 | 應變時間 |
|------|------|---------|
| 🔴 P0 | 憑證疑似外洩 | 立刻告知 Jan，停止所有 API |
| 🟡 P1 | API 配額連續 429 或 500 | 4小時內定位，12小時內修復 |
| 🟢 P2 | 單次 API 錯誤 | 下一心跳主動告知 |

### P0 應變流程
```
1. 立刻阻斷：停止所有對外的 API 調用
2. 立刻告知：向 Jan 報告（不受心跳節制）
3. 評估影響：確認哪些數據可能外洩
4. 補救措施：更換 API Key / Token
5. 根因分析：寫事故報告（DAMAIC）
```

---

## 六、備份與還原

### 每日自動化備份
- 00:00 UTC：C全量備份（GitHub API Push）
- 晨報完成後：立刻寫入 GitHub

### 手動備份觸發條件
```
- 大量筆記寫入後（>50篇）
- 系統變更前（插件更新、配置修改）
- 任何非預期錯誤發生後
```

---

## 七、審查機制

### 每月常規審查
- API 配額使用趨勢
- 憑證有效期檢查
- Log 規範遵守情況
- SOP 更新需求

---

*本 SOP 由 Aclis 維護，每季審查一次。*
*最後更新：2026-07-01 v1.1 by Aclis 🐉
*
*重大更新：新增「Commit 前 Secrets 掃描」機制（事故案例 2026-07-01）*