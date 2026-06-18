# 练习 23：RedisJSON

## 你将学到
- 使用 JSON.SET/JSON.GET 存储和检索 JSON 文档
- 使用 JSONPath 语法访问嵌套路径
- 原子地修改嵌套字段
- 使用 JSON.ARRAPPEND 修改数组

## 为什么重要
RedisJSON 是最流行的 Redis Stack 模块，提供原生 JSON 文档存储及嵌套路径的原子操作。

## 常见陷阱
- 需要 Redis Stack（普通 Redis OSS 不包含 JSON 模块）
- 根路径 `$` 是必需的
- JSONPath 功能强大但语法不同
