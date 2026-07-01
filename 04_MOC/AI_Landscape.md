# AI生态全景图 (AI Landscape)

```
                    ┌─────────────────┐
                    │   🤖 AI生态     │
                    └────────┬────────┘
                             │
     ┌──────────┬───────────┼───────────┬──────────┐
     ▼          ▼           ▼           ▼          ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ 🧠 基础 │ │ 📱 应用 │ │ ⚙️ 硬件 │ │ 🏛️ 治理 │ │ 💰 投资 │
│  模型   │ │   层    │ │   层    │ │         │ │         │
└────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘
     │           │           │           │           │
  LLM/GPT    Agent/RAG   GPU/芯片   安全/伦理   AI股票
  Transformer  多模态    HBM/封装   AI法规     相关ETF
  RL/Alignment RAG       云计算    版权问题   算力需求
```

## 核心节点

### 🧠 基础模型层
- **LLM**: GPT-4 / Claude / Gemini / Llama
- **架构**: Transformer / MoE / Long Context
- **训练**: RLHF / Alignment / Fine-tuning
- **上下文**: 128K / 1M tokens

### 📱 应用层
- **Agent**: 自动化执行 / 工具调用
- **RAG**: 检索增强生成
- **多模态**: 图生文 / 文生图 / 视频生成
- **垂直应用**: 医疗 / 金融 / 制造

### ⚙️ 硬件层
- **GPU**: H100 / H200 / B100 / MI300X
- **封装**: CoWoS / HBM3e / 3D堆叠
- **制程**: 3nm → 2nm → 1.4nm
- **云**: AWS / Azure / GCP / 自建算力

### 🏛️ 治理层
- AI安全 / 对齐问题
- 版权归属 / 训练数据
- 监管框架 / EU AI Act
- 开源 vs 闭源之争

### 💰 投资层
- **芯片**: NVIDIA / AMD / Intel / Qualcomm
- **云**: MSFT / GOOGL / AMZN / META
- **应用**: C3.ai / Palantir / Salesforce
- **算力租赁**: CoreWeave / AI Holding

## 关键关系

```
NVIDIA H100 ──驱动→ LLM训练规模
    │
    ▼
GPU产能 ──瓶颈→ CoWoS封装 ──瓶颈→ TSMC先进制程
    │
    ▼
HBM供应 ──瓶颈→ SK海力士/三星 ──影响→ AI芯片出货
```

## 相关笔记
- [[../01_Knowledge/011_AI_Tech/README]]
- [[../01_Knowledge/012_Semiconductor/README]]
- [[../02_Daily_Briefing/Semiconductor_*.md]]

## 更新日志
- 2026-04-16: 初版创建
- 2026-04-19: 🐉姐姐蒸馏W16周报+四月LLM混战专题

---
*标签: #AI生态 #NVIDIA #LLM #GPU #投资*
