# Redis 练习场

[English](README.md) | [中文版本](README.zh-CN.md)

26 个渐进式 Redis 学习练习。每个练习包含可运行的 Python 类、单元测试和双语概念文档（英文 + 中文）。

## 快速开始

```bash
pip install -e ".[dev]"
python -m redis_playground.main --exercise 01 --local --step
```

在浏览器中打开 RedisInsight：http://localhost:8001 可视化探索数据。

## 技术栈

![Python](https://img.shields.io/badge/Python_3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![Redis](https://img.shields.io/badge/Redis_Stack-FF4438?style=flat-square&logo=redis&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![Ruff](https://img.shields.io/badge/Ruff-FCC21B?style=flat-square&logo=ruff&logoColor=black)

双模式运行：[fakeredis](https://github.com/cunla/fakeredis-py)（内存模式，无需 Docker）或真实 Redis Stack。终端界面使用 [Rich](https://github.com/Textualize/rich)。中英双语概念文档。26 个练习均配有单元测试与集成测试。

## 练习列表

| # | 主题 | 学习内容 |
|---|------|---------|
| 01 | 基础命令 | PING, SET, GET, DEL, EXISTS, EXPIRE, TTL, KEYS, TYPE |
| 02 | 字符串 | INCR/DECR, MSET/MGET, GETRANGE/SETRANGE, SETNX, APPEND |
| 03 | 哈希 | HSET/HGET/HGETALL, HINCRBY, HDEL, HEXISTS, HKEYS/HVALS |
| 04 | 列表 | RPUSH/LPOP（队列）, LPUSH/LPOP（栈）, LRANGE, LTRIM |
| 05 | 集合 | SADD, SINTER/SUNION/SDIFF, SISMEMBER, SCARD |
| 06 | 有序集合 | ZADD, ZRANGE/ZREVRANGE, ZRANK, ZSCORE, ZINCRBY |
| 07 | 发布/订阅 | PUBLISH, SUBSCRIBE, PSUBSCRIBE, 即发即忘语义 |
| 08 | 流 | XADD, XREAD, XGROUP, XREADGROUP, XACK, XPENDING |
| 09 | 事务 | MULTI/EXEC, DISCARD, WATCH（乐观锁） |
| 10 | 管道 | pipeline(), 降低网络往返, 非原子交错 |
| 11 | Lua 脚本 | EVAL, EVALSHA, SCRIPT LOAD, 原子服务器端脚本 |
| 12 | 地理位置 | GEOADD, GEORADIUS, GEODIST, 基于位置的查询 |
| 13 | 位图与 HLL | SETBIT, BITCOUNT, PFADD, 概率计数 |
| 14 | 键空间通知 | notify-keyspace-events, PSUBSCRIBE `__keyspace@*` |
| 15 | 持久化 | RDB 快照, AOF, BGSAVE, 持久性权衡 |
| 16 | 客户端缓存 | CLIENT TRACKING, RESP3 推送, 缓存失效 |
| 17 | 限流 | 令牌桶, 滑动窗口, 固定窗口算法 |
| 18 | 分布式锁 | SET NX PX, Redlock 算法, 栅栏令牌 |
| 19 | 哨兵 | 哨兵监控, 自动故障转移, 主节点选举 |
| 20 | 集群 | 哈希槽, MOVED/ASK 重定向, 重新分片 |
| 21 | 分片发布/订阅 | SSUBSCRIBE, SPUBLISH, 分片频道分布 |
| 22 | SCAN | SCAN, HSCAN, SSCAN, ZSCAN — 基于游标的迭代 |
| 23 | RedisJSON | JSON.SET, JSON.GET, JSON.NUMINCRBY, JSON.ARRAPPEND |
| 24 | RediSearch | FT.CREATE, FT.SEARCH — 全文搜索与过滤 |
| 25 | RedisTimeSeries | TS.CREATE, TS.ADD, TS.RANGE 与聚合 |
| 26 | FUNCTION | FUNCTION LOAD, FCALL — Redis 7 持久化服务端函数 |

## CLI 参考

| 参数 | 说明 |
|------|------|
| `--exercise NN` | 练习编号（01–20） |
| `--local` | 使用 fakeredis（内存中，无需 Docker） |
| `--step` | 交互式逐步模式 |
| `--no-step` | 无暂停运行（CI/自动化） |

## 开发

```bash
make install-dev    # 安装开发依赖
make test           # 运行单元测试（fakeredis）
make lint           # Ruff 检查
make fmt            # Ruff 格式化
```

## 常见陷阱总结

- **KEYS 是 O(N)**：同步全键空间扫描——生产环境禁用，请用 `SCAN`。
- **TTL 返回 -1 与 -2**：`-1` 表示持久化（未设置过期）。`-2` 表示键不存在。
- **Pub/Sub 即发即忘**：订阅前发布的消息会丢失。需要持久化请用 Streams。
- **MULTI/EXEC 无回滚**：事务中某条命令失败，其他命令仍会执行。
- **管道非原子**：其他客户端的命令可能交错执行。
