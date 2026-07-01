---
tags: [ #Architecture, #AI/Hardware, #NVIDIA ]
created: 2026-05-02
updated: 2026-05-02
related-tags: [ #GB200, #GPU, #HBM3e, #CoWoS, #Blackwell-Architecture ]
---

# Blackwell 架構（Blackwell Architecture）

> NVIDIA 的第五代 GPU 架構，代號「Blackwell」（以統計學家 David Blackwell 命名）。
> 專為大規模 LLM 訓練與推理設計，GB200 是首款 Blackwell 架構產品，
> 透過 HBM3e 記憶體 + NVLink 5.0 + 新型 Transformer Engine，
> 在特定工作負載下號稱效能是 Hopper（H100）的 30 倍。

## 核心識別

|| 維度 | 內容 |
|------|------|
| **發布時間** | 2024 年 3 月（GTC 大會） |
| **代號由來** | David Blackwell（統計學家） |
| **前代架構** | Hopper（H100、A100） |
| **首款產品** | GB200（Grace Hopper Superchip） |
| **量產時間** | 2025 年下半年 |

## 架構設計目標

### 1. 解決 LLM 的 Memory-Wall 問題
- HBM3e 記憶體：每 GPU 192GB（vs H100 的 80GB）
- 記憶體頻寬：8TB/s（vs H100 的 3.35TB/s）
- **意義**：更大的模型無需頻繁在 GPU 和 CPU 之間交換資料

### 2. 加速 Transformer 運算
- 第五代 Transformer Engine
- 支援 FP4 精度（4 位元浮點），大幅降低記憶體需求
- 動態精度調配，硬體自動選擇最佳精度

### 3. 提升 Multi-GPU 擴展性
- NVLink 5.0：900GB/s 晶片間互聯（vs Hopper 的 900GB/s but 更高效率）
- NVSwitch 3：多 GPU 全互聯拓撲
- 目標：支援百萬級 GPU 叢集訓練

## GB200 規格表

```
GB200（Blackwell旗艦）：

CPU：2× NVIDIA Grace（ARM Neoverse）
GPU：2× Blackwell GPU（每顆 288 GB HBM3e）
總記憶體：576 GB HBM3e
GPU 間互聯：NVLink-C2C
系統功耗：~1200W（機櫃級）

vs H100 SXM：
記憶體：192GB vs 80GB（+140%）
記憶體頻寬：8TB/s vs 3.35TB/s（+139%）
Transformer 效能：聲稱 30x（特定工作負載）
```

## 為什麼重要（投資視角）

### 1. 驅動新一輪 CapEx 週期
- 雲端廠商（Microsoft、Google、AWS）需要升級到 Blackwell
- GB200 售價預計顯著高於 H100
- **結論**：NVIDIA 營收天花板再次提高

### 2. 鞏固 CoWoS 先進封裝需求
- GB200 需要台積電 CoWoS-L 先進封裝
- CoWoS 產能成為瓶頸（決定 NVIDIA 能交付多少 GPU）
- **結論**：CoWoS 供應商（台積電、日月光）持續受益

### 3. 拉動 HBM3e 需求
- GB200 每顆需要 192GB HBM3e
- SK 海力士、三星、美光爭奪 NVIDIA 訂單
- **結論**：HBM 廠商技術升級壓力持續

## 供應鏈受益順序

```
第一波（當下）：
└── 散熱解決方案廠商（液冷需求暴增）

第二波（2025-2026）：
├── 台積電（CoWoS 先進封裝）
├── SK 海力士（HBM3e 記憶體）
└── PCB/ABF 載板廠商

第三波（系統整合）：
└── 伺服器 ODM（鴻海、廣達、英業達）
```

## 與哪些概念相關

|| 相關概念 | 關係 |
|---------|--------|------|
| [[Memory-Wall]] | HBM3e 直接緩解 Memory-Wall | 解決方案 |
| [[HBM]] | GB200 需要最大容量 HBM3e | 記憶體配合 |
| [[CoWoS]] | 必須用 CoWoS 先進封裝 | 封裝配合 |
| [[NVIDIA]] | Blackwell 是 NVIDIA 最新架構 | 擁有者 |
| [[CUDA-Ecosystem]] | CUDA 持續優化 Blackwell | 軟體生態 |

## 為什麼是這個選項（而非其他）

- ❌ **只看 CUDA 生態** → 忽略硬體迭代對競爭格局的影響
- ❌ **只看 Blackwell vs H100 規格** → 忽略供應鏈瓶頸
- ✅ **從「整個供應鏈」的角度** → 理解誰在 Blackwell 浪潮中受益最深

## 關鍵事件追蹤

- [ ] GB200 量產進度（季度更新）
- [ ] 雲端廠商 GB200 訂單量
- [ ] 台積電 CoWoS 產能利用率
- [ ] HBM3e 供應商認證進度

---

*記憶宮殿位置：翼/Tech · 廳/AI-Hardware · 房/Blackwell*
