---
tags: [ #Semi/Memory, #Concept, #AI/Hardware ]
created: 2026-05-01
updated: 2026-05-01
related-tags: [ #Semi/Packaging, #AI/LLM, #Entity/NVIDIA, #Entity/TSMC ]
---

# Memory-Wall（記憶體牆）

> AI 訓練的硬體瓶頸不是算力，而是記憶體頻寬。
> 摩爾定律讓運算快 1000 倍，但記憶體頻寬只快了 100 倍——這個差距就是 Memory-Wall。

## 核心定義

**Memory-Wall（記憶體牆）**：CPU/GPU 的計算速度與記憶體訪問速度之間持續擴大的差距。

- 1980 年代：處理器速度 vs 記憶體速度幾乎同步
- 2020 年代：旗艦 GPU（GB200）運算能力：~20 PFLOPS，但 HBM 頻寬：~8 TB/s
- 這個差距意味著：**GPU 有大量時間在「等資料」，而非「算資料」**

## 為什麼重要

### AI 訓練瓶頸
- Transformer 模型：每次 attention 計算都需要讀取龐大的權重矩陣
- LLM 訓練：記憶體頻寬直接限制 batch size 和序列長度
- 沒有足夠的頻寬，再強的運算單元也是英雄無用武之地

### 解決方案演進
1. **HBM（High Bandwidth Memory）**：將 DRAM 堆疊在 GPU 封裝旁邊，大幅縮短資料傳輸距離
2. **CoWoS（Chip on Wafer on Substrate）**：用矽中介層將 HBM 和 GPU 整合在同一封裝
3. **新型態計算**：近記憶體計算、類比 AI 晶片（繞過傳統馮紐曼瓶頸）

## 與哪些概念相關

| 相關概念 | 關係 |
|---------|------|
| [[HBM]] | Memory-Wall 的直接解方 |
| [[CoWoS]] | HBM 與 GPU 整合的封裝技術 |
| [[CUDA-Ecosystem]] | NVIDIA 生態如何利用 Memory-Wall 設計硬體 |
| [[NVIDIA]] | GB200 針對 Memory-Wall 的架構優化 |
| [[TSMC]] | CoWoS 先進封裝的主要製造者 |

## 反覆出現的場景

### 場景1：HBM3E 缺貨影響 AI 晶片產能
- 2024-2025 年，HBM3E 供應緊張，NVIDIA/AMD 晶片出貨受限
- SK 海力士、三星、美光三家壟斷，擴產需要 12-18 個月
- **這就是 Memory-Wall 的商業表現：頻寬元件決定整個供應鏈節奏**

### 場景2：SK 海力士成為 AI 贏家
- HBM 市場佔比：SK 海力士 ~55%、三星 ~40%、美光 ~5%
- 海力士股價在 2023-2024 年大漲，因為它掌握了 Memory-Wall 的關鍵元件
- **投資意涵**：記憶體頻寬供應商有定價權

## 為什麼是這個選項（而非其他）

- ❌ **只關注摩爾定律** → 忽略了記憶體進步相對緩慢的事實
- ❌ **只看算力 FLOPS** → 沒有理解實際訓練瓶頸在頻寬
- ✅ **同時關注算力 + 頻寬** → 完整評估 AI 硬體的真實效能

## 關鍵數據

| 指標 | HBM2E | HBM3 | HBM3E |
|------|-------|------|-------|
| 頻寬/顆粒 | ~460 GB/s | ~819 GB/s | ~1.2 TB/s |
| 功耗 | 高 | 中 | 低（相對） |
| 主要廠商 | 三星 | SK海力士 | SK海力士領先 |
| 應用節點 | A100 | H100 | GB200 |

---

*記憶宮殿位置：翼/Semi · 廳/Memory · 房/Memory-Wall*