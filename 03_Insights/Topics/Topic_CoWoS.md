# 🔧 CoWoS 先進封裝

> TSMC Chip-on-Wafer-on-Substrate 先進封裝技術

## 核心定位

CoWoS 是 TSMC 的核心先進封裝技術，用於將多顆晶片（Compute + HBM）整合在同一封裝內，解決**晶片間互連頻寬瓶頸**。是 AI 晶片（尤其是 NVIDIA Hopper/Blackwell 系列）不可或缺的關鍵技術。

## 2026 年產能擴張

| 時間 | CoWoS 月產能 |
|------|------------|
| 2025 年中 | ~40,000 片 |
| 2026 年初 | 60,000 片 |
| **2026 年底目標** | **130,000 片**（+117%） |

## 市場動態

- **NVIDIA 包廠**：NVIDIA 已預訂 TSMC CoWoS 2026-2027 年過半產能（>50%）
- **ASE 呼應擴廠**：日月光（ASE）同步擴張先進封裝產能
- **產能吃緊**：AI 晶片訂單如潮水般湧入，CoWoS 供不應求格局延續至 2027 年

## 技術演進

- **CoWoS-S**：Silicon Interposer，頻寬最高，成本也最高
- **CoWoS-R**：Redistribution Layer，較低成本，2025 年主流
- **CoWoS-L**：Local Silicon Bridge，介於兩者之間

## 與 HBM 的關係

CoWoS 是承載 HBM 的關鍵介面：
```
GPU Die ←→ CoWoS Interposer ←→ HBM Stack
```
沒有 CoWoS，HBM 再強也無法與 GPU 高效互連。

## 關鍵公司

| 公司 | 角色 |
|------|------|
| TSMC | CoWoS 主要生產者 |
| NVIDIA | 最大採購方（GB200 / B300 系列） |
| ASE（日月光） | 後段封測協力廠 |
| 長電科技 | 中國客戶協力廠 |

## 投資觀察點

- CoWoS 擴產速度是否追得上 AI 晶片需求增速？
- Rubin 系列對 CoWoS 規格需求是否升級？
- 中國封測廠（如長電）是否有能力突破？

## 關聯主題

- [[HBM]] — CoWoS 的親密夥伴
- [[NVIDIA]] — 最大需求方
- [[半導體設備]] — 擴產受益者

---

*Last updated: 2026-04-28*