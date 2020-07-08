#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if(argc != 2)
    {
        printf("Usage:");
        return 1;
    }

    // sets up the file for reading
    FILE *file = fopen(argv[1], "r");

    for(int)


    unsigned char bytes[3];
    fread(bytes, 3, 1, file);
    char filename[7];

    if(bytes[0] == 0xff && bytes[1] == 0xd8 && bytes[2] == 0xff)
    {
        sprintf(filename, "%03i.jpg", 0);
    }
}
