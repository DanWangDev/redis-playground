# Exercise 23: RedisJSON

## What You'll Learn
- Store and retrieve JSON documents with `JSON.SET` / `JSON.GET`
- Access nested paths with JSONPath syntax
- Modify arrays with `JSON.ARRAPPEND`, `JSON.ARRINSERT`
- Query object keys with `JSON.OBJKEYS`
- Delete values with `JSON.DEL`

## Why This Matters

RedisJSON is the most popular Redis Stack module. It provides native JSON document storage with atomic operations on nested paths. Unlike storing JSON as a string (which requires full document read-modify-write), RedisJSON lets you update a single field deep inside a document atomically. This is the foundation for document-oriented use cases in Redis.

## Core Concepts

### JSONPath Access

```
JSON.SET user:1 $ '{"name":"Alice","address":{"city":"SF","zip":"94107"}}'
JSON.GET user:1 $.address.city  → ["SF"]
JSON.GET user:1 $.address       → [{"city":"SF","zip":"94107"}]
```

The `$` is the root path. `$.address.city` is a JSONPath expression.

### Atomic Nested Operations

```
JSON.SET user:1 $.login_count 0
JSON.NUMINCRBY user:1 $.login_count 1  → 1 (atomic increment!)
JSON.ARRAPPEND user:1 $.tags '"redis"' '"json"'  → 2 (array length)
```

## What You'll Practice

1. Store a JSON document with JSON.SET
2. Read full document and nested paths with JSON.GET
3. Increment a numeric field with JSON.NUMINCRBY
4. Append to an array with JSON.ARRAPPEND
5. Query object keys with JSON.OBJKEYS
6. Delete a path with JSON.DEL

## Key Gotchas

- **Requires Redis Stack**: Plain Redis OSS doesn't include the JSON module.
- **JSONPath is powerful but different**: Not all JSONPath features are supported.
- **Root path `$` is required**: Most commands need an explicit path.
- **JSON values are typed**: `JSON.GET` returns properly typed values, not strings.
