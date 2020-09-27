#include <stdio.h>
#include <string.h>
#include <stdlib.h> // For exit() function

static char *DATAFILE = "loanSheet.csv";
#define MAXCHAR 1000
#define MAXLOANSHEETITEMS 10

#define MAXNAMESIZE 50
#define MAXDATESIZE 50
// #define DEBUG

struct LoanSheetItem
{
    char name[MAXNAMESIZE];
    long owed;
    char date[MAXDATESIZE];
};

void printLoanSheetItem(struct LoanSheetItem lsi)
{
    printf("LoanSheetItem->{name:'%s',owed:'%d',date:'%s'}\n", lsi.name, lsi.owed, lsi.date);
}

int main()
{
    char buf[MAXCHAR];                                      // buffer to hold file line data
    FILE *fileptr = fopen(DATAFILE, "r");                   // open a file handle on file
    struct LoanSheetItem loanSheetItems[MAXLOANSHEETITEMS]; // array of LoanSheetItem structs to hold our data

    if (fileptr == NULL)
    {
        printf("Error opening file '%s'!\n", DATAFILE);
        // Program exits if file pointer returns NULL.z
        exit(1);
    }

    int i = 0;
    int numLoanSheetItems = 0;
    while (fgets(buf, MAXCHAR, fileptr) != NULL)
    {
        if (i == 0)
        {
            printf("Header: %s", buf);
        }
        else
        {
            // printf("Line %d: '%s'\n\n", i, buf);

            char name[MAXNAMESIZE];
            long owed;
            char date[MAXDATESIZE];

            //TODO sscanf into 3 fields, populate struct
            sscanf(buf, "%[^,],%d,%[^,\n]\n", name, &owed, date);

            /* Ok, WTF is this format string??? Well...

                "%[^,],%d,%[^,\n]\n"
            
                 %[^,]
            Match strings that do NOT have commas. Saves to memory location pointed to by 'name' pointer. 
            
                       ,
            Match a comma.
            
                       %d
            Match an int. Saves to memory location of 'owed' variable (&owed).
            
                         ,
            Match a comma.
            
                          %[^,\n]
            Match strings that do NOT have commas OR NEWLINES. Saves to memory location pointed to by 'date' pointer.
            
                                 \n 
            Match a newline. Not necessary BTW.
            */

#ifdef DEBUG
            printf("line %d:\n", i);
            printf("name: '%s'\n", name);
            printf("owed: '%ld'\n", owed);
            printf("date: '%s'\n", date);
            printf("\n");
#endif

            // i-1 because we ignore the header and `i` counts rows...
            numLoanSheetItems = i - 1;

            struct LoanSheetItem loanSheetItem = loanSheetItems[numLoanSheetItems];

            strncpy(loanSheetItem.name, name, MAXNAMESIZE);
            loanSheetItem.owed = owed;
            strncpy(loanSheetItem.date, date, MAXDATESIZE);

            printLoanSheetItem(loanSheetItem);
        }
        i++;
    }

    return 0;
}
