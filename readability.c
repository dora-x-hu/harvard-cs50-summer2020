#include <cs50.h>
#include <string.h>
#include <stdio.h>

double grade(string sample);

int main(void)
{
    string text = get_string("Text: ");
    double mygrade = grade(text);

    int index = mygrade;

    if(index<1)
    {
        printf("Below Grade 1\n");
    }
    else if(index>16)
    {
        printf("Grade 16+\n");
    }
    else if(-mygrade+index+1 < mygrade-index)
    {
        printf("Grade %i\n", index+1);
    }
    else
    {
        printf("Grade %i\n", index);
    }

}


double grade(string sample)
{
    int i=0;
    double letters=0, words=0, sentences=0;
    int n = strlen(sample);
    while(i<n)
    {
        // letter counter: is this character a-z
        if((sample[i]>=65 && sample[i]<=90) || (sample[i]>=97 && sample[i]<=122))
        {
            letters++;
        }
        // sentence counter: is there end-sentence punctuation?
        if(sample[i]=='.' || sample[i]=='?' || sample[i]=='!')
        {
            sentences++;
        }
        // word counter: is this character sin a-z? If it is, then is the next character a space?
        if( ((sample[i]>=65 && sample[i]<=90) || (sample[i]>=97 && sample[i]<=122)) && /*(sample[i+1] == '\0' || (!(sample[i+1]>=65 && sample[i+1]<=90) && !(sample[i+1]>=97 && sample[i+1]<=122)) )*/ (sample[i+1]==' ' || sample[i+1]=='\0') )
        {
            words++;
        }
        i++;
    }

    double L = letters/words * 100;
    double S = sentences/words * 100;

    double thisGrade = 0.0588 * L - 0.296 * S - 15.8;

    return thisGrade;
}