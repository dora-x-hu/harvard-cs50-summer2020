def balanceable(numbers):
    sum = 0
    max = 0
    for element in numbers:
        sum += element
        if element > max:
            max = element

    if sum%2 == 1:
        return False
    if max > float(sum)/2:
        return False

    return isThere(numbers, sum/2, 0)


def isThere(numbers, sum, index):
    if sum == 0:
        return True
    if sum < 0:
        return False
    if index == len(numbers):
        return False
    return isThere(numbers, sum-numbers[index], index+1) or isThere(numbers, sum, index+1)