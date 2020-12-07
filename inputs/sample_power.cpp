// Include the headers
#include "blocks/c_code_generator.h"
#include "builder/builder.h"
#include "builder/builder_context.h"
#include "builder/static_var.h"
#include <iostream>

// Include the BuildIt types
using builder::dyn_var;
using builder::static_var;


// The power function to stage
dyn_var<int> power(dyn_var<int> base, static_var<int> exponent) {
    dyn_var<int> res = 1, x = base;
    while (exponent > 1) {
        if (exponent % 2 == 1)
            res = res * x;
        x = x * x;
        exponent = exponent / 2;
    }
    return res * x;
}

// The main driver function 
int main(int argc, char* argv[]) {
    // Declare the context object
    builder::builder_context context;
    
    // Generate the AST for the next stage
    // The exponent can also be a command line argument, we will supply a constant for simplicity
    int exponent = 15;
    auto ast = context.extract_function_ast(power, "power_15", exponent);
    
    // Generate the headers for the next stage
    std::cout << "#include <stdio.h>" << std::endl;
    block::c_code_generator::generate_code(ast, std::cout, 0);
    
    
    // Print the main function for the next stage manually
    // Can also be generated using BuildIt, but we will skip for simplicity
    std::cout << "int main(int argc, char* argv[]) {printf(\"2 ^ 15 = %d\\n\", power_15(2)); return 0;}" << std::endl;
    
    return 0;
}
