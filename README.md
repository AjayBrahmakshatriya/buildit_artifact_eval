# BuildIt artifact evaluation

## Introduction
This repository is the guide for evaluating our CGO2021 paper, "BuildIt: A type based multistage programming framework for code generation in C++". This guide has steps for cloning, compiling and executing the implementation of the library.

The  guide has two parts - 
 - Part 1: Reproducing the results in Figure 17 that show that enabling the memoization optimization reduces the execution time from exponential to polynomial. 
 - Part 2: Reproducing the results in Figure 24 to demonstrate that BuildIt can extract C code from a Brain Fuck interpreter essentially producing a Brain Fuck compiler

## Requirements
We expect you to run the artifact evaluation on a Linux/Unix system with atleast 100 MBs of space. Following are the software requirements for both the parts of the evaluations - 

 - make
 - CXX compiler (line g++ >= 5.4.0)
 - python3 
 - bash
 - git

## How to run

### Cloning
We will start by cloning this repository on the evaluation system using the following command - 

    git clone --recursive https://github.com/AjayBrahmakshatriya/buildit_artifact_eval.git

If you have already cloned this repository without the `--recursive` flag, you can get the submodules by running the following commands. Otherwise you can directly proceed to Building BuildIt. 
  
    git submodule init
    git submodule update

### Building BuildIt
Start by navigating to the `buildit_artifact_eval` directory. We will first build the BuildIt library by running the following commands from the repo's top level directory - 

    cd buildit
    make -j$(nproc)

If no errors are reported, the BuildIt library and all the sample/test cases are built correctly. 

If you are running on MacOS and get some errors about missing headers, it might be because your xcode installation is broken after the Catalina upgrade. This is a known issue with MacOS that has got nothing to do with BuildIt. A possible fix for this is - https://stackoverflow.com/questions/58278260/cant-compile-a-c-program-on-a-mac-after-upgrading-to-catalina-10-15/58349403#58349403

If all goes well, you can quickly run the test cases to make sure BuildIt is running properly on your system using the command - 
 
    make run

This command should run the test cases and print a bunch of "OK"s. If some test case fails, the system will print the name of the failing test case. 
If all test cases succeed you can proceed to "Running the evaluation"

### Running the evaluation
First, navigate to the repo's top level directory by running  the command `cd ../`. We will now run a command that generates the table in Figure 17 of the paper and the code snippets in Figure 24 of the paper (and a few more examples). Run the command - 

    python gen_figs.py

If everything goes correctly, the command should run in less than a few minutes and print the results. 


### Interpreting Part 1 results
For Part 1, the script runs the code in Figure 17 with increasing values for `iter` and with the memoization optimization enabled and then disabled. The input code for this part is in the file `inputs/fig17/cpp`. After this part runs successfully, the script should print a table to the console with 5 columns. 
The first column like in the table in the paper should be increasing number of iters. Unlike the paper we run this for 18 iters instead of 10 to clearly demonstrate the execution time difference. The second column shows the number of `build_context` objects instantiated during the execution with memoization enabled and the third column should show the execution time for the experiment. The values in the second column should be linearly increasing with the `iter` value. 

The fourth and the fifth column similarly show the number of `builder_context` objects instantiated and the execution time with memoization disabled. The values in column four should increase exponentially with `iter` and so should the execution time (almost doubling with one increase in iter). 

This table is also saved in the `outputs/fig17.txt` file for your reference later. 


### Interpreting Part 2 results
Immediately after this the results from Part 2 should be printed. For Part 2 the input code can be found at `inputs/fig24.cpp`. This is Brain Fuck interpreter written in BuildIt. We run the interpreter with 3 inputs. The first input is the simple one shown in the caption of Figure 25 ("+[+[+[-]]]"). The script should run the Brain Fuck interpreter written in BuildIt on this input and save the results in `outputs/fig24_ex1.cpp`. You can open this in your favorite text editor and match it with the code in Figure 25 of the paper. Notice that the variable names would be different. We changed the variable names int he paper for easy readability. You can match the triply nested while loop as expected. 

For the next example, the script runs the interpreter on a Hello World program written in Brain Fuck. The generated code can be found at `outputs/fig24_ex2.cpp`. The script also compiles and runs this example and prints the output. You should see "Hello World!" being printed on the console. 

