#!/bin/bash

# Clean previous build artifacts
rm -f lex.yy.c parser.tab.c parser.tab.h compiler log.txt error.txt

echo "Running Bison parser generator..."
bison -d -y parser.y -o parser.tab.c

echo "Running Flex lexical scanner..."
flex -o lex.yy.c lexer.l

echo "Compiling parser and lexer with g++..."
g++ -w -o compiler parser.tab.c lex.yy.c

if [ $? -eq 0 ]; then
    echo "Build successful! Executing with input.txt..."
    ./compiler input.txt
else
    echo "Compilation failed."
    exit 1
fi
