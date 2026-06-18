# 练习 25：RedisTimeSeries

## 你将学到
- 使用 TS.CREATE 创建时间序列
- 使用 TS.ADD 添加数据点
- 使用 TS.RANGE 查询范围

## 为什么重要
RedisTimeSeries 是专用的时间序列模块，提供自动降采样和保留策略。

## 常见陷阱
- 时间戳是 Unix 纪元毫秒
- 需要 Redis Stack