The final example is a Brain Fuck program that prints a Mandelbrot set (borrowed from https://github.com/brain-lang/brainfuck). The script again compiles the generated code but doesn't execute it to avoid clutter. You can inspect the generated code in `outputs/fig24_ex3.cpp` and the compiled binary at `outputs/fig24_ex3`. You can run this example by running the command - 

    ./outputs/fig24_ex3

and a large Mandelbrot set should be generated on the screen. 

The reason we have included example 3 is to show that BuildIt is able to extract code from *really* large programs. The Brain Fuck program for this input is stored in `inputs/mandel.bf` and has `11597` characters. The generated code in `outputs/fig24_ex3.cpp` should be roughly `11464` lines of code. BuildIt is able to extract this code in matter of few seconds. 

### Writing your own BuildIt programs
This section will describe how you can use the BuildIt library to write your own multi-stage programs. As mentioned in the paper, BuildIt takes a pure library approach and doesn't require a specialized compiler to stage the C++ program. We will start by identifying where the BuildIt headers and library is located. We will need these paths when compiling our programs. If you have followed the exact steps above, the headers should be located at the path - `buildit/include`. You can check this by running the following command from the top level directory of the repository - 

    ls buildit/include
    
You should see three folders - `blocks`, `builder` and `utils`. 

Similarly the library should be built at `buildit/build/libbuildit.a`. You can run the following command to check the same - 

    ls buildit/build/libbuildit.a
    
We can now proceed to writing our own BuildIt program. In this example we will be staging the power funciton which calculates x<sup>y</sup> using repeated squaring. We will bind the exponent in the static stage and bind the base in the generated code. 

Start by creating a new C++ file in your favorite text editor. 

We will first include some basic headers that have the BuildIt types (`dyn_var<T>` and `static_var<T>`) and other helper functions to support code generation. 

```
#include "blocks/c_code_generator.h"
#include "builder/builder.h"
#include "builder/builder_context.h"
#include "builder/static_var.h"
#include <iostream>
```

The BuildIt types are in the `builder` namespace. You can add the following lines for accessing the two new types or use the namespace every time you refer to them - 

```
using builder::dyn_var;
using builder::static_var;
```

We will now write a function to actually compute the power function using repeated squaring. Since we are binding the exponent in the static stage, we will declare it using `static_var<T>` and the base using `dyn_var<T>`. You can add a function definition like this - 

```
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
```

This is exactly how you would write a power function in C++ with repeated squaring other than the templated types for staging. We have copied this exact implementation from the iterative version on [Wikipedia](https://en.wikipedia.org/wiki/Exponentiation_by_squaring). 

We will now write a driver function which will supply the arguments and generate code. In BuildIt, all the extraction of program is done using a `builder::builder_context` object. The main function that we will use is the `builder::builder_context::extract_function_ast`.

This function takes the following arguments - 

1. Function pointer that we want to extract the program from using staging (in our case case `power`). 
2. A C string for the name for the function after extracting. This is used while generating code. 

Following this, the function takes the values for the `static_var` arguments in the function in the order they are declared (skipping over the `dyn_var` arguments). In our case since the power function only takes one `static_var` argument for the exponent, that is all we will supply. The only constraint is that this function needs an `lvalue` so instead of passing a constant we will declare a variable and pass that. 

This function returns a `block::block::Ptr` which is a handle to the generated AST. We can pass this to the `block::c_code_generator::generate_code` function to generate the C code for the next stage.

Adding the rest of the code our main function will look like the following - 

```
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
```

This entire program is also provided as a sample in the `inputs/sample_power.cpp` file for your reference. 

Now we will compile this program with the BuildIt library and headers. Run the following command replacing `filename.cpp` with the path to the cpp that you wrote or just use `inputs/power_sample.cpp`. Please run the command from the top level directory of this repository - 

    c++ -std=c++11 -O3 -rdynamic -I buildit/include -L buildit/build filename.cpp -o power_stage1 -lbuildit
    
This will generate the executable `power_stage1`. Run the program by simply running the command - 

    ./power_stage1
    
This will print the code for the second stage on the console. 

We will now also compile this code and run it. Start by saving the program in a file and compiling it as - 

    ./power_stage1 > power_stage2.c
    gcc -O3 power_stage2.c - power_stage2
    
Compiling the generated code doesn't require BuildIt headers or library because it is a normal C program. Finally run it as - 

    ./power_stage2
    
and the program should print - 

> 2 ^ 15 = 32768

You have successfully written and run your first BuildIt program. 


The `buildit/samples` directory has many more samples that you can read and run (executables at `buildit/build` directory) that exercise the full power of `BuildIt`. 

This concludes the artifact evaluation for BuildIt.
