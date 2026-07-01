---
tags: [ #Semi/Packaging, #Concept, #AI/Hardware ]
created: 2026-05-01
updated: 2026-05-01
related-tags: [ #Semi/Memory, #Memory-Wall, #Entity/TSMC, #Entity/NVIDIA ]
---

# CoWoS（Chip on Wafer on Substrate）

> 先進封裝技術：將多顆晶片整合在同一封裝基板上。
> 不是簡單的「把晶片放在一起」，而是重建晶片之間的互聯方式。

## 核心定義

**CoWoS（Chip on Wafer on Substrate）**：台積電的先進封裝平台，全稱「晶片在基板上」。

**本質**：將邏輯晶片（GPU/CPU）與高頻寬記憶體（HBM）透過矽中介層（Silicon Interposer）整合在同一封裝中，大幅縮短晶片間距離。

```
     ┌─────────────────────────────┐
     │      基板（Substrate）       │
     │  ┌───────────────────────┐  │
     │  │   矽中介層            │  │
     │  │  ┌────┐    ┌────┐    │  │
     │  │  │GPU │────│HBM │    │  │
     │  │  │Die │    │Stack│   │  │
     │  │  └────┘    └────┘    │  │
     │  └───────────────────────┘  │
     └─────────────────────────────┘
```

## CoWoS 的兩種變體

| 變體 | 全稱 | 應用 | 中介層 |
|------|------|------|--------|
| **CoWoS-S** | Silicon Interposer | H100、GB200 | 矽中介層（最貴，效能最高） |
| **CoWoS-L** | Local Silicon Interposer | 部分 GB200 | 局部矽 + RDL（成本較低） |

**CoWoS-L 是 2025-2026 年的主力**，因為：
- 矽中介層面積越做越大，成本指數上升
- CoWoS-L 用局部連接替代全矽中介，維持足夠效能但降低成本
- 台積電 CoWoS 總產能 2025 年約 35K-40K/月，CoWoS-L 佔比越來越高

## 為什麼重要

### 解決 Memory-Wall 的物理方案
- GPU 運算單元與 HBM 的距離從 PCB 級（數十毫米）縮短到封裝級（不到 1 毫米）
- 訊號延遲大幅降低，頻寬利用率提升
- **沒有 CoWoS，就沒有 Hopper/Blackwell 時代的 AI 晶片**

### 台積電的策略性武器
- CoWoS 是台積電區別於純晶圓代工廠的核心差異化
- 毛利率極高（封裝毛利 > 60%），成為台積電新的成長引擎
- 客戶黏著度高：NVIDIA、AMD、蘋果都需要 CoWoS 來做 AI 晶片

## 供需瓶頸

**CoWoS 是 2024-2025 年 AI 晶片出貨的最大瓶頸**：

```
需求：
  NVIDIA GB200：CoWoS 封裝，每顆需要一個封裝槽位
  AMD MI350：CoWoS 封裝
  各大雲端廠自研晶片（Google TPU、AWS Trainium）

供給：
  台積電 CoWoS 總產能：~35-40K/月（2025 年中）
  其中 CoWoS-L 擴張速度快於 CoWoS-S

瓶頸緩解時間：
  預計 2026 年 H2 供需趨於平衡（若擴產順利）
```

## 與哪些概念相關

| 相關概念 | 關係 |
|---------|------|
| [[Memory-Wall]] | CoWoS 直接解決了記憶體牆問題 |
| [[HBM]] | HBM 必須透過 CoWoS 與 GPU 整合 |
| [[NVIDIA]] | 最大 CoWoS 需求方，GB200 需要 CoWoS |
| [[TSMC]] | CoWoS 的製造者 |
| [[Blackwell]] | 架構離不開 CoWoS 先進封裝 |

## 投資意涵

### 直接受益者
- **台積電（TSM/2330.TW）**：CoWoS 營收佔比提升，帶動毛利率上升
- **日月光（ASE/3711.TW）**：部分 CoWoS 後段測試/最終封裝
- **欣興（3037.TW）**：ABF 載板供應商

### 間接影響
- NVIDIA AI 晶片出貨量取決於台積電 CoWoS 產能
- **CoWoS 產能是觀察 AI 供應鏈健康的領先指標**

## 為什麼是這個選項（而非其他）

- ❌ **只關注 CoWoS 設備供應商** → 忽略了台積電的直接定價權
- ❌ **把 CoWoS 當成普通封裝** → 忽略了它需要與前端晶圓製造深度整合
- ✅ **從 AI 供應鏈瓶頸視角** → CoWoS 是整個 AI 晶片供應鏈的關鍵節點

---

*記憶宮殿位置：翼/Semi · 廳/Packaging · 房/CoWoS*