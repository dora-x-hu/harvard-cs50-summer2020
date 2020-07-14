from cs50 import get_string

def main():
    number = get_string("Number: ")
    intnumber = int(number)
    isCard = valid(intnumber)
    if isCard == False:
        print("INVALID")
        exit(1)
    findtype(intnumber)
    exit(0)


def valid(num):
    num2 = num
    sum = 0
    # start with 2nd-to-last digit
    num //= 10
    started = False
    while num > 0:
        # get the end digit times 2
        thisNum = num%10
        thisNum *= 2
        # get the sum of the digits of (end digit * 2)
        while thisNum > 0:
            sum += thisNum%10
            thisNum //= 10
        # every other digit
        num //= 100
    # add the sum of the digits that weren't multiplied by 2
    while num2 > 0:
        sum += num2%10
        num2 //= 100
    # valid if the end sum is divisible by 10
    if sum % 10 == 0:
        return True
    return False

def findtype(num):
    digits = 0
    # find first 2 digits (when reading from left to right)
    while num > 99:
        num //= 10
        digits += 1
    if (num == 34 or num == 37) and digits+2 == 15:
        print("AMEX")
    elif (num >= 51 and num <= 55) and digits+2 == 16:
        print("MASTERCARD")
    elif num // 10 == 4 and (digits+2 == 13 or digits+2 == 16):
        print("VISA")
    else:
        print("INVALID")

main()
