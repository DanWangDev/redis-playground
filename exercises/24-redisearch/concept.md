# Exercise 24: RediSearch

## What You'll Learn
- Create a search index with `FT.CREATE`
- Index documents with `HSET` (auto-indexed)
- Search with `FT.SEARCH` — full-text, numeric, tag filters
- Aggregate with `FT.AGGREGATE`

## Why This Matters
RediSearch adds full-text search and secondary indexing to Redis. Unlike querying by key, RediSearch lets you find documents by content, filter by numeric ranges, and facet by tags — all at Redis speed. It's used for product catalogs, user search, and real-time analytics dashboards.

## Core Concepts
- **FT.CREATE**: Defines a search index over hash keys matching a prefix pattern
- **TEXT fields**: Full-text searchable
- **NUMERIC fields**: Range-filterable
- **TAG fields**: Exact-match / faceting
- **FT.SEARCH**: Query with `@field:value` syntax, returns matching documents

## What You'll Practice
1. Create a search index on `product:*` hash keys
2. Index products with HSET
3. Full-text search with FT.SEARCH
4. Numeric range filter
5. Tag filter

## Key Gotchas
- Indexes only apply to keys matching the prefix pattern (e.g., `product:*`)
- New keys matching the pattern are auto-indexed
- Requires Redis Stack (not plain Redis OSS)
