import os
from pprint import pprint
import pytest


INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def get_sorted_chunks(chunks: list[str]):
    sorted_chunks = []
    for chunk in chunks:
        ranges = []
        lines = chunk.split("\n")
        for line in lines[1:]:
            if len(line) == 0:
                continue
            ranges.append(tuple([int(n) for n in line.split(" ")]))
        sorted_chunks.append(sorted(ranges, key=lambda r: r[1]))

    return sorted_chunks


def get_destination_for_chunk(seed: int, sorted_chunk: list[tuple[int]]):
    for i in range(len(sorted_chunk)):
        m = sorted_chunk[i]
        if seed < m[1] and i == 0:
            return seed
        if seed >= m[1] and seed < m[1] + m[2]:
            return m[0] + seed - m[1]
    return seed


def compute(s: str):
    chunks = s.split("\n\n")
    seeds = [int(seed) for seed in chunks[0][7:].split(" ")]
    sorted_chunks = get_sorted_chunks(chunks[1:])
    results = []
    for seed in seeds:
        result = seed
        for chunk in sorted_chunks:
            pprint(chunk)
            result = get_destination_for_chunk(result, chunk)
        results.append(result)
    return min(results)


INPUT_S = """\
seeds: 79 14 55

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
EXPECTED = 43


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main():
    with open(INPUT_TXT) as f:
        pprint(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
