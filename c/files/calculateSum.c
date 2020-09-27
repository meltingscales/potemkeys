#include <stdio.h>
#include <stdlib.h> // For exit() function

static char *DATAFILE = "data.csv";
#define MAXCHAR 1000

int main()
{
    char buf[MAXCHAR];
    FILE *fileptr = fopen(DATAFILE, "r");

    if (fileptr == NULL)
    {
        printf("Error opening file '%s'!\n", DATAFILE);
        // Program exits if file pointer returns NULL.
        exit(1);
    }

    int i = 0;
    while (fgets(buf, MAXCHAR, fileptr) != NULL)
    {
        printf("Line %d: '%s'\n\n", i, buf);
        i++;
    }

    return 0;
}
