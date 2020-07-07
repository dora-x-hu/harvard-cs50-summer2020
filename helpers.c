#include "helpers.h"

int roundToInt(double roundee)
{
    int lesser = (int)roundee;
    if((double)(lesser+1-roundee) > (double)(roundee-lesser))
    {
        return lesser;
    }
    else
    {
        return lesser+1;
    }
}

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    BYTE grayVal;
    for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            grayVal = roundToInt(image[i][j].rgbtBlue + image[i][j].rgbtRed + image[i][j].rgbtGreen) / 3;
            image[i][j].rgbtBlue = grayVal;
            image[i][j].rgbtRed = grayVal;
            image[i][j].rgbtGreen = grayVal;
        }
    }

    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    BYTE orRed, orGreen, orBlue;
    for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            orRed = image[i][j].rgbtRed;
            orGreen = image[i][j].rgbtGreen;
            orBlue = image[i][j].rgbtBlue;

            image[i][j].rgbtBlue = roundToInt(.272 * orRed + .534 * orGreen + .131 * orBlue);
            image[i][j].rgbtRed = roundToInt(.393 * orRed + .769 * orGreen + .189 * orBlue);
            image[i][j].rgbtGreen = roundToInt(.349 * orRed + .686 * orGreen + .168 * orBlue);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    BYTE leftRed, leftGreen, leftBlue;

    for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < width/2; j++)
        {
            leftRed = image[i][j].rgbtRed;
            leftGreen = image[i][j].rgbtGreen;
            leftBlue = image[i][j].rgbtBlue;

            image[i][j].rgbtRed = image[i][width-1-j].rgbtRed;
            image[i][j].rgbtGreen = image[i][width-1-j].rgbtGreen;
            image[i][j].rgbtBlue = image[i][width-1-j].rgbtBlue;

            image[i][width-1-j].rgbtRed = leftRed;
            image[i][width-1-j].rgbtGreen = leftGreen;
            image[i][width-1-j].rgbtBlue = leftBlue;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    BYTE sumRed, sumGreen, sumBlue, divide;

    for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            // same position
            sumRed = image[i][j].rgbtRed;
            sumBlue = image[i][j].rgbtBlue;
            sumGreen = image[i][j].rgbtGreen;
            divide = 1;

            // left
            if(j > 0)
            {
                sumRed += image[i][j-1].rgbtRed;
                sumBlue += image[i][j-1].rgbtBlue;
                sumGreen += image[i][j-1].rgbtGreen;
                divide++;
            }
            // right
            if(j < width-1)
            {
                sumRed += image[i][j+1].rgbtRed;
                sumBlue += image[i][j+1].rgbtBlue;
                sumGreen += image[i][j+1].rgbtGreen;
                divide++;
            }


            if(i > 0)
            {
                // one row up
                sumRed += image[i-1][j].rgbtRed;
                sumBlue += image[i-1][j].rgbtBlue;
                sumGreen += image[i-1][j].rgbtGreen;
                divide++;

                // left up
                if(j > 0)
                {
                    sumRed += image[i-1][j-1].rgbtRed;
                    sumBlue += image[i-1][j-1].rgbtBlue;
                    sumGreen += image[i-1][j-1].rgbtGreen;
                    divide++;
                }

                // right up
                if(j < width-1)
                {
                    sumRed += image[i-1][j+1].rgbtRed;
                    sumBlue += image[i-1][j+1].rgbtBlue;
                    sumGreen += image[i-1][j+1].rgbtGreen;
                    divide++;
                }
            }

            if(i < height-1)
            {
                // one row down
                sumRed += image[i+1][j].rgbtRed;
                sumBlue += image[i+1][j].rgbtBlue;
                sumGreen += image[i+1][j].rgbtGreen;
                divide++;

                // left down
                if(j > 0)
                {
                    sumRed += image[i+1][j-1].rgbtRed;
                    sumBlue += image[i+1][j-1].rgbtBlue;
                    sumGreen += image[i+1][j-1].rgbtGreen;
                    divide++;
                }

                // right down
                if(j < width-1)
                {
                    sumRed += image[i+1][j+1].rgbtRed;
                    sumBlue += image[i+1][j+1].rgbtBlue;
                    sumGreen += image[i+1][j+1].rgbtGreen;
                    divide++;
                }
            }

            copy[i][j].rgbtRed = roundToInt(sumRed/divide);
            copy[i][j].rgbtGreen = roundToInt(sumGreen/divide);
            copy[i][j].rgbtBlue = roundToInt(sumBlue/divide);
        }
    }

    for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            image[i][j] = copy[i][j];
        }
    }
    return;
}
