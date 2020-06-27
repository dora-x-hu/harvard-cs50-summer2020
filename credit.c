#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long number = get_long("Number: ");
    long number2 = number;
    long number3 = number;


    int sum = 0; // sum of digits of products of 2 and every other digit of number
    int thisNum;

    number = number/10; // start with 2nd last digit
    while(number>0)
    {
        // last digit * 2
        thisNum = number%10;
        thisNum = thisNum * 2;

        // add sum of digits in last digit * 2 to total sum
        while(thisNum>0)
        {
            sum += (thisNum%10);
            thisNum = thisNum/10;
        }

        // every other digit
        number = number/100;
    }

    while(number2>0)
    {
        sum += number2 % 10;

        number2 = number2 / 100;
    }

    bool valid;
    // checks sum ends in 0 condition
    if(sum%10 == 0)
    {
        valid = true;
    }
    else
    {
        valid = false;
    }


    int numDigits = 0;
    if(!valid)
    {
        printf("INVALID\n");
    }
    else
    {
        // finds number of digits
        while(number3>99)
        {
            number3 = number3 / 10;
            numDigits++;
        }

        if((number3 == 34 || number3 == 37) && numDigits==13)
        {
            printf("AMEX\n");
        }
        else if(number3 >= 51 && number3 <=55 && numDigits==14)
        {
            printf("MASTERCARD\n");
        }
       else  if(number3 / 10 == 4 && (numDigits==11 || numDigits==14))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }

}