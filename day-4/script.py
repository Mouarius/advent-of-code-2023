from collections import defaultdict
from pprint import pprint
import numpy as np
import math

with open("./input.txt") as f:
    f_lines = f.readlines()


def get_winning_played_numbers(line: str):
    numbers_str = line.split(":")[1]
    winning_str, played_str = numbers_str.split("|")
    winning = []
    played = []
    for w_digits in winning_str.strip().split(" "):
        try:
            winning.append(int(w_digits.strip()))
        except Exception:
            continue

    for p_digits in played_str.strip().split(" "):
        try:
            played.append(int(p_digits.strip()))
        except Exception:
            continue

    return winning, played


def get_won_numbers(line: str):
    winning, played = get_winning_played_numbers(line)
    intersection = np.intersect1d(winning, played)
    return intersection


def get_line_points(line: str):
    won_numbers = get_won_numbers(line)
    return int(math.pow(2, len(won_numbers) - 1) if len(won_numbers) > 0 else 0)


def get_part_one_result(lines: list[str]):
    total = 0
    for line in lines:
        total += get_line_points(line)
    return total


class Card:
    index: int
    cards_to_win: list[int]
    times_to_count: int

    def __init__(self, index) -> None:
        self.index = index


def solve_cards(lines: list[str]) -> dict[int, list[int]]:
    solved_cards = defaultdict(list)
    max_index = len(lines)
    for index, line in enumerate(lines, start=1):
        count = len(get_won_numbers(line))
        solved_cards[index] = [
            [n for n in range(index + 1, min(index + count + 1, max_index + 1))],
            1,
        ]
    return solved_cards


def annotate_cards_count(lines):
    solved_cards = solve_cards(f_lines)
    for i, values in solved_cards.items():
        for key in values[0]:
            solved_cards[key][1] += solved_cards[i][1]
    return solved_cards


def get_part_two_result(lines):
    solved_cards = solve_cards(lines)
    return sum([v[1] for v in solved_cards.values()])

