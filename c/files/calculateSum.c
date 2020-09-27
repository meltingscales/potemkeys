#include <stdio.h>
#include <stdlib.h> // For exit() function

static char *DATAFILE = "loanSheet.csv";
#define MAXCHAR 1000
#define MAXLOANSHEETITEMS 100

#define MAXNAMESIZE 50
#define MAXDATESIZE 50

struct LoanSheetItem
{
    char name[MAXNAMESIZE];
    long owed;
    char date[MAXDATESIZE];
};

int main()
{
    char buf[MAXCHAR];                                      //buffer to hold file line data
    FILE *fileptr = fopen(DATAFILE, "r");                   // open a file handle on file
    struct LoanSheetItem loanSheetItems[MAXLOANSHEETITEMS]; // array of LoanSheetItem structs to hold our data

    if (fileptr == NULL)
    {
        printf("Error opening file '%s'!\n", DATAFILE);
        // Program exits if file pointer returns NULL.
        exit(1);
    }

    int i = 0;
    while (fgets(buf, MAXCHAR, fileptr) != NULL)
    {
        if (i == 0)
        {
            printf("Header: %s", buf);
        }
        else
        {
            printf("Line %d: '%s'\n\n", i, buf);

            char name[MAXNAMESIZE];
            long owed;
            char date[MAXDATESIZE];

            // sscanf() //TODO sscanf into 3 fields, populate struct
        }
        i++;
    }

    return 0;
}
