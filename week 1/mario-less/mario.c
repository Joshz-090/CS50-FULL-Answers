#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int hight;
    do
    {
        hight = get_int("Hight: ");
    }
    while (hight <= 0 || hight > 8);

    for (int i = 1; i <= hight; i++)
    {
        for (int j = hight - 1; j >= i; j--)
        {

            printf(" ");
        }
        for (int j = 1; j <= i; j++)
        {

            printf("#");
        }

        printf("\n");
    }
}
