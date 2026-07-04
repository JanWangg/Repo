# 🛠️ Skill 備份 · huashu-nuwa/references/README.md

> **備份日期**：2026-07-04
> **來源路徑**：`/workspace/skills/huashu-nuwa/references/README.md`
> **Skill**：huashu-nuwa · 女媧造人
> **KB**：🛠️ 技能模板（`JOaEOM5Y`）
> **管理員**：Aclis 🐉

---

# 女媧 Skill · 使用指引

## 安裝位置

```
/userspace/skills/huashu-nuwa/
```

> **重要**：`/workspace/skills` 是壞掉的符號連結（指向 `/userspace/skills`）。所有 skill 必須放在 `/userspace/skills/`。

## 觸發詞

| 類型 | 範例 |
|------|------|
| 明確人名 | 「蒸餾芒格」「做一個費曼 skill」「女媧蒸餾張一鳴」 |
| 主題 | 「做個反脆弱決策 skill」「主題 skill：長期主義」 |
| 模糊需求 | 「我想提升決策品質」「有沒有一種思維方式能幫我看透商業」 |
| 更新 | 「更新馬斯克的 skill」「王陽明 v2」 |

## 快速開始

### 範例 1：蒸餾新人物
```
你：女媧，蒸餾一個「張一鳴」的 skill
Claude：
  → 確認人名（張一鳴，字節跳動創辦人）
  → 確認用途（思維顧問/決策參考/角色扮演）
  → 啟動 Phase 1 6 個並行 Agent
  → Phase 2 降維
  → Phase 3 組裝 SKILL.md
  → Phase 4 品質驗證
  → 輸出：/userspace/skills/zhangyiming-perspective/SKILL.md
```

### 範例 2：模糊需求 → 推薦
```
你：我總是做決定太慢，分析癱瘓
Claude：
  → 詢問 1 個場景問題
  → 推薦 2-3 個候選（已有 skill 優先）
  → 用戶選擇後啟動蒸餾
```

### 範例 3：更新既有
```
你：更新馬斯克 skill
Claude：
  → 讀取現有 /userspace/skills/elon-musk-perspective/SKILL.md
  → 只啟動 Agent 2/5/6（最新對話、決策、時間線）
  → 增量更新，不重寫整個 skill
```

## 對話風格

女媧是**思維教練 + 框架工程師**的混合體：
- 對蒸餾對象保持中立（不神化也不貶低）
- 對用戶保持直接（不囉嗦、不廢話）
- 失敗時誠實承認（資訊不足就說，不編造）

## 與其他 Skill 的關係

- **find-skills**：發現可用的 skill（推薦先用它）
- **skill-creator**：建立新 skill 的通用流程（女媧是專門的人物 skill 蒸餾版）
- **clawhub**：發布/下載 skill 的工具

## 限制

- 不支援本地影片檔案的轉寫（用戶需提供字幕或 transcript）
- 不蒸餾**非公開人物**（無公開資訊無法搜尋）
- 不蒸餾**活著的隱私人物**（倫理邊界）


---

_Aclis 🐉 自動備份 · 2026-07-04 08:00 UTC_
