#include <stdio.h>
#include <string.h>

int main(int argc, char const *argv[])
{

    char myString[10] = {0};
    // char* myString2 = {0*10};

    myString[0] = 'h';
    myString[1] = 'e';

    for (int i = 0; i < sizeof(myString); i++)
    {
        printf("myString[%d]=0x%02x or '%c'\n",i,myString[i],myString[i]);
    }

    printf("strlen(myString) = '%lu'...NOT 10!",strlen(myString));

    return 0;
}
