"""Exercise 12: Geospatial — location storage, radius queries, distance."""

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner


class Ex12Geospatial(ExerciseRunner):
    def __init__(self):
        super().__init__("12-geospatial", "Geospatial")

    def run(self, client: redis.Redis) -> dict:
        results = {}

        self.log.section("Step 1: GEOADD — Add Locations")
        self.log.concept("GEOADD stores longitude, latitude coordinates for members.")
        client.geoadd("stores", (-122.4194, 37.7749, "downtown"))
        client.geoadd("stores", (-122.4184, 37.7599, "mission"))
        client.geoadd("stores", (-122.3982, 37.7810, "soma"))
        self.log.command("GEOADD stores (downtown, mission, soma)")
        count = client.zcard("stores")  # internals: sorted set
        self.log.output(f"Stored {count} locations")
        results["count"] = count

        self.log.section("Step 2: GEOPOS — Get Coordinates")
        coords = client.geopos("stores", "downtown")
        self.log.command("GEOPOS stores downtown")
        self.log.output(f"→ {coords}")
        results["downtown_coords"] = coords

        self.log.section("Step 3: GEODIST — Distance Between Members")
        dist_m = client.geodist("stores", "downtown", "mission", unit="m")
        dist_km = client.geodist("stores", "downtown", "mission", unit="km")
        self.log.command("GEODIST stores downtown mission m → km")
        self.log.output(f"{dist_m:.0f}m = {dist_km:.2f}km")
        results["dist_m"] = dist_m
        results["dist_km"] = dist_km

        self.log.section("Step 4: GEORADIUS — Find Nearby")
        nearby = client.georadius(
            "stores", -122.4194, 37.7749, 3, unit="km", withdist=True
        )
        self.log.command("GEORADIUS stores -122.42 37.77 3 km WITHDIST")
        for name, dist in nearby:
            self.log.output(f"  {name}: {dist:.2f}km")
        results["nearby_3km"] = len(nearby)

        self.log.section("Step 5: GEORADIUSBYMEMBER")
        near_mission = client.georadiusbymember("stores", "mission", 2, unit="km")
        self.log.command("GEORADIUSBYMEMBER stores mission 2 km")
        self.log.output(f"Near mission: {near_mission}")
        results["near_mission"] = near_mission

        self.log.separator()
        self.log.success(
            f"Geo: {count} stores, downtown-mission={dist_km:.2f}km, nearby={len(nearby)}"
        )
        return results
