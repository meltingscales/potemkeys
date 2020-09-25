#include <stdio.h>
#include <string.h>

/*
This file demonstrates pointers, pointer math, and how strings are allocated in memory.
*/

int main(int argc, char const *argv[])
{

    // char myString[20]; //Note that this line will cause the unallocated array contents to be whatever was previously in memory.
    char myString[20] = {0 * 0};
    // char* myString2 = {0*10};

    myString[0] = 'h';
    myString[1] = 'e';

    char *data = "llo world";
    // char* data = "llo world... oh crap, uncommenting this line, and commenting out the previous line, is going to result in a buffer overflow. Better do math before I copy data, or use a safe memory copying function.";

    strcpy(myString + 2, data);
    //    strcpy(myString + 12, "test");

    for (int i = 0; i < sizeof(myString) + 1; i++)
    {
        printf("myString[%2d]=0x%02x or '%c'\n", i, myString[i], myString[i]);
    }

    printf("\nstrlen(myString) = '%lu'...NOT %lu, %lu being the NUMBER OF BYTES we allocated for the string!\n\n", strlen(myString), sizeof(myString), sizeof(myString));

    printf("byte at %luth index (is NOT null terminator due to way the string was initialized) of myString is '0x%02x'\n\n", sizeof(myString), myString[sizeof(myString)]);

    return 0;
}
