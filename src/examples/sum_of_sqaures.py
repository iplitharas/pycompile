def sum_of_squares(n):
    return sum([i**2 for i in range(1, n + 1)])


def sum_of_squares_benchmark():
    result = sum_of_squares(5_000_000)
