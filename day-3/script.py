import re
import numpy as np
from pprint import pprint

with open("./input.txt") as file:
    file_lines = file.readlines()


def get_symbol_positions_in_line(line: str, line_index: int):
    positions = set()
    regex = r"(?!\.\d)([^\.\d\n])"
    matches = re.finditer(regex, line, re.MULTILINE)
    for match in matches:
        positions.add((match.start(), line_index))
    return positions


def get_symbol_positions(lines: list[str]):
    index = 0
    symbol_positions = set()
    for line in lines:
        symbol_positions = symbol_positions.union(
            get_symbol_positions_in_line(line, index)
        )
        index += 1
    return symbol_positions


test_lines = (
    "....45....\n",
    "*...?.....\n",
    "100..2....\n",
    "..%.....4.\n",
)


def build_adjacent_matrix(lines):
    """
    Returns a matrix with ones on positions adjacent to a symbol and zeros everywhere else
    """
    width = len(lines[0].rstrip("\n"))
    height = len(lines)
    adj_matrix = np.zeros((height, width), dtype=int)
    symbol_positions = get_symbol_positions(lines)
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
    adj = build_adjacent_matrix(lines)
    num = build_numbers_matrix(lines)
    res = [[ val * index for val, index in zip(num[i], adj[i])] for i in range(len(adj))]
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
