import re

with open("./day-1/input.txt") as file:
    lines = file.readlines()


def get_part_one_code(input: list[str]) -> int:
    sum = 0
    for line in input:
        first_digit = None
        last_digit = None
        for char in line:
            try:
                digit = int(char)
                if not first_digit:
                    first_digit = digit
                last_digit = digit
            except ValueError:
                continue

        if first_digit is None or last_digit is None:
            raise ValueError("Digits cannot be none")

        sum += first_digit * 10 + last_digit
    return sum

def find_first_digit(input:str) -> int:
    pattern = re.compile(r"((one|two|three|four|five|six|seven|eight|nine)|(\d))")
    str_numbers = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }
    match = pattern.search(input).group()
    try:
        digit = int(match)
    except ValueError:
        digit = int(str_numbers[match])
    return digit


def find_last_digit(input:str) -> int:
    pattern = re.compile(r"((eno|owt|eerht|ruof|evif|xis|neves|thgie|enin)|(\d))")
    str_numbers = {
        "eno": 1,
        "owt": 2,
        "eerht": 3,
        "ruof": 4,
        "evif": 5,
        "xis": 6,
        "neves": 7,
        "thgie": 8,
        "enin": 9,
    }
    reversed_line = ""
    for char in reversed(input):
        reversed_line+= char
    match = pattern.search(reversed_line).group()
    try:
        digit = int(match)
    except ValueError:
        digit = int(str_numbers[match])

    return digit

def get_part_two_code(input: list[str]) -> int:
    sum = 0
    for line in input:
        first_digit = find_first_digit(line)
        last_digit = find_last_digit(line)
        sum += first_digit * 10 + last_digit
    return sum

print(get_part_two_code(lines))
