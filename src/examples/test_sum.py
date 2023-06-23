from .sum import sum_numbers_bench


def test_sum(benchmark):
    benchmark(sum_numbers_bench)
