"""Exercise 24: RediSearch — full-text search and secondary indexing (Redis Stack)."""

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner


class Ex24RediSearch(ExerciseRunner):
    def __init__(self):
        super().__init__("24-redisearch", "RediSearch")

    def run(self, client: redis.Redis) -> dict:
        results = {}

        self.log.section("Step 1: FT.CREATE — Define a Search Index")
        self.log.concept(
            "RediSearch indexes hash keys matching a prefix pattern (e.g., product:*)."
        )
        self.log.concept("Requires Redis Stack — may not be available in plain Redis.")
        try:
            try:
                client.execute_command("FT.DROPINDEX", "idx:products", "DD")
            except redis.exceptions.ResponseError:
                pass
            client.execute_command(
                "FT.CREATE",
                "idx:products",
                "ON",
                "HASH",
                "PREFIX",
                "1",
                "product:",
                "SCHEMA",
                "title",
                "TEXT",
                "WEIGHT",
                "5.0",
                "description",
                "TEXT",
                "price",
                "NUMERIC",
                "SORTABLE",
                "category",
                "TAG",
            )
            self.log.command(
                "FT.CREATE idx:products ON HASH PREFIX 1 product: SCHEMA ..."
            )
            self.log.success("Index created")
        except redis.exceptions.ResponseError as e:
            self.log.warn(f"FT.CREATE not available: {e}")
            results["search_available"] = False
            self.log.separator()
            self.log.success(
                "RediSearch requires Redis Stack — exercise complete (conceptual)"
            )
            return results

        results["search_available"] = True

        self.log.section("Step 2: Index Products with HSET")
        products = [
            (
                "product:1",
                {
                    "title": "Redis T-Shirt",
                    "description": "Cool cotton shirt with redis logo",
                    "price": "25",
                    "category": "clothing",
                },
            ),
            (
                "product:2",
                {
                    "title": "Redis Hoodie",
                    "description": "Warm hooded sweatshirt for developers",
                    "price": "55",
                    "category": "clothing",
                },
            ),
            (
                "product:3",
                {
                    "title": "Redis Book",
                    "description": "Comprehensive guide to redis internals",
                    "price": "40",
                    "category": "books",
                },
            ),
        ]
        for key, fields in products:
            client.hset(key, mapping=fields)
        self.log.command("HSET product:1, product:2, product:3 (3 products)")
        results["indexed"] = 3

        def _count(r) -> int:
            """Extract hit count from FT.SEARCH response (handles RESP2 list and RESP3 dict)."""
            if isinstance(r, dict):
                return r.get("total_results", 0)
            return r[0]

        self.log.section("Step 3: FT.SEARCH — Full-Text Search")
        results_text = client.execute_command(
            "FT.SEARCH", "idx:products", "shirt | hoodie", "LIMIT", "0", "5"
        )
        self.log.command("FT.SEARCH idx:products 'shirt | hoodie'")
        self.log.output(f"Found {_count(results_text)} match(es)")
        results["text_search"] = _count(results_text)

        self.log.section("Step 4: Numeric Range Filter")
        results_price = client.execute_command(
            "FT.SEARCH", "idx:products", "@price:[0 50]", "LIMIT", "0", "5"
        )
        self.log.command("FT.SEARCH idx:products '@price:[0 50]'")
        self.log.output(f"Products under $50: {_count(results_price)}")
        results["price_filter"] = _count(results_price)

        self.log.section("Step 5: Tag Filter")
        results_tag = client.execute_command(
            "FT.SEARCH", "idx:products", "@category:{clothing}", "LIMIT", "0", "5"
        )
        self.log.command("FT.SEARCH idx:products '@category:{clothing}'")
        self.log.output(f"Clothing products: {_count(results_tag)}")
        results["tag_filter"] = _count(results_tag)

        client.execute_command("FT.DROPINDEX", "idx:products", "DD")

        self.log.separator()
        self.log.success(
            f"RediSearch: text={results['text_search']}, price={results['price_filter']}, tag={results['tag_filter']}"
        )
        return results
