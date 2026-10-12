#include <iostream>
#include <string>

using namespace std;

// Use a SymbolInfo pointer to pass information from lexical analyzer to parser 

class symbol_info
{
private:
    string sym_name;
    string sym_type;

public:

    symbol_info(string name, string type)
    {
        sym_name = name;
        sym_type = type;
    }

    string getname()
    {
        return sym_name;
    }

    string gettype()
    {
        return sym_type;
    }

};
