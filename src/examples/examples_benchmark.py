from .fib import fibonacci
from .harmonic import harmonic_mean
from .sum import sum_numbers, sum_of_squares, sum_strings


def samples_benchmark():
    sum_of_squares()
    harmonic_mean()
    fibonacci(30)
    sum_numbers()
    sum_strings()
