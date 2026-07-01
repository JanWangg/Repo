# DeepSeek-V3 的多头潜在注意力（MLA）架构分析

## 核心创新

DeepSeek-V3 采用了**多头潜在注意力（Multi-Head Latent Attention, MLA）**机制，这是其区别于标准 Transformer 的关键架构创新。

### 与 MHA 的对比

| 维度 | MHA | MLA |
|------|-----|-----|
| 参数量 | O(d·h·n) | O(d·h) 压缩 |
| KV Cache | O(n·h·d) | O(d·h) 潜在向量 |
| 推理效率 | 低 | 高 |

### 低秩联合压缩

MLA 的核心思想是将传统的键值对 (Key-Value) 压缩到一个低维潜在空间中：

```
Q = W_Q · x
K = W_K · x  
V = W_V · x
↓ 潜在压缩
KV_latent = W_KV · [K; V]
```

### 推理优化

通过将 KV 缓存压缩为低秩潜在向量，MLA 显著降低了长上下文推理时的内存占用，使得部署成本大幅下降。

## 对国产大模型的启示

1. 架构创新比堆参数更有效
2. 低秩近似是工程可行的优化方向
3. MLA 可与 MoE 结合进一步提升效率

## 来源

技术报告：DeepSeek-V3 Technical Report，2024年12月
