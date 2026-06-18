# 练习 26：FUNCTION — Redis 7 服务器端函数

## 你将学到
- 使用 FUNCTION LOAD 加载函数库
- 使用 FCALL 调用函数
- 理解为什么 FUNCTION 取代了 EVAL

## 为什么重要
Redis 7 引入了 FUNCTION API — Lua 脚本的后继者。函数是持久的，在重启后仍然存在。

## 常见陷阱
- 需要 Redis 7.0+
- 使用与 EVAL 相同的 Lua 5.1 解释器
