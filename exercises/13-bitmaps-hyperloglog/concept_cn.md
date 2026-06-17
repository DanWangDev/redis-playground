# 练习 13：位图和 HyperLogLog

## 你将学到
- 使用 `SETBIT` / `GETBIT` 设置/获取单个位
- 使用 `BITCOUNT` 计数设置的位
- 使用 `BITOP` 执行按位操作
- 使用 `PFADD` / `PFCOUNT` 估算唯一计数
- 使用 `PFMERGE` 合并 HyperLogLog

## 为什么重要
位图提供紧凑的布尔存储——在 125KB 中追踪 100 万日活用户。HyperLogLog 提供概率性唯一计数，误差约 0.81%，每个键仅使用 12KB。它们共同支持分析仪表板、A/B 测试追踪和独立访客计数。

## 常见陷阱
- HLL 是概率性的——PFCOUNT 有约 0.81% 的误差，不是精确值。
- BITCOUNT 是 O(N)——在大位图上使用子范围进行增量计数。
- 无法检索单个 HLL 元素——它是计数器，不是集合。
