#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    // validate Command-line argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    int n = strlen(argv[1]);
    for (int i = 0; i < n; i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    int key = atoi(argv[1]);
    key = key % 26;

    // take input from the user (plaintext)
    string plain = get_string("plaintext: ");

    // print the encryted text (ciphertext)
    printf("ciphertext: ");

    for (int i = 0, len = strlen(plain); i < len; i++)
    {
        if (isalpha(plain[i]))
        {
            if (isupper(plain[i]))
            {
                printf("%c", (plain[i] - 'A' + key) % 26 + 'A');
            }
            else
            {
                printf("%c", (plain[i] - 'a' + key) % 26 + 'a');
            }
        }

        else
        {
            printf("%c", plain[i]);
        }
    }

    printf("\n");
    return 0;
}
