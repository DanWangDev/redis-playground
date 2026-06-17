# 练习 19：Redis 哨兵

## 你将学到
- 理解哨兵架构：监控、故障转移、发现
- 使用 `SENTINEL get-master-addr-by-name` 查询主节点地址
- 使用 `SENTINEL replicas` 发现副本
- 配置支持哨兵的 Redis 客户端

## 为什么重要
Redis Sentinel 提供无分片的高可用性。多个 Sentinel 进程监控 Redis 实例，通过法定人数就故障达成一致，并自动将副本提升为主节点。

## 常见陷阱
- Sentinel 提供 HA 但不提供分片。水平扩展请使用 Redis 集群（Ex20）。
- 客户端必须支持 Sentinel 以跟随故障转移。
- 至少需要 3 个 Sentinel 实例才能可靠部署。
