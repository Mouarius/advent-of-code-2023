with open("./day-1/input.txt") as file:
    lines = file.readlines()

sum = 0
for line in lines:
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

    sum += first_digit*10 + last_digit

print(f"The final code is: {sum}")
