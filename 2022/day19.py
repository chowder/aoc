import functools
import itertools
import re
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from functools import cache

Robots = Resources = Cost = tuple[int, int, int, int]
Costs = tuple[Cost, Cost, Cost, Cost]


@dataclass
class Blueprint:
    blueprint_id: int
    costs: tuple[Cost, Cost, Cost, Cost]

    @staticmethod
    def from_line(line):
        matches = re.findall(r"(\d+)", line)

        costs = (
            (int(matches[1]), 0, 0, 0),
            (int(matches[2]), 0, 0, 0),
            (int(matches[3]), int(matches[4]), 0, 0),
            (int(matches[5]), 0, int(matches[6]), 0)
        )

        return Blueprint(blueprint_id=int(matches[0]), costs=costs)


def can_afford(resources: Resources, cost: Cost):
    return all(have >= need for have, need in zip(resources, cost))


@cache
def required_robots(costs: Costs):
    return functools.reduce(lambda acc, n: tuple(max(l, r) for l, r in zip(acc, n)), costs, (0, 0, 0, 1000))


@cache
def farm_geodes(resources: Resources, robots: Robots, costs: Costs, minutes_left: int) -> int:
    if minutes_left == 0:
        return resources[-1]

    decisions = []
    could_not_afford_something = False

    # Explore the option of creating a robot, if we are able to
    for i, cost in reversed(list(enumerate(costs))):
        if not can_afford(resources, cost):
            could_not_afford_something = True
            continue
        if robots[i] >= required_robots(costs)[i]:
            continue
        # Pay the cost of the robot
        new_resources = tuple((have - need) for have, need in zip(resources, cost))
        # Run a production step
        new_resources = tuple((res + rob) for res, rob in zip(new_resources, robots))
        # Create a new robot
        new_robots = robots[:i] + (robots[i] + 1,) + robots[i+1:]

        # Just build the geode bot...
        if i == 3:
            return farm_geodes(new_resources, new_robots, costs, minutes_left - 1)

        decisions.append(farm_geodes(new_resources, new_robots, costs, minutes_left - 1))

    # Or we can just not build any robots (if we couldn't afford something, or we didn't build any other robots)
    if could_not_afford_something or not decisions:
        new_resources = tuple((res + rob) for res, rob in zip(resources, robots))
        decisions.append(farm_geodes(new_resources, robots, costs, minutes_left - 1))

    return max(decisions)


def main():
    with open("inputs/day19.txt") as f:
        blueprints = [Blueprint.from_line(l) for l in f.read().splitlines()]

    # quality = 0
    # for i, blueprint in enumerate(blueprints):
    #     print(f"{i + 1}/{len(blueprints)}")
    #     geodes = farm_geodes((0, 0, 0, 0), (1, 0, 0, 0), blueprint.costs, 24)
    #     quality += blueprint.blueprint_id * geodes
    #     print("Blueprint ID:", blueprint.blueprint_id, "\tGeodes:", geodes)
    #     farm_geodes.cache_clear()
    #
    # print(quality)

    total = 1
    for i, blueprint in enumerate(blueprints[:3]):
        print(f"{i + 1}/3")
        geodes =
        total *= geodes
        print("Blueprint ID:", blueprint.blueprint_id, "\tGeodes:", geodes)
        farm_geodes.cache_clear()


if __name__ == "__main__":
    main()
