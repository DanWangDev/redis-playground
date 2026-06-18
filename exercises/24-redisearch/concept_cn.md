# 练习 24：RediSearch

## 你将学到
- 使用 FT.CREATE 创建搜索索引
- 使用 FT.SEARCH 进行全文搜索
- 使用数值和标签过滤器

## 为什么重要
RediSearch 为 Redis 添加全文搜索和二级索引，让你以 Redis 的速度查找内容。

## 常见陷阱
- 索引仅适用于匹配前缀模式的键
- 需要 Redis Stack
