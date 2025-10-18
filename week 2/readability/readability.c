#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int letter_count(string text);
int word_count(string text);
int sentence_count(string text);

int main(void)
{
    // prompt text from the user
    string text = get_string("Text: ");

    // count number of letter, words and sentenses in the text
    int letter = letter_count(text);
    int word = word_count(text);
    int sentence = sentence_count(text);

    // compute the Coleman-Liau index
    float L = (float) letter / word * 100;
    float S = (float) sentence / word * 100;

    int index = (int) round(0.0588 * L - 0.296 * S - 15.8);

    // Print the grade level
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int letter_count(string text)
{
    int n = strlen(text);
    int letters = 0;
    for (int i = 0; i < n; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }

    return letters;
}
int word_count(string text)
{
    int n = strlen(text);
    int words = 1;
    for (int i = 0; i < n; i++)
    {
        if (text[i] == ' ')
        {
            words++;
        }
    }

    return words;
}
int sentence_count(string text)
{
    int n = strlen(text);
    int sentence = 0;
    for (int i = 0; i < n; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentence++;
        }
    }

    return sentence;
}
