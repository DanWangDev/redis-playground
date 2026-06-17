# 练习 05：集合

## 你将学到

- 使用 `SADD` 存储唯一成员
- 使用 `SISMEMBER` 测试成员资格
- 使用 `SREM` 删除成员
- 集合运算：`SINTER`（交集）、`SUNION`（并集）、`SDIFF`（差集）
- 使用 `SMEMBERS` 获取所有成员
- 使用 `SCARD` 计数，使用 `SRANDMEMBER` 随机获取成员

## 为什么重要

Redis 集合是唯一字符串的无序集合。它们支持标签系统、好友列表、独立访客追踪以及任何需要成员测试或集合运算的问题。`SINTER`（共同好友）、`SUNION`（所有兴趣）和 `SDIFF`（缺失标签）等操作是 O(N)，其中 N 是最小集合的大小，因此非常快。

## 核心概念

### 集合运算

```
SADD user:1:tags "redis" "python" "docker"
SADD user:2:tags "redis" "java" "docker"

SINTER user:1:tags user:2:tags  → {"redis", "docker"}  # 共同标签
SUNION user:1:tags user:2:tags  → {"redis", "python", "docker", "java"}  # 所有标签
SDIFF user:1:tags user:2:tags   → {"python"}  # user:1 有但 user:2 没有的标签
```

## 常见陷阱

- **SMEMBERS 是 O(N)**：对于有数百万成员的集合，会返回所有成员。使用 `SSCAN` 处理大型集合。
- **没有排序**：集合是无序的。需要排序？使用有序集合（练习 06）。
- **重复项被静默丢弃**：`SADD set "a" "a"` 只会添加一次 "a"。
- **与空集合求交**：与空集合的交集总是返回空。
