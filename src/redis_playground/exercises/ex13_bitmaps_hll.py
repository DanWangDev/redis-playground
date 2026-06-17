"""Exercise 13: Bitmaps & HyperLogLog — compact analytics structures."""

import redis

from redis_playground.shared.exercise_runner import ExerciseRunner


class Ex13BitmapsHLL(ExerciseRunner):
    def __init__(self):
        super().__init__("13-bitmaps-hyperloglog", "Bitmaps & HyperLogLog")

    def run(self, client: redis.Redis) -> dict:
        results = {}

        self.log.section("Step 1: SETBIT — Track Daily Logins")
        self.log.concept("Each bit represents a user. '1' = logged in on day N.")
        # User 7 logged in on day 0, user 42 on day 0, user 7 on day 1
        client.setbit("logins:day-0", 7, 1)
        client.setbit("logins:day-0", 42, 1)
        client.setbit("logins:day-1", 7, 1)
        client.setbit("logins:day-1", 99, 1)
        self.log.command(
            "SETBIT logins:day-0 7 1 → 42 1, SETBIT logins:day-1 7 1 → 99 1"
        )
        results["day0_bitcount"] = client.bitcount("logins:day-0")
        results["day1_bitcount"] = client.bitcount("logins:day-1")
        self.log.output(
            f"Day 0 logins: {results['day0_bitcount']}, Day 1: {results['day1_bitcount']}"
        )

        self.log.section("Step 2: GETBIT — Check Specific User")
        user7_day0 = client.getbit("logins:day-0", 7)
        user7_day1 = client.getbit("logins:day-1", 7)
        self.log.command("GETBIT logins:day-0 7 → GETBIT logins:day-1 7")
        self.log.output(
            f"User 7: day0={user7_day0}, day1={user7_day1} (logged in both days)"
        )
        results["user7_both_days"] = user7_day0 and user7_day1

        self.log.section("Step 3: BITOP — Both Days Active")
        client.bitop("AND", "logins:both-days", "logins:day-0", "logins:day-1")
        both_count = client.bitcount("logins:both-days")
        self.log.command("BITOP AND logins:both-days logins:day-0 logins:day-1")
        self.log.output(f"Users active both days: {both_count} (only user 7)")
        results["both_days"] = both_count

        self.log.section("Step 4: PFADD — Unique Visitors (HLL)")
        self.log.concept(
            "HyperLogLog estimates unique elements with ~0.81% error in 12KB."
        )
        client.pfadd("visitors:page-a", "user:1", "user:2", "user:3", "user:1")
        client.pfadd("visitors:page-b", "user:2", "user:3", "user:4")
        self.log.command(
            "PFADD visitors:page-a user:1-3, PFADD visitors:page-b user:2-4"
        )
        results["page_a"] = client.pfcount("visitors:page-a")
        results["page_b"] = client.pfcount("visitors:page-b")
        self.log.output(f"Page A: ~{results['page_a']}, Page B: ~{results['page_b']}")

        self.log.section("Step 5: PFMERGE — Total Unique Visitors")
        client.pfmerge("visitors:total", "visitors:page-a", "visitors:page-b")
        total = client.pfcount("visitors:total")
        self.log.command("PFMERGE visitors:total visitors:page-a visitors:page-b")
        self.log.output(f"Total unique: ~{total} (users 1-4)")
        results["total_unique"] = total

        self.log.separator()
        self.log.success(
            f"Analytics: day0={results['day0_bitcount']}, both days={both_count}, unique~{total}"
        )
        return results
