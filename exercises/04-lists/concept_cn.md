# 练习 04：列表

## 你将学到

- 使用 `LPUSH` + `RPOP` 构建队列（FIFO）
- 使用 `LPUSH` + `LPOP` 构建栈（LIFO）
- 使用 `LRANGE` 检查范围
- 使用 `LTRIM` 限制集合大小
- 使用 `BLPOP` / `BRPOP` 在空列表上阻塞等待
- 使用 `LLEN` 获取长度

## 为什么重要

Redis 列表是链表，不是数组。它们针对头/尾操作进行了优化（O(1)），但基于索引的访问较慢（O(N)）。这使得它们非常适合队列、栈、动态流和任务系统。阻塞弹出操作（`BLPOP`/`BRPOP`）使工作池无需忙等待轮询。

## 核心概念

### 队列与栈

```
# 队列（FIFO）：LPUSH + RPOP
LPUSH queue "task1" "task2"      # 任务按顺序等待
RPOP queue                        # "task1"（先进先出）

# 栈（LIFO）：LPUSH + LPOP
LPUSH stack "page1" "page2"      # 页面被压入
LPOP stack                        # "page2"（后进先出）
```

## 常见陷阱

- **LRANGE 是 O(S+N)**：起始偏移量越大越慢。在巨大列表上使用 `LRANGE list 0 -1` 代价高昂。
- **LTRIM 是 O(N)**：只计被删除的元素。将百万级列表裁剪到 10 个很快（只保留 10 个）。
- **BLPOP 超时设为 0** 表示无限期阻塞——在单线程代码中要小心。
- **列表不是数组**：随机访问（`LINDEX`）是 O(N)。位置查询请使用有序集合。
