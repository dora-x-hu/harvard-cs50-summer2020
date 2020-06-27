#include <cs50.h>
#include <stdio.h>

int main(void)
{

    int height = get_int("Height: \n");
    //asks for height until it gets a proper one
    while(height < 1 || height > 8)
    {
        height = get_int("Height: ");
    }

    //each i loop represents a level of the pyramid
    for(int i=1; i<=height; i++)
    {
        //spaces on left
        for(int j=0; j<height-i; j++)
        {
            printf(" ");
        }
        //hashtags on left
        for(int j=0; j<i; j++)
        {
            printf("#");
        }

        //middle
        printf("  ");

        //hashtags on right
        for(int j=0; j<i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}