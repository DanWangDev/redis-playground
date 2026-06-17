"""Tests for Exercise 12: Geospatial."""

from redis_playground.exercises.ex12_geospatial import Ex12Geospatial


class TestEx12Geospatial:
    def test_geoadd_count(self, fake_redis):
        results = Ex12Geospatial().execute(fake_redis)
        assert results["count"] == 3

    def test_geopos(self, fake_redis):
        results = Ex12Geospatial().execute(fake_redis)
        lon, lat = results["downtown_coords"][0]
        assert abs(lon - (-122.4194)) < 0.001
        assert abs(lat - 37.7749) < 0.001

    def test_geodist(self, fake_redis):
        results = Ex12Geospatial().execute(fake_redis)
        assert results["dist_m"] > 0
        assert 1 < results["dist_km"] < 3

    def test_georadius(self, fake_redis):
        results = Ex12Geospatial().execute(fake_redis)
        assert results["nearby_3km"] >= 1
