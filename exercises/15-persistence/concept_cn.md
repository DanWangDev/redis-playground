# 练习 15：持久化

## 你将学到
- 使用 `CONFIG GET` 检查持久化配置
- 理解 RDB 快照和 AOF 日志
- 使用 `INFO persistence` 检查持久化状态

## 为什么重要
Redis 是内存数据库，但数据可以通过 RDB 快照和 AOF 日志在重启后存活。理解持久化权衡对生产环境至关重要。

## 常见陷阱
- RDB 快照使用 fork——子进程写入，父进程继续服务。保存期间内存翻倍。
- AOF 文件无限增长——使用 `BGREWRITEAOF` 进行压缩。
- `appendfsync always` 最安全但最慢。
