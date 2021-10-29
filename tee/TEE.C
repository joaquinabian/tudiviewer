/**************************************
 * TEE.C - ANSI C
 * A very simple TEE
 * jcm@individual.EUnet.pt
 */

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char ** argv)
    {
    char C, *P;
    FILE * Out;

    if (*argv[1]) P = &argv[1][0];
    else P= &argv[0][0];

    switch (argc)
       {
       case 1 :	(Out = (FILE *) fopen("tee.out", "w"));
		/* Write to tee.out */
		break;
       case 2 : if (*P =='-')
		   {
		   P++;
		   if ((*P =='a') || (*P=='A'))
		   (Out = (FILE *) fopen("tee.out", "a"));
		   /* Append to tee.out */
		   break;
		   }
		 else (Out = (FILE *) fopen(argv[1], "w"));
		      /* Write to file named argv[1] */
		 break;

       case 3 : if (*P =='-')
		   {
		   P++;
		   if ((*P =='a') || (*P=='A'))
		   (Out = (FILE *) fopen(argv[2], "a"));
		   /* Append to file named argv[2] */
		   else (Out = (FILE *) fopen(argv[1], "w"));
		      /* Write to file named argv[1] */
		   break;
		   }
		 else (Out = (FILE *) fopen(argv[1], "w"));
		      /* Write to file named argv[1] */
		 break;

       }

    if (! Out)
       {
       fprintf(stderr,"\ntee: cannot open tee-file. USE: [pipe] | TEE [-a] [tee-file]\n");
       exit(1);
       }

    while ((C=putc(getc(stdin), stdout)) != EOF)
	putc(C, Out);
    putc(EOF, Out);

    fclose(Out);

    return 0;
    }
