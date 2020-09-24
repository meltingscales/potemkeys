#include <stdio.h>
#include <string.h>

int main(int argc, char const *argv[])
{

    char myString[15] = {0};
    // char* myString2 = {0*10};

    myString[0] = 'h';
    myString[1] = 'e';

    char* data = "llo world";
    // char* data = "llo world... oh crap, uncommenting this line, and commenting out the previous line, is going to result in a buffer overflow. Better do math before I copy data, or use a safe memory copying function.";
    

    strcpy(myString + 2, data);

    for (int i = 0; i < sizeof(myString); i++)
    {
        printf("myString[%2d]=0x%02x or '%c'\n",i,myString[i],myString[i]);
    }

    printf("\nstrlen(myString) = '%lu'...NOT %lu, %lu being the NUMBER OF BYTES we allocated for the string!\n\n",strlen(myString), sizeof(myString), sizeof(myString));

    printf("byte at %luth index (should be null terminator) of myString is '0x%02x'\n\n",sizeof(myString),myString[sizeof(myString)]);

    return 0;
}
