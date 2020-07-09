#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main(int argc, char *argv[])
{
    if(argc != 2)
    {
        printf("Usage:");
        return 1;
    }

    // sets up the file for reading
    FILE *file = fopen(argv[1], "r");
    //FILE *file_output = fopen("p_0000.jpg", "w");

    unsigned char buffer[512];
    char filename[8];
    //int numPics;



    bool start = false;

    int index=0;

    FILE *img;

    // while the end of the file hasn't been reached yet:
    while(fread(buffer, 1, 512, file) == 512)
    {
        // if the 1st four bites indicate that this is the start of a JPEG
        if(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //if very first jpeg found
            if(!start)
            {
                // show that the first jpeg has been found
                start = true;

                // prints name of jpeg
                sprintf(filename, "%03i.jpg", index);

                // opens new file to write in
                img = fopen(filename, "w");

                index++;
            }
            // not the first jpeg
            else
            {
                fclose(img);

                // start writing file
                sprintf(filename, "%03i.jpg", index);

                //
                img = fopen(filename, "w");

                index++;

            }
        }
        // not the start of a jpeg

        if(start)
            {
                fwrite(buffer, 1, 512, img);
            }

    }

    fclose(img);
    fclose(file);

}
