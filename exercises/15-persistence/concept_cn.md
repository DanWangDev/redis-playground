# 练习 15：持久化

## 你将学到
- 使用 CONFIG GET 检查持久化配置
- 理解 RDB 快照和 AOF 日志
- 使用 INFO persistence 检查状态

## 常见陷阱
- RDB 快照使用 fork——保存期间内存翻倍。
- AOF 文件无限增长——使用 BGREWRITEAOF。
- CONFIG 命令需要真实 Redis（fakereds 不支持）。
