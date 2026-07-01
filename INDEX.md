# Jan 的知识管理系统 🐉

> 三轨知识管理 · Obsidian Vault · 最后更新: 2026-07-01
> 重构版本 v3.1 | by Aclis
> 知识统一路线 · 新目錄重建（清乾淨 secrets）

---

## 🎯 系统架构（v3.1 新目錄重建）

```
📦 Jan 的知识管理系统（v3.1）
├── 00_Inbox/
├── 01_Daily/      ← AI 自動生成
├── 02_Knowledge/  ← 結構化資產（7 個分類）
├── 03_Insights/   ← llm-wiki 深度
├── 04_MOC/
├── 05_Outputs/
├── 06_System/
├── 07_Jan-知識庫/  ← llm-wiki 源頭
├── _workspace/    ← Aclis 執行區
│   ├── memory/
│   ├── daily_notes/
│   ├── SECURITY.md  ← 安全指南
│   └── 元檔
├── .gitignore     ← 防止 secrets 進 git
└── INDEX.md
```

---

## 🔄 變更日誌

### 2026-07-01 v3.1（本次）
- **新建 /workspace/jan-vault/**（取代 /workspace/obsidian_backup/）
- 全部 sanitize：移除真實 secrets（PAT / OAuth / API keys）
- 建立 .gitignore（防止未來 secrets 進 git）
- 建立 _workspace/SECURITY.md（提醒指南）
- 備份舊 vault 到 `/workspace/backup/before_new_dir_*/`

### 2026-07-01 v3.0（上一版，已廢棄）
- 合併兩個 .git
- 整合 4 個來源
- ❌ 因含 secrets 被 GitHub push protection 拒絕
- ❌ 備份保留，未 push 到遠端

### 2026-05-01 v2.0
- 目錄重構

---

*由 Aclis (小A) 重構 · 2026-07-01 · v3.1 新目錄重建*
