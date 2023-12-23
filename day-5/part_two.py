import os
from typing import NamedTuple
from pprint import pprint
import pytest


INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


class SeedRange(NamedTuple):
    start: int
    span: int


class ChunkLine(NamedTuple):
    destination: int
    source: int
    span: int


class SourceMap:
    source_lower: int
    source_upper: int
    dest_lower: int
    dest_upper: int

    def __init__(self, chunk_line: tuple[int, int, int]) -> None:
        self.source_lower = chunk_line[1]
        self.source_upper = chunk_line[1] + chunk_line[2] - 1
        self.dest_lower = chunk_line[0]
        self.dest_upper = chunk_line[0] + chunk_line[2] - 1

    def get_destination(self, value: int) -> None | int:
        if value < self.source_lower or value > self.source_upper:
            return None
        return self.dest_lower + (value - self.source_lower)

    def __str__(self) -> str:
        return f"[{self.source_lower}..{self.source_upper}] -> [{self.dest_lower}..{self.dest_upper}]"


class ObjectRange(NamedTuple):
    lower_bound: int
    upper_bound: int

    def __str__(self) -> str:
        return f"[{self.lower_bound}..{self.upper_bound}]"


def get_mappings_by_chunk(chunks: list[str]) -> list[list[SourceMap]]:
    source_maps = []
    for chunk in chunks:
        smaps_for_chunk = []
        lines = chunk.split("\n")
        for line in lines[1:]:
            if len(line) == 0:
                continue
            smaps_for_chunk.append(SourceMap(tuple(int(n) for n in line.split(" "))))
        source_maps.append(sorted(smaps_for_chunk, key=lambda r: r.source_lower))

    return source_maps


def compute_destinations(
    srange: ObjectRange, source_maps: set[SourceMap]
) -> list[ObjectRange]:
    destinations: list[ObjectRange] = []
    dest_lower = None
    dest_upper = None
    last_intersected_upper_bound = None
    for smap in source_maps:
        if smap.source_upper < srange.lower_bound:
            # .....SS.
            # .CCC....
            continue

        if smap.source_lower > srange.upper_bound:
            # .SSS....
            # .....CCC
            break

        if smap.source_lower < srange.lower_bound:
            # ..SSSSS.
            # CCCC....
            # or
            # ..SSSSS.
            # CCCCCCCC
            dest_lower = smap.get_destination(srange.lower_bound)
            # if the last intersected upper bound is higher thatn the range upper bound, the loop will be skipped anyway
            last_intersected_upper_bound = min(smap.source_upper, srange.upper_bound)
            dest_upper = smap.get_destination(
                min(smap.source_upper, srange.upper_bound)
            )

            destinations.append(ObjectRange(dest_lower, dest_upper))
            continue

        # ..SSSSS.
        # ..CCCC..
        # or
        # ..SSSSS.
        # .....CCCC

        # Add the uninterseced ranges to the destination
        if last_intersected_upper_bound is None:
            if srange.lower_bound < smap.source_lower:
                # if the interval is at least of 1 length
                destinations.append(
                    ObjectRange(srange.lower_bound, smap.source_lower - 1)
                )
        else:
            if last_intersected_upper_bound + 1 < smap.source_lower:
                # if the interval is at least of 1 length
                destinations.append(
                    ObjectRange(last_intersected_upper_bound + 1, smap.source_lower - 1)
                )

        dest_lower = smap.get_destination(smap.source_lower)
        last_intersected_upper_bound = min(smap.source_upper, srange.upper_bound)
        dest_upper = smap.get_destination(min(smap.source_upper, srange.upper_bound))

        destinations.append(ObjectRange(dest_lower, dest_upper))
    if len(destinations) == 0:
        destinations = [srange]
    return destinations


def compute(s: str):
    chunks = s.split("\n\n")
    split_seeds = chunks[0][7:].split(" ")
    parsed_seeds = [
        SeedRange(int(split_seeds[i]), int(split_seeds[i + 1]))
        for i in range(0, len(split_seeds), 2)
    ]
    seeds_range = [ObjectRange(sr.start, sr.start + sr.span - 1) for sr in parsed_seeds]
    sorted_mappings_by_chunk = get_mappings_by_chunk(chunks[1:])
    previous_destinations = seeds_range.copy()
    step = 1
    for sorted_mappings in sorted_mappings_by_chunk:
        print(f"COMPUTING STEP {step}/{len(sorted_mappings_by_chunk)}")
        chunk_destinations = []
        for destination_range in previous_destinations:
            chunk_destinations += compute_destinations(
                destination_range, sorted_mappings
            )
        previous_destinations = chunk_destinations.copy()
        step += 1

    return min([destination.lower_bound for destination in previous_destinations])


INPUT_S = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
EXPECTED = 46


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


# def test2() -> None:
#     seeds = set([ObjectRange(79, 92), ObjectRange(55, 67)])
#     smaps = [
#         SourceMap((52, 50, 48)),
#         SourceMap((50, 98, 2)),
#     ]
#     destinations = []
#     for seed in seeds:
#         destinations += compute_destinations(seed, smaps)
#     assert destinations == [ObjectRange(81, 94), ObjectRange(57, 69)]


def main():
    with open(INPUT_TXT) as f:
        pprint(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
