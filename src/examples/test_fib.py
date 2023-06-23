from .fib import fibonacci_benchmark


def test_fib(benchmark):
    benchmark(fibonacci_benchmark)
