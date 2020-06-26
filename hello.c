#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //asks user for name
    string yourName = get_string("What's your name?");
    //prints "hello," followed by user's name
    printf("hello, %s\n", yourName);
}