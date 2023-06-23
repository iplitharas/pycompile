from .sum_of_sqaures import sum_of_squares_benchmark


def test_sum_of_squares(benchmark):
    benchmark(sum_of_squares_benchmark)
