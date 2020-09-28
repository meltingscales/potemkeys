#include <stdio.h>
#include <string.h>
#include <stdlib.h> // For exit() function

static char *DATAFILE = "loanSheet.csv";    // Input file
static char *OUTFILE = "loanSheet.out.txt"; // Output file

#define MAXCHAR 1000
#define MAXLOANSHEETITEMS 10

#define MAXNAMESIZE 50
#define MAXDATESIZE 50
// #define DEBUG

struct LoanSheetItem
{
    char name[MAXNAMESIZE];
    float owed;
    char date[MAXDATESIZE];
};

void printLoanSheetItem(struct LoanSheetItem *lsi)
{
    printf("LoanSheetItem->{name:'%s',owed:'%.2f',date:'%s'}\n", lsi->name, lsi->owed, lsi->date);
}

void writeLoanSheetItemToFile(FILE *f, struct LoanSheetItem *lsi)
{
    char buf[MAXCHAR];

    // copy content to buf
    snprintf(buf, sizeof(buf), "'%s' owes $%.2f incurred on %s", lsi->name, lsi->owed, lsi->date);

    // copy buf to file stream
    fputs(buf, f);
}

int main()
{
    struct LoanSheetItem loanSheetItems[MAXLOANSHEETITEMS]; // array of LoanSheetItem structs to hold our data
    char buf[MAXCHAR];                                      // buffer to hold file line data
    FILE *fileptr = fopen(DATAFILE, "r");                   // open a file handle on file

    if (fileptr == NULL)
    {
        printf("Error opening file '%s'!\n", DATAFILE);
        // Program exits if file pointer returns NULL.z
        exit(1);
    }

    int i = 0;
    int numLoanSheetItems = 0;
    float totalOwed = 0;

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
            float owed;
            char date[MAXDATESIZE];

            //TODO sscanf into 3 fields, populate struct
            sscanf(buf, "%[^,],%f,%[^,\n]\n", name, &owed, date);

            /* Ok, WTF is this format string??? Well...

                "%[^,],%f,%[^,\n]\n"
            
                 %[^,]
            Match strings that do NOT have commas. Saves to 'name'.
            
                       ,
            Match a comma.
            
                       %f
            Match a float. Saves to 'owed' (&owed).
            
                         ,
            Match a comma.
            
                          %[^,\n]
            Match strings that do NOT have commas OR NEWLINES. Saves to 'date'.
            
                                 \n 
            Match a newline. Not necessary BTW.
            */

#ifdef DEBUG
            printf("line %d:\n", i);
            printf("name: '%s'\n", name);
            printf("owed: '%.2f'\n", owed);
            printf("date: '%s'\n", date);
            printf("\n");
#endif

            // i-1 because we ignore the header and `i` counts rows...
            numLoanSheetItems = i - 1;

            struct LoanSheetItem *loanSheetItem = &loanSheetItems[numLoanSheetItems];

            strncpy(loanSheetItem->name, name, MAXNAMESIZE);
            loanSheetItem->owed = owed;
            strncpy(loanSheetItem->date, date, MAXDATESIZE);

            totalOwed += owed;

            printLoanSheetItem(loanSheetItem);
        }
        i++;
    }

    numLoanSheetItems++; // because header was ignored...

    if (fclose(fileptr) != 0)
    {
        printf("Error %d when closing file '%s'!", DATAFILE, errno);
        exit(errno);
    };

    printf("Total owed: $%.2f", totalOwed);

    // Write data out to file

    fileptr = fopen(OUTFILE, "w+"); // open a file handle on file, create file if DNE, truncate file if it exists

    fputs("========== LOAN REPORT ==========\n", fileptr);
    fprintf(fileptr, " > Total Owed: $%.2f\n", totalOwed);
    fprintf(fileptr, " > Total Records: %d\n", numLoanSheetItems);
    fputs("\n", fileptr);

    for (int i = 0; i < numLoanSheetItems; i++)
    {
        struct LoanSheetItem *loanSheetItem = &loanSheetItems[i];

#ifdef DEBUG
        printLoanSheetItem(loanSheetItem);
        printf("ducky %d\n", i);
#endif

        writeLoanSheetItemToFile(fileptr, loanSheetItem);

        if (i != numLoanSheetItems) //avoid trailing '\n'
        {
            fputc('\n', fileptr);
        }
    }

    if (fclose(fileptr) != 0)
    {
        printf("Error %d when closing file '%s'!", OUTFILE, errno);
        exit(errno);
    };

    return 0;
}
