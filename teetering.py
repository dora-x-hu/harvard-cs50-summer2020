def balanceable(numbers):
    sum = 0
    max = 0
    # find the largest element as well as the sum of all the elements
    for element in numbers:
        sum += element
        if element > max:
            max = element

    # if the sum is odd numbers is not balanceable
    if sum%2 == 1:
        return False
    # if the largest element is too big, numbers is not balanceable
    if max > float(sum)/2:
        return False

    # calls a helper function that returns whether elements in numbers can be added together to get exactly half the sum
    return isThere(numbers, sum/2, 0)

# helper function: parameters are the list, the target sum(when called in balanceable, this equals the sum/2), and the current index of the list
def isThere(numbers, sum, index):
    # if the target sum has been reached by adding elements of the list
    if sum == 0:
        return True

    # if by adding elements in this order, we exceed the target sum
    if sum < 0:
        return False

    # if we have reached the end of the list but the target sum has not been reached
    if index == len(numbers):
        return False

    # add the element at this index or don't, then proceed to the next index
    # (this uses OR statements so that if the target sum is reached at all, the function returns true)
    return isThere(numbers, sum-numbers[index], index+1) or isThere(numbers, sum, index+1)