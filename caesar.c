#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    string cipher;

    // checks for correct number of araguments
    if(argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // iterates through string to make sure it is a legitimate number
    cipher = argv[1];
    bool intOrNot = true;
    int len = strlen(cipher);
    for(int i=0; i<len; i++)
    {
        if(cipher[i] <= 48 || cipher[i] >= 57)
        {
            intOrNot = false;
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    int rotate = atoi(argv[1]);


    string plaintext = get_string("plaintext:\n");
    int len2 = strlen(plaintext);

    // convert original plaintext with cipher
    for(int i=0; i<len2; i++)
    {
        if(plaintext[i] >= 65 && plaintext[i] <= 90)
        {
            plaintext[i] += rotate%26;
            if(plaintext[i] > 90)
            {
                plaintext[i] -= 26;
            }
        }
        else if(plaintext[i] >= 97 && plaintext[i] <= 122)
        {
            if(127 - (rotate%26) < plaintext[i])
            {
                plaintext[i] -= 26;
                plaintext[i] += rotate%26;
            }
            else if(plaintext[i] + (rotate%26) > 122)
            {
                plaintext[i] += rotate%26;
                plaintext[i] -= 26;
            }
            else
            {
                plaintext[i] += rotate%26;
            }
        }
    }

    printf("ciphertext: %s\n", plaintext);
}