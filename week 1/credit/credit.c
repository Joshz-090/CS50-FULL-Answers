#include <cs50.h>
#include <stdio.h>
int main(void)
{
    long card;
    do
    {
        card = get_long("Number: ");
    }
    while (card <= 0);

    int length = 0;
    long t_card = card;

    do
    {
        length++;
        t_card /= 10;
    }
    while (t_card > 0);

    if (length != 13 && length != 15 && length != 16)
    {
        printf("INVALID\n");
        return 0;
    }

    int sum = 0;
    t_card = card;
    int position = 0, mod;

    do
    {
        mod = t_card % 10;
        t_card /= 10;
        position++;

        if (position % 2 == 0)
        {
            mod *= 2;
            sum = sum + (mod / 10) + (mod % 10);
        }

        else
        {
            sum += mod;
        }
    }
    while (t_card > 0);

    if (sum % 10 != 0)
    {
        printf("INVALID\n");
        return 0;
    }
    else
    {
        long start = card;

        do
        {
            start /= 10;
        }
        while (start >= 100);

        if ((length == 13 || length == 16) && (start / 10 == 4))
        {
            printf("VISA\n");
        }

        else if (length == 15 && (start == 37 || start == 34))
        {
            printf("AMEX\n");
        }
        else if (length == 16 && (start > 50 && start < 56))
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
}
