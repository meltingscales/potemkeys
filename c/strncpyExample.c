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

    
    char src[10];
    char dest[10];

    strncpy(src, "source", 6);
    printf("%s\n", src);

    for(int i =0;i<sizeof(src); i++){
        printf("src[%d] = %d or %c\n",i,src[i],src[i]);
        // This shows how `strncpy` does not add null terminating characters.
    }

    strncpy(dest, "destination", sizeof(dest));
    printf("%s", dest);

    return 0;
}
