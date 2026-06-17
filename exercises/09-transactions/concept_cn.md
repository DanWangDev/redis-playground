# 练习 09：事务

## 你将学到

- 使用 `MULTI` / `EXEC` 原子性地批量执行命令
- 使用 `DISCARD` 放弃事务
- 使用 `WATCH` / `UNWATCH` 实现乐观锁
- 理解其局限性：错误时不会回滚

## 为什么重要

Redis 事务保证一批命令原子执行——没有其他客户端的命令会插入其中。这对于在账户间转账等操作至关重要，你需要作为一个原子单元从一个账户扣款并记入另一个账户。`WATCH` 命令实现了乐观并发控制——在执行事务前检查键是否被更改。

## 核心概念

### MULTI/EXEC 原子性

```
MULTI
SET account:a 50
SET account:b 150
EXEC
```

MULTI 和 EXEC 之间的所有命令会被排队，然后作为一个原子批次执行。没有其他客户端可以看到中间状态。

### 使用 WATCH 进行乐观锁

```
WATCH account:a
val = GET account:a
MULTI
SET account:a (val - 10)
EXEC
```

如果 `account:a` 在 `WATCH` 和 `EXEC` 之间被其他客户端修改，事务会中止，`EXEC` 返回 `None`。

### 事务中的错误

- **EXEC 前的语法错误**：Redis 拒绝整个事务。
- **EXEC 期间的运行时错误**：Redis 仍会执行事务，但失败的命令会报错。其他命令会成功。**没有回滚。**

## 常见陷阱

- **没有回滚**：如果事务中的某条命令失败，其他命令仍会执行。
- **WATCH 是连接作用域**：WATCH 绑定到连接而非事务。`EXEC`、`DISCARD` 或连接关闭会清除监视。
- **EXEC 在事务中止时返回 None**：不是异常——当被 WATCH 的键被修改时，`EXEC` 返回 `None`。
- **MULTI 内的读取是延迟的**：MULTI 中的 `GET` 不会立即返回值——它只是排队命令。值会在 `EXEC` 的结果数组中返回。
