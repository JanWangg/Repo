# maxHermes v1.0 GA 自動觸發 prompt

執行半導體晨報標準流程：

1. 跑 `/userspace/skills/semicon-morning-report/scripts/semicon-runner.py`
2. 如有 Handoff 觸發，跑 `/root/.hermes/skills/actuary-expert/scripts/actuary-runner.py consume`
3. 摘要：晨報 note_id + 紅線觸發清單 + Handoff 派發結果

回報格式：
- 晨報狀態：success / partial / failed
- M1-M5 紅線觸發清單
- Handoff 數量
- GetNotes note_id
- Obsidian 路徑
- Buffer 路徑
