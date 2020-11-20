#include "blocks/c_code_generator.h"
#include "builder/builder.h"
#include "builder/builder_context.h"
#include "builder/static_var.h"
#include <iostream>
#include <cstring>

using builder::dyn_var;
using builder::static_var;

// Function with unrolled branches
static void foo(int iter) {
	dyn_var<int> a;
	for (static_var<int> i = 0; i < iter; i++) {
		if (a) {
			a = a + i;
		} else {
			a = a - i;
		}
	}
}
int main(int argc, char *argv[]) {
	if (argc < 2) {
		printf("Usage: %s <iters> [no_memoize]\n", argv[0]);
		return -1;
	}	

	int iter = 1;
	if (sscanf(argv[1], "%d", &iter) != 1) {
		printf("Invalid value for iters, please supply an integer\n");
		return -1;
	}


	builder::builder_context context;

	if (argc > 2 && strcmp(argv[2], "no_memoize") == 0) 
		context.use_memoization = false;

	auto ast = context.extract_function_ast(foo, "power", iter);
	

	// For the artifact evaluation we will not dump the AST and the code
	// Uncomment the lines below if you want to see the generated code

	// ast->dump(std::cout, 0);
	// block::c_code_generator::generate_code(ast, std::cout, 0);


	std::cout << builder::builder_context::debug_creation_counter << std::endl;
	return 0;
}
