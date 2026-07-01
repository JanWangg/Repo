---
tags: [ #Semi/Memory, #Concept, #AI/Hardware ]
created: 2026-05-01
updated: 2026-05-01
related-tags: [ #Semi/Packaging, #Memory-Wall, #Entity/SK-Hynix, #Entity/NVIDIA ]
---

# HBM（High Bandwidth Memory）

> 解決 Memory-Wall 的關鍵封裝技術。
> DRAM 堆疊 + 矽通孔（TSV）+ 短距離傳輸 = 讓 GPU 不再等資料。

## 核心定義

**HBM**：將多層 DRAM 晶片垂直堆疊，透過矽通孔（TSV）電氣連接，再以 TCP（Through Silicon Via）封裝於 GPU 旁邊。

### HBM vs GDDR（傳統顯示記憶體）

| 維度 | GDDR6X | HBM3E |
|------|--------|-------|
| 頻寬/顆 | ~96 GB/s | ~1.2 TB/s |
| 功耗 | 較高 | 較低（同等頻寬下） |
| 面積 | 獨立顆粒 | 堆疊整合封裝 |
| 成本 | 低 | 高 |
| 主要應用 | 消費顯卡 | AI 訓練晶片 |

**關鍵差距**：HBM3E 頻寬是 GDDR6X 的 **12 倍**，但造價也是數倍。

## 技術架構

```
GPU Die
  │
  │ ← 矽中介層（Silicon Interposer）
  │
  ├── DRAM Die 1（HBM 堆疊）
  ├── DRAM Die 2
  ├── DRAM Die 3
  └── DRAM Die 4（4-high 或 8-high 堆疊）
  │
  └── Base Die（邏輯控制）
```

- **TSV（矽通孔）**：垂直穿過晶片的導電孔，讓電力/訊號從底部貫穿到頂層
- **矽中介層**：承載 HBM 堆疊的高速訊號轉發，訊號延遲極低
- **8-high 堆疊**：8 層 DRAM 垂直疊加，2025-2026 年量產

## 市場格局

| 廠商 | 市佔 | 技術狀態 | 合作對象 |
|------|------|---------|---------|
| **SK 海力士** | ~55% | HBM3E 領先量產，8-high 2025 | NVIDIA、AMD |
| **三星** | ~40% | HBM3E 追趕中，產能擴張 | NVIDIA（部分）、AMD |
| **美光** | ~5% | HBM3E 落後，但 High-NA EUV 佈局 | AMD |

### 為何 SK 海力士鶴立雞群？
1. **TSV 良率**：海力士 TSV 製程領先，8-high 堆疊良率最高
2. **與 NVIDIA 深度合作**：從 HBM2 時代開始綁定，共同最佳化
3. **封裝經驗**：CoWoS 配合台積電，與海力士 HBM 整合最順暢

## 與哪些概念相關

| 相關概念 | 關係 |
|---------|------|
| [[Memory-Wall]] | HBM 是解決方案 |
| [[CoWoS]] | 先進封裝容納 HBM |
| [[NVIDIA]] | 最大採購方（GB200 用 HBM3E） |
| [[Blackwell]] | 架構需要 HBM3E |

## 投資意涵

### 上游（記憶體廠）
- SK 海力士（000660.KS）：HBM 最大受益者，股價與 AI CapEx 高度相關
- 三星（005930.KS）：記憶體部門受惠，但內部業務複雜
- 美光（MU）：HBM 落後，彈性相對低

### 中游（封裝廠）
- 台積電（TSM）：CoWoS 封裝量能決定 HBM 滲透速度

### 下游（AI 晶片廠）
- NVIDIA：HBM 供應緊張 → 晶片出貨受限 → 供需缺口持續

## 為什麼是這個選項（而非其他）

- ❌ **把所有記憶體股當同質** → 忽略了 HBM 與一般 DRAM 的技術/毛利率差異
- ❌ **只看產能不看良率** → TSV 良率決定實際供應量
- ✅ **從 AI 供應鏈視角** → 將 HBM 視為緊缺的 AI 基礎設施元件

## 供需缺口模型

```
需求側（2025-2026）：
  NVIDIA GB200：每顆需要 8 顆 HBM3E
  AMD MI350：每顆需要 8 顆 HBM3E
  Google TPU / AWS Trainium：額外需求

供給側：
  SK 海力士：月產能 ~30K（2025）- 預計 50K（2026）
  三星：月產能 ~20K（2025）- 預計 35K（2026）
  美光：月產能 ~10K（落後）

結論：供需缺口可能持續到 2026 年底，價格維持高檔
```

---

*記憶宮殿位置：翼/Semi · 廳/Memory · 房/HBM*