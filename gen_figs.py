import os
import subprocess
import sys
import time

DIR_PATH=os.path.dirname(os.path.realpath(__file__)).rstrip("/")



def get_command_output(command):
	start = time.time()
	output = ""
	if isinstance(command, list):
		proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	else:
		proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	exitcode = proc.wait()
	if exitcode != 0:
		print(command)
	assert(exitcode == 0)
	for line in proc.stdout.readlines():
		if isinstance(line, bytes):
			line = line.decode()
		output += line.rstrip() + "\n"
	proc.stdout.close()
	end = time.time()

	return (output, end-start)


def compile_buildit_program(infile, outfile):
	compile_command = "c++ -I " + DIR_PATH+"/buildit/include -O3 -L " + DIR_PATH + "/buildit/build -rdynamic " + DIR_PATH + "/inputs/" + infile + " -o " + DIR_PATH + "/outputs/" + outfile + " -lbuildit"
	get_command_output(compile_command)

def print_cell(f, val, w = 1):
	total_spaces = 12 * w
	spaces = total_spaces - len(str(val)) - 2
	f.write(" " * spaces + str(val) + " |")

def gen_fig17(res_mem, res_nomem):
	width = 12 * 5 + 1
		
	filepath = DIR_PATH + "/outputs/fig17.txt"
	
	f = open(filepath, "w")
	
	f.write("-" * width)
	f.write("\n")
	
	f.write("|")
	print_cell(f, "iter")	
	print_cell(f, "with_memz", 2)
	print_cell(f, "without_memz", 2)
	f.write("\n")
	
	f.write("-" * width)
	f.write("\n")

	f.write("|")
	print_cell(f, "")	
	print_cell(f, "count")
	print_cell(f, "time(sec)")
	print_cell(f, "count")
	print_cell(f, "time(sec)")	
	f.write("\n")
	
	f.write("-" * width)
	f.write("\n")

	for i in range(16):
		f.write("|")	
		print_cell(f, str(i+1))
		print_cell(f, res_mem[i][0].strip())
		print_cell(f, "%.2f" % res_mem[i][1])
		print_cell(f, res_nomem[i][0].strip())
		print_cell(f, "%.2f" % res_nomem[i][1])
		f.write("\n")

	f.write("-" * width)
	f.write("\n")

	f.close()
		
	print(open(filepath, "r").read())
	print("# This table is generated at: ", filepath)

def run_fig17():
	print("Running evaluation for Figure 17")	
	compile_buildit_program("fig17.cpp", "fig17")
	
	print("Running with Memoization enabled")
	res_mem = [0] * 16
	for i in range(16):
		res_mem[i] = get_command_output(DIR_PATH + "/outputs/fig17 " + str(i+1))

	print("Running with Memoization disabled")
	res_nomem = [0] * 16
	for i in range(16):
		res_nomem[i] = get_command_output(DIR_PATH + "/outputs/fig17 " + str(i+1) + " no_memoize")
	
	gen_fig17(res_mem, res_nomem)	
	


def run_fig24():
	print("Running evaluation for Figure 24")
	compile_buildit_program("fig24.cpp", "fig24")
	
	inputs = [("\"+[+[+[-]]]\"", False), ("\"++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.\"", True), (open(DIR_PATH + "/inputs/mandel.bf").read().strip(), False)]
	for counter, (program, to_run) in enumerate(inputs):
		print("-" * 20)
		print("Running for input ", str(counter+1))
		filepath = DIR_PATH + "/outputs/fig24_ex" + str(counter+1) + ".cpp"
		output, _ = get_command_output(DIR_PATH + "/outputs/fig24 " + program + " > " + filepath)
		#f = open(filepath, "w")
		#f.write(output)
		#f.close()

		print("Output written to ", filepath)
		get_command_output("c++ -O3 " + filepath + " -o " + DIR_PATH + "/outputs/fig24_ex" + str(counter+1))
	
		if to_run:
			print("Now running generated file: ")
			output, _ = get_command_output(DIR_PATH + "/outputs/fig24_ex" + str(counter+1))

			print(output.rstrip())
	

def main():
	print("Starting artifact evaluation in directory: ", DIR_PATH)
	
	OUTPUT_PATH = DIR_PATH + "/outputs"		
	if os.path.exists(OUTPUT_PATH):
		os.system("rm -rf " + OUTPUT_PATH)
	os.makedirs(OUTPUT_PATH)


	run_fig17()
	run_fig24()



if __name__ == "__main__":
	main()	
