from .harmonic import harmonic_mean_benchmark


def test_harmonic_mean(benchmark):
    result = benchmark(harmonic_mean_benchmark)
