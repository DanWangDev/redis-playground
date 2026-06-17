# 练习 02：字符串

## 你将学到

- 使用 `INCR`、`DECR`、`INCRBY` 进行原子计数器操作
- 使用 `MSET` 和 `MGET` 进行批量操作
- 使用 `GETRANGE` 和 `SETRANGE` 进行字符串切片
- 使用 `SETNX` 进行原子性的"不存在则设置"
- 字符串元数据：`STRLEN`、`APPEND`

## 为什么重要

Redis 字符串不仅用于文本——它们处理计数器、缓存值、序列化的 JSON 和二进制数据。原子递增操作（`INCR`/`DECR`）是限流器、浏览计数器和库存系统的基础。`MSET`/`MGET` 将多个操作批量合并为单次往返，对性能至关重要。

## 核心概念

### 计数器是原子的

与应用代码中的 `GET` → 递增 → `SET` 不同，`INCR` 是单个原子操作。如果两个客户端同时调用 `INCR views`，Redis 保证计数器增加 2——不会丢失更新。

### 批量操作减少往返延迟

```
# 未批量化：3 次网络往返
SET user:1:name "Alice"
SET user:1:email "alice@example.com"
SET user:1:plan "pro"

# 使用 MSET：仅 1 次往返
MSET user:1:name "Alice" user:1:email "alice@example.com" user:1:plan "pro"
```

每次往返增加约 0.5-2ms 的网络延迟。`MSET`/`MGET` 消除了这些开销。

### SETNX 用于分布式锁（预览）

`SETNX key value` 仅在键不存在时设置。这是分布式锁的基础原语（详见练习 18）。

## 常见陷阱

- **对非整数使用 INCR**：对值为 "hello" 的键使用 `INCR` 会返回错误。先用 `TYPE` 检查。
- **INCR 会创建键**：对不存在的键使用 `INCR` 会先创建值为 0 的键，然后递增到 1。
- **GETRANGE 是闭区间**：`GETRANGE key 0 4` 返回第 0 到第 4 个字符（共 5 个字符）。
- **字符串最大大小**：512 MB。不要将大对象存储在 Redis 中——使用对象存储（S3、GCS），将 URL 存放在 Redis 中。
