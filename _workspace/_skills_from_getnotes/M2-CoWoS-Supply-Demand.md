# 🛠️ Skill 備份 · M2-CoWoS-Supply-Demand.md

> **備份日期**：2026-07-04
> **來源路徑**：`/workspace/skills/semicon-morning-report/references/models/M2-CoWoS-Supply-Demand.md`
> **KB**：🛠️ 技能模板（`JOaEOM5Y`）
> **管理員**：Aclis 🐉

---

# M2｜CoWoS 供需缺口模型

> 先進封裝缺口量化 — 半導體超級週期的**最大瓶頸**

## 核心公式

$$\text{缺口\%} = \frac{D(t) - S_{\text{actual}}(t)}{D(t)} \times 100\%$$

其中：
- $D(t)$ = 終端需求（wafer per month, WPM）
- $S_{\text{actual}}(t)$ = 實際產能
- $S_{\text{design}}(t)$ = 設計產能（理輪最大值）

## 標準供需表（v6.1，2026-07-04 更新）

| 時間 | 設計產能 | 實際 | 需求 | 缺口 | 來源 |
|------|---------|------|------|------|------|
| 2025 底 | 65K | 60K | 75K | -20% | TSMC IR |
| 2026 中 | 95K | 82K | 100K | -18% | Digitimes |
| 2026 底 | **130K** | **105K** | 115K | **-9%** | TSMC Q2 2026 |
| 2027 中 | 130K | 130K | 130K | 平衡 | TSMC Roadmap |

## 關鍵變數

### 需求端
- **NVIDIA Blackwell**：2026 全年需求 ~50K WPM
- **NVIDIA Rubin**：2027 接力，再增加 ~30K WPM
- **AMD MI300/MI400**：~15K WPM
- **Broadcom/AVGO 客製晶片**：~15K WPM（Google TPU、Meta MTIA）

### 供給端
- **TSMC**：CoWoS-S / CoWoS-L / CoWoS-R 三線並進
- **ASE / Amkor**：CoWoS-S 輔助產能 ~10K WPM
- **新技術**：CoPoS / SoIC（2027 量產）

## 異常偵測規則

| 異常類型 | 觸發條件 | 警示等級 |
|---------|---------|---------|
| 產能下修 | 公告產能 < 上月預期 10% | 🔴 |
| 需求上修 | 新客戶/新晶片使需求 > 預期 15% | 🟡 |
| 平衡提前 | 達平衡時間 < 預期 6 月 | 🟢（週期短） |
| 平衡延後 | 達平衡時間 > 預期 6 月 | 🔴（週期延長） |

## 在晨報中的應用

M2 是**最關鍵的供需指標**：
- 缺口收斂 → 超級週期接近尾聲
- 缺口擴大 → 超級週期延長，受惠股（HBM/設備/封裝）持續強勢

**訊號組合判讀**：
- 🔴 M2 缺口 + 🔴 M3 EUV 交期長 = 雙瓶頸，最強訊號
- 🟢 M2 缺口收斂 + 🟡 M3 設備市場仍成長 = 進入末升段

---

_Aclis 🐉 自動備份 · 2026-07-04 07:51 UTC_
