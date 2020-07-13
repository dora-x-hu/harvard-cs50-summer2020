// Implements a dictionary's functionality

#include <stdbool.h>

#include "dictionary.h"

#include <strings.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

bool started[N];
int numWords;
FILE *dicFile;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int index = hash(word);
    node *cursor = table[index];
    bool same;
    while(cursor != NULL)
    {
        same = strcasecmp(word, cursor->word);

        if(same==0)
        {
            return true;
        }
        cursor = cursor->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // get the first character in the word
    char first = *word;

    int ascii = first;
    if(ascii > 97)
    {
        return (ascii - 97);
    }
    return ascii - 65;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    char array[46];
    numWords = 0;

    // open dictionary file

    dicFile = fopen(dictionary, "r");
    if(dicFile == NULL)
    {
        return false;
    }

    node *insert;
    //node thisOne;

    node *start;
    int hashIndex;

    // reads individual words
    while(fscanf(dicFile, "%s", array) != EOF)
    {
        numWords++;

        // allocate memory for a new node
        insert = malloc(sizeof(node));

        if(insert == NULL)
        {
            return false;
        }

        // create new node to add to
        strcpy(insert->word, array); //put string as insert's value

        hashIndex = hash(insert->word);


        // if this is the first word that starts with this letter
        if(!started[hashIndex])
        {
            insert->next = NULL; //the first word's next doesn't point anywhere
            started[hashIndex] = true;
        }
        else
        {
            insert->next = table[hashIndex]; // start and insert's next are temporarily both pointers to the first element in the linked list
        }
        table[hashIndex] = insert; // start will become a pointer to insert now REGARDLESS of (insert is a pointer to the first word)

    }
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return numWords;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node *cursor;
    node *temp;

    for(int i = 0; i < N; i++)
    {
        cursor = table[i];
        temp = cursor;

        while(cursor != NULL)
        {
            cursor = cursor->next;
            free(temp);
            temp = cursor;
        }
    }

    fclose(dicFile);

    return true;
}