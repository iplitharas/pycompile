def sum_numbers():
    numbers = [i for i in range(5_000_000)]
    total = 0
    for num in numbers:
        total += num
    return total


def sum_of_squares():
    n = 5_000_000
    numbers = [i for i in range(n)]
    numbers_squared = [i**2 for i in numbers]
    total = 0
    for num in numbers_squared:
        total += num
    return total


def sum_strings():
    result = ""
    for i in range(1, 100_000):
        result += str(i)
