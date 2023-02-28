from harmonic import harmonic_mean


def main():
    nums = [float(num) for num in range(1, 100_000_00)]
    print(nums)
    try:
        result = harmonic_mean(nums)
        print(result)
    except ZeroDivisionError:
        pass


if __name__ == "__main__":
    main()
