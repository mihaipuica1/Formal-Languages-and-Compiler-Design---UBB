%{
#include <stdio.h>
#include <stdlib.h>

#define YYDEBUG 1
%}

%token &START&
%token &END&
%token LET
%token &
%token NUMBER
%token STRING 
%token ARRAY_NUMBERS 
%token IF 
%token WHILE 
%token FOR 
%token READ 
%token PRINT 

%token (
%token ) 
%token [
%token ]
%token {
%token }
%token ;
%token :
%token  

%token +
%token -
%token *
%token /
%token <-
%token ++
%token AND
%token OR
%token SMALLER_THAN
%token BIGGER_THAN
%token EQUALS
%token NOT_EQUALS

%%

program : &START& compound_statement &END&
declaration_statement : LET identifier $ type ;
type : NUMBER | STRING | array_numbers
expression : expression ( + | - ) term | term
term : term (* | / | MOD) factor | factor
factor : ( expression ) | const | identifier
assign_statement : IDENTIFIER <- expression ;
input_output_statement = "read" | "write" IDENTIFIER ;
compound_statement : declaration_statement ; statement | declaration_statement ; statement ; compound_statement ;
statement : simple_statement | struct_statement ;
simple_statement : assign_statement | input_output_statement ;
condition : expression relation expression (|| | && condition)
relation : SMALLER_THAN | BIGGER_THAN | EQUALS | NOT_EQUALS
if_statement : IF ( condition ) { compound_statement } ELSE { compound_statement } ;
while_statement : WHILE ( condition ) { compound_statement } ;
for_statement : FOR ( assign_statement ; condition ; compound_statement ) { compound_statement } ;
struct_statement : if_statement | while_statement | for_statement

%%

yyerror(char *s)
{
    printf("%s\n", s);
}

extern FILE *yyin;

main(int argc, char **argv)
{
    if (argc > 1) 
        yyin = fopen(argv[1], "r");

    if ( (argc > 2) && ( !strcmp(argv[2], "-d") ) ) 
        yydebug = 1;

    if ( !yyparse() ) 
        fprintf(stderr,"\t U GOOOOOD !!!\n");
}