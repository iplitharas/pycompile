def harmonic_mean(nums):
    return len(nums) / sum(1 / num for num in nums)


def harmonic_mean_benchmark():
    nums = [float(num) for num in range(1, 5_000_000)]
    try:
        result = harmonic_mean(nums)
    except ZeroDivisionError:
        pass
