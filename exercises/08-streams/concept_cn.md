# 练习 08：流

## 你将学到

- 使用 `XADD` 向流中添加条目
- 使用 `XREAD` 读取条目（非消费者组模式）
- 使用 `XGROUP CREATE` 创建消费者组
- 使用 `XREADGROUP` 以消费者组身份读取
- 使用 `XACK` 确认消息
- 使用 `XPENDING` 检查待处理条目
- 使用 `XRANGE` 按范围查询

## 为什么重要

Redis Streams 是 Pub/Sub 的持久化、可靠替代方案。它提供带有消费者组的追加日志，支持扇出消息传递、消息确认（ACK）和待处理消息检查。这是事件溯源、可靠任务队列和微服务通信的基础。

## 核心概念

### Stream 作为追加日志

```
XADD events * type "page_view" user "alice"
XADD events * type "purchase" user "bob" amount 49.99
```

`*` 让 Redis 自动生成条目 ID（时间戳-序号对，如 `1680000000000-0`）。

### 消费者组

```
XGROUP CREATE events mygroup $ MKSTREAM
XREADGROUP GROUP mygroup consumer-1 COUNT 2 STREAMS events >
XACK events mygroup 1680000000000-0
```

- `>` 表示"给我从未投递给该组中任何消费者的消息"
- 消费者组允许多个独立的应用读取同一个流

## 常见陷阱

- **XREAD 不感知消费者组**：使用 XREADGROUP 进行可靠投递。
- **未确认的消息永远存在**：如果从不 ACK，消息将无限期保留在 PEL 中。
- **消费者组需要显式创建**：`XGROUP CREATE` 在组已存在时会失败。
- **Stream 修剪**：Stream 会无限增长。使用 `MAXLEN` 配合 XADD 或 `XTRIM` 进行限制。
