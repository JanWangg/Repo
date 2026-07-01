# 🔐 安全性指南

## ⚠️ 千萬不要做的事

1. **不要在 .md / .txt / .json 裡寫 secrets**
   - GitHub PAT、API Key、OAuth Secret、密碼
2. **不要把 .env 檔 commit 進 git**
3. **不要截圖含 secrets 的畫面進 vault**

## ✅ 安全做法

1. **Secrets 統一存在環境變數**
   ```bash
   export GITHUB_TOKEN=ghp_xxx
   export GOOGLE_CLIENT_SECRET=xxx
   ```

2. **或存在 vault 外的檔案**
   - `/root/.credentials/`（已有）
   - 本地 `.env`（加進 .gitignore）

3. **在 .md 裡引用時用 placeholder**
   - ✅ `ghp_***REDACTED***`
   - ✅ `<your-pat-here>`
   - ❌ 真實 token 字串

## 🛡️ 如果不小心 commit 了 secret

1. **立刻 rotate**（撤銷 + 重生）
2. 從 git 歷史移除（`git filter-repo`）
3. force push
4. 確認遠端無殘留

## 📋 Aclis 自動檢查

- commit 前會掃描 secrets pattern
- 偵測到 → 警告 + 拒絕 commit
