# 练习 03：哈希

## 你将学到

- 使用 `HSET` 将对象存储为字段-值对
- 使用 `HGET`、`HGETALL`、`HMGET` 获取字段
- 使用 `HINCRBY` 进行原子字段递增
- 使用 `HDEL` 删除字段
- 使用 `HEXISTS`、`HLEN`、`HKEYS`、`HVALS` 检查哈希结构

## 为什么重要

Redis 哈希是存储对象的主要方式（用户资料、产品目录、会话数据）。与将 JSON 存储为字符串不同，哈希允许对单个字段进行原子操作——你可以在不读取整个对象的情况下递增计数字段。它们内存效率高：小型哈希（约少于 512 个字段）使用紧凑的 ziplist 编码，可节省大量内存。

## 核心概念

### 对象即哈希模式

```
HSET user:1 name "Alice" email "alice@example.com" age 28 plan "pro"
```

相当于 SQL：
```sql
INSERT INTO users (id, name, email, age, plan)
VALUES (1, 'Alice', 'alice@example.com', 28, 'pro');
```

但与 SQL 不同，你可以原子性地执行 `HINCRBY user:1 age 1`，无需先读后写带来的竞态条件。

## 常见陷阱

- **HGETALL 是 O(N)**：返回所有字段和值。对于数百万字段的哈希，这很昂贵。使用 `HSCAN` 处理大型哈希。
- **HINCRBY 用于非数值**：如果字段包含非数值数据，会报错。
- **HSET 覆盖**：设置已存在的字段会静默覆盖其值。
- **字段被删除后消失**：对已删除字段的 `HGET` 返回 `None`。`HEXISTS` 返回 0。当最后一个字段被删除时，哈希本身也被删除。
