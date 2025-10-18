#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int value[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

void winner(int score1, int score2);
int compute(string word);

int main(void)
{
    // get input from the 2 differnt player
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // compute which word is get more score
    int playerScore1 = compute(word1);
    int playerScore2 = compute(word2);

    // print the winner
    winner(playerScore1, playerScore2);
}

int compute(string word)
{
    int score = 0;
    int len = strlen(word);

    for (int i = 0; i < len; i++)
    {
        if (isupper(word[i]))
        {
            score += value[word[i] - 'A'];
        }

        if (islower(word[i]))
        {
            score += value[word[i] - 'a'];
        }
    }

    return score;
}

void winner(int score1, int score2)
{
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }

    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }

    else
    {
        printf("Tie!\n");
    }
}
