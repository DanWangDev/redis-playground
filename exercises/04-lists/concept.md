# Exercise 04: Lists

## What You'll Learn

- Build queues with `LPUSH` + `RPOP` (FIFO)
- Build stacks with `LPUSH` + `LPOP` (LIFO)
- Inspect ranges with `LRANGE`
- Cap collections with `LTRIM`
- Block on empty lists with `BLPOP` / `BRPOP`
- Get length with `LLEN`

## Why This Matters

Redis Lists are linked lists optimized for head/tail operations (O(1)). They're perfect for queues, stacks, activity feeds, and job systems. The blocking pop operations enable worker pools without busy-wait polling.

## Core Concepts

### Queue vs Stack

```
# Queue (FIFO): RPUSH + LPOP
RPUSH queue "task1" "task2"    # add to tail
LPOP queue                      # "task1" (first in, first out)

# Stack (LIFO): LPUSH + LPOP
LPUSH stack "page1" "page2"    # push onto head
LPOP stack                      # "page2" (last in, first out)
```

### Capped Collections

`LTRIM list 0 99` keeps only the first 100 elements — perfect for activity feeds where you only need recent items.

## What You'll Practice

1. Build a task queue with RPUSH + LPOP
2. Build a history stack with LPUSH + LPOP
3. Inspect elements with LRANGE (including negative indices)
4. Cap a collection with LTRIM (keep last N)
5. Check length with LLEN

## Key Gotchas

- **LRANGE is O(S+N)**: Start offset cost matters. `LRANGE list 0 -1` on a huge list is expensive.
- **Lists are not arrays**: Random access (`LINDEX`) is O(N). Use Sorted Sets for positional queries.
- **LTRIM is O(N)** of removed elements: Trimming a million-element list to 10 is fast.
