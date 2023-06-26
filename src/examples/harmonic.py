def harmonic_mean():
    nums = [float(num) for num in range(1, 5_000_000)]
    return len(nums) / sum(1 / num for num in nums)
