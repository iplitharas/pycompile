def sum_numbers(numbers):
    total = 0
    for num in numbers:
        total += num
    return total


def sum_numbers_bench():
    sum_numbers([i for i in range(5_000_000)])
