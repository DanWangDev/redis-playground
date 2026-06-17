# Exercise 12: Geospatial

## What You'll Learn
- Store coordinates with `GEOADD`
- Query by radius with `GEORADIUS` / `GEORADIUSBYMEMBER`
- Calculate distance with `GEODIST`
- Get coordinates with `GEOPOS`
- Get GeoHash with `GEOHASH`

## Why This Matters
Redis Geospatial indexes store lat/lon pairs and provide radius queries — find all restaurants within 5km, locate nearest drivers, calculate store-to-user distances. Built on Sorted Sets, geospatial operations are O(log N).

## Core Concepts
- **GEOADD** stores member coordinates (lon, lat, member)
- **GEORADIUS** finds members within a radius from a point
- **GEORADIUSBYMEMBER** finds members near another member
- **GEODIST** returns distance between two members in meters/km/mi/ft

## Key Gotchas
- Coordinates order is **longitude, latitude** (not lat, lon).
- Valid ranges: lon -180..180, lat -85..85 (near poles excluded).
- Internally, it's a Sorted Set — you can also use ZREM, ZCARD, etc.
