# C-Subset Compiler Front-End: Lexical & Syntax Analyzer

A multi-phase compiler front-end implementation designed using **Flex (Fast Lexical Analyzer)** and **Bison / Yacc (LALR Parser)** with an integrated custom **Symbol Table** data structure in C/C++.

---

## Architecture & Compiler Pipeline

1. **Lexical Analysis (`lexer.l` / `scanner.l`):**
   - Tokenizes C-subset source code: identifiers, keywords, integer/floating-point literals, arithmetic/relational operators, and control constructs.
   - Handles comment stripping (single-line `//` and multi-line `/* ... */`) and line tracking for precise syntax error reporting.

2. **Syntax & Semantic Parsing (`parser.y`):**
   - Context-Free Grammar (CFG) rules compiled using Bison into an LALR(1) parsing table.
   - Enforces variable declaration scoping, operand type matching, and syntax error recovery.

3. **Symbol Table Management (`symbol_info.h`):**
   - Hash-based symbol table storing token identifiers, variable types, function signatures, and lexical scope depths.
   - Implements scope entry/exit mechanisms to track nested lexical blocks.

4. **Automation Script (`run.sh`):**
   - Shell script streamlining the build pipeline: running Flex, compiling the parser with Bison, linking with `g++`/`gcc`, and feeding test source files.

---

## File Structure

```text
├── src/
│   ├── lexer.l          # Lexical rules & token definitions (Flex)
│   ├── parser.y         # Grammar rules & semantic actions (Bison/Yacc)
│   └── symbol_info.h    # Symbol table and scope hierarchy implementation
├── tests/
│   └── input.txt        # Sample input C-subset source program
├── scripts/
│   └── run.sh           # Build and execution automation script
└── README.md
