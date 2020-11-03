#include <stdio.h>
#include <string.h>

int main(int argc, char const *argv[])
{

    // if (0 == '\0')
    // {
    //     printf("0 == '\\0'");
    // }
    // else
    // {

    //     printf("0 != '\\0'");
    // }

    char src[] = "source";
    char dest[] = "destination";

    strncpy(dest, src, 2);

    printf("%s",dest);

    return 0;
}
