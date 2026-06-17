# Exercise 04: Lists

## What You'll Learn

- Build queues with `LPUSH` + `RPOP` (FIFO)
- Build stacks with `LPUSH` + `LPOP` (LIFO)
- Inspect ranges with `LRANGE`
- Cap collections with `LTRIM`
- Block on empty lists with `BLPOP` / `BRPOP`
- Get length with `LLEN`

## Why This Matters

Redis Lists are linked lists, not arrays. They are optimized for head/tail operations (O(1)) but slow for index-based access (O(N)). This makes them perfect for queues, stacks, activity feeds, and job systems. The blocking pop operations (`BLPOP`/`BRPOP`) enable worker pools without busy-wait polling.

## Core Concepts

### Queue vs Stack

```
# Queue (FIFO): LPUSH + RPOP
LPUSH queue "task1" "task2"      # tasks wait in order
RPOP queue                        # "task1" (first in, first out)

# Stack (LIFO): LPUSH + LPOP
LPUSH stack "page1" "page2"      # pages pushed
LPOP stack                        # "page2" (last in, first out)
```

### List Internals

Redis Lists are doubly-linked lists. Head/tail push and pop are O(1). Accessing by index (`LINDEX`) is O(N). This is the opposite of Python lists (arrays) where indexing is O(1) but head insert is O(N).

### Capped Collections

`LTRIM list 0 99` keeps only the first 100 elements. Combined with `LPUSH`, this creates a capped FIFO collection — perfect for activity feeds where you only need the most recent N items.

### Blocking Pops

`BLPOP queue 5` blocks for up to 5 seconds waiting for an item. Returns immediately if items exist. This enables efficient worker pools — no polling loop needed.

## What You'll Practice

1. Build a task queue with LPUSH + RPOP
2. Build a history stack with LPUSH + LPOP
3. Inspect elements with LRANGE (start to end, by index)
4. Cap a collection with LTRIM (keep last N)
5. Block on an empty queue with BLPOP (with timeout)
6. Check length with LLEN

## Key Gotchas

- **LRANGE is O(S+N)** where S is the start offset. `LRANGE list 0 -1` on a huge list is expensive.
- **LTRIM is O(N)** of removed elements. Trimming a million-element list to 10 is fast (only 10 kept).
- **BLPOP with timeout 0** blocks indefinitely — be careful in single-threaded code.
- **Lists are not arrays**: Random access (`LINDEX`) is O(N). Use Sorted Sets for positional queries.
