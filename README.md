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

If no errors are reported, the BuildIt library and all the sample/test cases are built correctly. You can quickly run the test cases to make sure BuildIt is running properly on your system using the command - 
 
    make run

This command should run the test cases and print a bunch of "OK"s. If some test case fails, the system will print the name of the failing test case. 
If all test cases succeed you can proceed to "Running the evaluation"

### Running the evaluation
First, navigate to the repo's top level directory by running  the command `cd ../`. We will now run a command that generates the table in Figure 17 of the paper and the code snippets in Figure 24 of the paper (and a few more examples). Run the command - 

    python gen_figs.py

If everything goes correctly, the command should run in less than a few minutes and print the results. 


### Interpreting Part 1 results
For Part 1, the script runs the code in Figure 17 with increasing values for `iter` and with the memoization optimization enabled and then disabled. The input code for this part is in the file `inputs/fig17/cpp`. After this part runs successfully, the script should print a table to the console with 5 columns. 
The first column like in the table in the paper should be increasing number of iters. Unlike the paper we run this for 16 iters instead of 10 to clearly demonstrate the execution time difference. The second column shows the number of `build_context` objects instantiated during the execution with memoization enabled and the third column should show the execution time for the experiment. The values in the second column should be linearly increasing with the `iter` value. 

The fourth and the fifth column similarly show the number of `builder_context` objects instantiated and the execution time with memoization disabled. The values in column four should increase exponentially with `iter` and so should the execution time (almost doubling with one increase in iter). 

This table is also saved in the `outputs/fig17.txt` file for your reference later. 


### Interpreting Part 2 results
Immediately after this the results from Part 2 should be printed. For Part 2 the input code can be found at `inputs/fig24.cpp`. This is Brain Fuck interpreter written in BuildIt. We run the interpreter with 3 inputs. The first input is the simple one shown in the caption of Figure 25 ("+[+[+[-]]]"). The script should run the Brain Fuck interpreter written in BuildIt on this input and save the results in `outputs/fig24_ex1.cpp`. You can open this in your favorite text editor and match it with the code in Figure 25 of the paper. Notice that the variable names would be different. We changed the variable names int he paper for easy readability. You can match the triply nested while loop as expected. 

For the next example, the script runs the interpreter on a Hello World program written in Brain Fuck. The generated code can be found at `outputs/fig24_ex2.cpp`. The script also compiles and runs this example and prints the output. You should see "Hello World!" being printed on the console. 

The final example is a Brain Fuck program that prints a Mandelbrot set (borrowed from https://github.com/brain-lang/brainfuck). The script again compiles the generated code but doesn't execute it to avoid clutter. You can inspect the generated code in `outputs/fig24_ex3.cpp` and the compiled binary at `outputs/fig24_ex3`. You can run this example by running the command - 

    ./outputs/fig24_ex3

and a large Mandelbrot set should be generated on the screen. 

The reason we have included example 3 is to show that BuildIt is able to extract code from *really* large programs. The Brain Fuck program for this input is stored in `inputs/mandel.bf` and has `11597` characters. The generated code in `outputs/fig24_ex3.cpp` should be roughly `11464` lines of code. BuildIt is able to extract this code in matter of few seconds. 

This concludes the artifact evaluation for BuildIt.
