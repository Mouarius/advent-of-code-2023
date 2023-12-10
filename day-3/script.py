import re
import numpy as np
from pprint import pprint

with open("./input.txt") as file:
    file_lines = file.readlines()


def get_symbol_positions_in_line(line: str, line_index: int, symbols_regex: str):
    positions = set()
    matches = re.finditer(symbols_regex, line, re.MULTILINE)
    for match in matches:
        positions.add((match.start(), line_index))
    return positions


def get_symbol_positions(lines: list[str], symbols_regex: str):
    index = 0
    symbol_positions = set()
    for line in lines:
        symbol_positions = symbol_positions.union(
            get_symbol_positions_in_line(line, index, symbols_regex)
        )
        index += 1
    return symbol_positions


test_lines = (
    "....45....\n",
    "*...?.....\n",
    "100..2....\n",
    "..%.....4.\n",
)


def build_adjacent_matrix(lines, symbols_regex: str):
    """
    Returns a matrix with ones on positions adjacent to a symbol and zeros everywhere else
    """
    width = len(lines[0].rstrip("\n"))
    height = len(lines)
    adj_matrix = np.zeros((height, width), dtype=int)
    symbol_positions = get_symbol_positions(lines, symbols_regex)
    for x, y in symbol_positions:
        # center line
        adj_matrix[y][x] = 1
        if x >= 1:
            adj_matrix[y][x - 1] = 1
        if x < width - 1:
            adj_matrix[y][x + 1] = 1

        # top line
        if y >= 1:
            adj_matrix[y - 1][x] = 1
            if x >= 1:
                adj_matrix[y - 1][x - 1] = 1
            if x < width - 1:
                adj_matrix[y - 1][x + 1] = 1

        # bottom line
        if y < height - 1:
            adj_matrix[y + 1][x] = 1
            if x >= 1:
                adj_matrix[y + 1][x - 1] = 1
            if x < width - 1:
                adj_matrix[y + 1][x + 1] = 1

    return adj_matrix


def build_numbers_matrix(lines):
    """
    Returns a matrix where every position of a digit is replaced by the number the digit was a part of

    Example :
    "12..2."    [ [12, 12, 0, 0, 2, 0],
    "..123." ->   [0, 0 123, 123, 123, 0]]
    """
    width = len(lines[0].rstrip("\n"))
    height = len(lines)
    num_matrix = np.zeros((height, width), dtype=int)
    i = 0
    for line in lines:
        regex = r"(?!\.\d)(\d+)"
        matches = re.finditer(regex, line, re.MULTILINE)
        for match in matches:
            for j in range(match.start(), match.end()):
                num_matrix[i][j] = int(match.group())
        i += 1
    return num_matrix


def get_part_numbers(lines):
    """
    Returns a list of part numbers identified in the given lines
    It uses the matrix of adjacent positions as a mask for the matrix of the numbers by multiplying each number with its corresponding adjacent position index
    """
    symbols_regex = r"(?!\.\d)([^\.\d\n])"
    adj = build_adjacent_matrix(lines, symbols_regex)
    num = build_numbers_matrix(lines)
    res = [[val * index for val, index in zip(num[i], adj[i])] for i in range(len(adj))]
    w = len(adj[0])
    h = len(adj)
    numbers = []
    for i in range(h):
        prev = 0
        for j in range(w):
            if res[i][j] != prev and res[i][j] != 0:
                numbers.append(res[i][j])
            prev = res[i][j]
    return numbers


def get_part_one_result(lines):
    return sum(get_part_numbers(lines))


def get_unique_adjacent_numbers(symbol_position: tuple[int], numbers_matrix: np.array):
    x, y = symbol_position
    numbers = []
    height = len(numbers_matrix)
    width = len(numbers_matrix[0])
    # center line
    if x >= 1:
        l_number = numbers_matrix[y][x - 1]
        if l_number != 0:
            numbers.append(l_number)
    if x < width - 1:
        r_number = numbers_matrix[y][x + 1]
        if r_number != 0:
            numbers.append(r_number)

    # top line
    if y >= 1:
        tl_number = 0
        tm_number = numbers_matrix[y - 1][x]
        tr_number = 0

        if x >= 1:
            tl_number = numbers_matrix[y - 1][x - 1]
        if x < width - 1:
            tr_number = numbers_matrix[y - 1][x + 1]

        if tl_number != 0:
            numbers.append(tl_number)
        if tm_number != 0 and tm_number != tl_number:
            numbers.append(tm_number)
        if tr_number != 0 and tr_number != tm_number:
            numbers.append(tr_number)

    # bottom line
    if y < height - 1:
        bl_number = 0
        bm_number = numbers_matrix[y + 1][x]
        br_number = 0

        if x >= 1:
            bl_number = numbers_matrix[y + 1][x - 1]
        if x < width - 1:
            br_number = numbers_matrix[y + 1][x + 1]

        if bl_number != 0:
            numbers.append(bl_number)
        if bm_number != 0 and bm_number != bl_number:
            numbers.append(bm_number)
        if br_number != 0 and br_number != bm_number:
            numbers.append(br_number)

    return numbers


def get_part_two_result(lines):
    symbol_positions = get_symbol_positions(lines, r"\*")
    numbers_matrix = build_numbers_matrix(lines)
    total_gear_ratio = 0

    for symbol_position in symbol_positions:
        adjacent_numbers = get_unique_adjacent_numbers(symbol_position, numbers_matrix)
        # if it is a gear
        if len(adjacent_numbers) == 2:
            total_gear_ratio += adjacent_numbers[0] * adjacent_numbers[1]
    return total_gear_ratio

print(get_part_two_result(file_lines))
