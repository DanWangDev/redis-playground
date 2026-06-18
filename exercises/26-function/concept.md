# Exercise 26: FUNCTION — Redis 7 Server-Side Functions

## What You'll Learn
- Load functions with `FUNCTION LOAD`
- Call functions with `FCALL`
- List functions with `FUNCTION LIST`
- Understand why FUNCTION replaces EVAL/EVALSHA

## Why This Matters

Redis 7.0 introduced the FUNCTION API — the successor to Lua scripting (Ex11). Unlike EVAL scripts which are ephemeral (lost on restart), functions are durable: they survive restarts, can be replicated to replicas, and have proper library management. This is the production way to run server-side logic in Redis.

## Core Concepts

### FUNCTION vs EVAL

| Feature | EVAL/EVALSHA | FUNCTION |
|---------|-------------|----------|
| Persistence | Ephemeral (lost on restart) | Durable (survives restarts) |
| Replication | Script content replicated | Function replicated once |
| Library management | None | Named libraries |
| Call syntax | `EVALSHA sha` | `FCALL name keys args` |

## What You'll Practice
1. Load a function library with FUNCTION LOAD
2. Call a function with FCALL
3. List loaded functions with FUNCTION LIST
4. Delete with FUNCTION DELETE

## Key Gotchas
- **Requires Redis 7.0+**: FUNCTION commands don't exist in Redis 6.
- **Lua 5.1**: Functions use the same Lua 5.1 interpreter as EVAL.
- **Library name**: Must be unique — loading a library with the same name REPLACEs it.
