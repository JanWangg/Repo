# 💾 HBM 高頻寬記憶體

> High Bandwidth Memory，AI 軍備競賽的核心彈藥

## 核心定位

HBM 是 AI GPU 的「記憶體牆」解方。傳統 DDR/GDDR 頻寬遠遠無法滿足 LLM 訓練與推理的資料傳輸需求。HBM 通過 3D 堆疊封裝，將多顆 DRAM 晶片垂直堆疊，實現超高速頻寬。

## 2026 年超級週期確認

| 指標 | Q1 2026 數據 | 備註 |
|------|------------|------|
| DRAM 現貨價季漲幅 | **+80-95%** | 歷史罕見 |
| 64GB DDR5 RDIMM 季增 | **+150%** | 伺服器記憶體 |
| Gartner 記憶體 2026 營收 | **+125% YoY** | |
| 儲存晶片市場 | **+234% YoY** | Gartner 預測 |
| 全球記憶體市場規模（2026） | ~$3,000 億 | 美銀上調 |

## 主要廠商與規格

| 廠商 | HBM 世代 | 目標 AI 晶片 |
|------|---------|------------|
| **SK Hynix** | HBM3E（12層） | NVIDIA B200/B300, AMD MI350 |
| **Samsung** | HBM3E（12層） | 自用 + 其他 CSP |
| **Micron** | HBM3E | NVIDIA, Intel Gaudi 3 |

SK Hynix 目前是 NVIDIA HBM3E 的獨家供應商，市場份額領先。

## 與 GPU 的綁定關係

```
HBM3E specs:
- 頻寬：>1.2 TB/s（vs DDR5 的 ~100 GB/s）
- 功耗：每顆 ~1W per GB/s bandwidth
- 單片容量：24Gb（3GB per stack layer）× 12層 = 36GB per stack
```

NVIDIA B200 使用 8 顆 HBM3E（8×36GB = 288GB），頻寬總計 ~9.6 TB/s。

## 投資觀察點

- **HBM3E 良率**：12 層堆疊良率仍是瓶頸
- **CoWoS 配合**：HBM 需要 CoWoS 介面，兩者共同構成長邏輯+記憶體 combo
- **中國廠商進度**：長江存儲、長鑫存儲 HBM 開發落後國際 2-3 代
- **定價權**：HBM 現貨價 vs 合約價的價差是否存在套利空間？

## 關聯主題

- [[CoWoS]] — HBM 的封裝介面
- [[NVIDIA]] — 最大採購方
- [[半導體景氣循環]] — 記憶體週期框架

---

*Last updated: 2026-04-28*