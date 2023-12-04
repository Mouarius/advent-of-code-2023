with open("./day-2/input.txt") as file:
    data = file.readlines()

initial_cubes = (12, 13, 14)  # (red, green, blue)


def parse_game_information(line: str) -> tuple[int, list[tuple[int]]]:
    game_id, game_content = (line.lstrip("Game ").rstrip("\n")).split(":")
    round_list = game_content.split(";")
    rounds = []
    for round_value in round_list:
        round_total = [0, 0, 0]
        for amount_color in round_value.split(","):
            amount, color = amount_color.strip().split(" ")
            round_value = (
                int(amount) * (color == "red"),
                int(amount) * (color == "green"),
                int(amount) * (color == "blue"),
            )
            round_total = tuple(
                total + value for total, value in zip(round_total, round_value)
            )
        rounds.append(round_total)
    return (game_id, rounds)


def is_round_possible(initial_cubes: tuple[int], showed_cubes: tuple[int]) -> bool:
    for icube, scube in zip(initial_cubes, showed_cubes):
        if scube > icube:
            return False
    return True


def is_game_possible(
    initial_cubes: tuple[int], game: tuple[int, list[tuple[int]]]
) -> bool:
    for round in game[1]:
        if not is_round_possible(initial_cubes, round):
            return False
    return True


def get_result(initial_cubes, lines):
    total = 0
    for line in lines:
        game = parse_game_information(line)
        total += int(game[0]) * (is_game_possible(initial_cubes, game))
    return total


print(get_result(initial_cubes, data))
