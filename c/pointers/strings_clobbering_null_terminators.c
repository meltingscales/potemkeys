#include <stdio.h>
#include <string.h>

/**
 * This code shows you what can happen to strings in C when you get rid of null terminators.
 */

int main(int argc, char const *argv[])
{

    char myString[] = "hello world!";

    myString[strlen(myString)] = 'X'; //This gets rid of the null terminator...Bad!

    for (int i = 0; i <strlen(myString); i++)
    {
        printf("myString[%2d]=0x%02x or '%c'\n", i, myString[i], myString[i]);
    }

    printf("\n\nsizeof(myString)='%lu', but strlen(myString)='%lu'..."
    "\nThis is bad! We only allocated %lu bytes for the string!",
    sizeof(myString),strlen(myString), sizeof(myString));


    return 0;
}
