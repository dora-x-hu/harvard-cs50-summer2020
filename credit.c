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
        thisNum = number%10;
        thisNum = thisNum * 2;
        while(thisNum>0)
        {
            sum += (thisNum%10);
            thisNum = thisNum/10;
        }

        number = number/100;
    }

    while(number2>0)
    {
        sum += number2 % 10;

        number2 = number2 / 100;
    }

    bool valid;

    if(sum%10 == 0)
    {
        valid = true;
    }
    else
    {
        valid = false;
    }



    if(!valid)
    {
        printf("INVALID\n");
    }
    else
    {
        while(number3>99)
        {
            number3 = number3 / 10;
        }

        if(number3 == 34 || number3 == 37)
        {
            printf("AMEX\n");
        }
        else if(number3 >= 51 && number3 <=55)
        {
            printf("MASTERCARD\n");
        }
       else  if(number3 / 10 == 4)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }

}