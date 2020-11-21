#include <stdio.h>
#include <stdlib.h>

int main(int argc, char const *argv[]) {


  printf("argc is %d\n",argc);
  for (int i = 0; i < argc; i++)
  {
    printf("argument %d = %s\n",i,argv[i]);
  }  
  
  if(argc < 3)
  {
    float a = 3.0;
    float b = 4.0;
        
    printf("Gimme two numbers to multiply on the command-line!\n");
    printf("Example: '%s %f %f' -> %f\n", argv[0], a, b, (a*b));
  }
  else
  {
    float a, b;
    int ai = sscanf(argv[1], "%f", &a);
    int bi = sscanf(argv[2], "%f", &b);
    
    if((ai == bi) && (bi == 1))
    {
      printf("%f * %f = %f\n", a, b, (a * b));
    }
    else
    {
      printf("You didn't give me two numbers!\n");
      if(!ai)
      {
        printf("'%s' isn't a number.\n", argv[1]);
      }
      if(!bi)
      {
        printf("'%s' isn't a number.\n", argv[2]);
      }
    }
  }


  return 0;
}
