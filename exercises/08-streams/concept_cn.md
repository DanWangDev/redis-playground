# 练习 08：流

## 你将学到
- 使用 `XADD` 追加条目
- 使用 `XREAD` 和 `XRANGE` 读取条目
- 使用 `XGROUP CREATE` 创建消费者组
- 使用 `XREADGROUP` 以消费者组身份读取
- 使用 `XACK` 确认消息
- 使用 `XPENDING` 检查待处理条目

## 为什么重要
Redis Streams 是 Pub/Sub 的持久化、可靠替代方案。提供带有消费者组的追加日志，用于扇出消息传递、消息确认和待处理消息检查。

## 常见陷阱
- XREAD 不感知消费者组——使用 XREADGROUP 进行可靠投递。
- 未确认的消息会永远保留在 PEL 中。
- Stream 会无限增长——使用 MAXLEN 或 XTRIM 进行限制。
