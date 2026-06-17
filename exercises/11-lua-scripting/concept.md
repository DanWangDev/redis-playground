# Exercise 11: Lua Scripting

## What You'll Learn
- Execute Lua scripts with `EVAL` and `EVALSHA`
- Load scripts for cached execution with `SCRIPT LOAD`
- Implement atomic check-and-set patterns
- Understand why Lua is atomic: scripts block the server

## Why This Matters
Lua scripting is Redis's most powerful atomicity primitive. Unlike MULTI/EXEC (no intermediate reads), Lua scripts can read, compute, and write atomically — ideal for rate limiters, inventory deduction, and distributed locks. Scripts run server-side with zero network round-trips.

## Core Concepts
- **EVAL**: Sends script + keys + args; executes atomically
- **EVALSHA**: Executes a previously cached script by SHA hash (saves bandwidth)
- **SCRIPT LOAD**: Caches a script, returns its SHA
- **Keys vs ARGV**: Lua receives `KEYS[1]..KEYS[N]` and `ARGV[1]..ARGV[N]` — keys enable cluster routing

## What You'll Practice
1. Run a simple Lua script with EVAL
2. Load a script with SCRIPT LOAD, then execute with EVALSHA
3. Implement atomic inventory deduction (check quantity, decrement if sufficient)
4. Handle EVALSHA fallback when script isn't cached

## Key Gotchas
- **Scripts block the server**: Long-running Lua scripts block all other clients. Keep scripts short.
- **EVALSHA needs fallback**: If the script isn't cached (e.g., after server restart), EVALSHA returns NOSCRIPT. Always fall back to EVAL.
- **No external I/O**: Lua sandbox has no network, filesystem, or time access.
- **Keys must be explicit**: For Redis Cluster compatibility, all accessed keys must be passed in KEYS array.
