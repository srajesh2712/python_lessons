def sum_two_smallest_numbers(numbers):
    numbers = sorted(numbers)
    return numbers[0] + numbers[1]

if __name__ == '__main__':
    print(sum_two_smallest_numbers([10, 343445353, 3453445, 3453545353453]))