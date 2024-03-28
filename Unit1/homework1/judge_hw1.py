import subprocess
import re as regex
import time
import os

from sympy import *

'''
    [ run the evaluation machine according to the following steps ] 
    1.  Place the folder containing your source code in the current directory
    2.  Modify [codeSrcDirectory] to the name of your source code folder
    3.  Modify [MainClass] to the name of your main class
    4.  Modify [inputFile] to the name of your input file that stores test data
    5.  If you only want to see evaluation information about errors, set [outputMode] to 1 (Optional)
'''

# here are some variables that you need to modify based on your code

# the folder containing your source code
codeSrcDirectory = 'src'
# the name of your main class
MainClassName = 'Main'
# the name of your input file that stores test data
inputFile = 'TestData.txt'
# 1: only show the evaluation information about errors; 0: show the evaluation information about all
outputMode = 0

program_run_time = 0.0
values = [-999, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100]
count = 0
judge_result = ['AC', 'WRONG_FORMAT', 'WRONG_VAL', 'UNSIMPLIFIED']
AC = 0
WRONG_FORMAT = 1
WRONG_VAL = 2
UNSIMPLIFIED = 3


def create_jar():
    meta_inf_path = os.path.join(codeSrcDirectory, 'META-INF')
    os.makedirs(meta_inf_path, exist_ok=True)
    manifest_path = os.path.join(meta_inf_path, 'MANIFEST.MF')
    with open(manifest_path, 'w') as f:
        f.write('Manifest-Version: 1.0\n')
        f.write('Main-Class: ' + MainClassName + '\n')
    process = subprocess.Popen(['javac', '-encoding', 'UTF-8', codeSrcDirectory + '\\*.java'],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    process.stdout.readline().strip()
    process.wait()
    process = subprocess.Popen(['javac', codeSrcDirectory + '\\*.java'],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    process.stdout.readline().strip()
    process.wait()
    process = subprocess.Popen(
        ['jar', '-cvfm', 'main.jar', codeSrcDirectory + '\\META-INF\\MANIFEST.MF', '-C', codeSrcDirectory, '.'],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    process.stdout.readline().strip()
    process.wait()


def check(standard: str, output: str) -> int:
    """if outputExpr has (), return WRONG_FORMAT; if outputExpr can still be simplified, return UNSIMPLIFIED;
    if outputExpr is not equal to inputExpr, return WRONG_VAL; otherwise, return AC(correct answer)"""
    standard_expr = sympify(regex.sub(r'\b0+(\d+)', r'\1', standard))
    output_expr = sympify(output)
    format_valid = not ('(' in output or ')' in output)
    val_valid = true
    simplified = len(expand(output_expr).args) == len(output_expr.args)
    for val in values:
        if output_expr.subs(Symbol('x'), val) != standard_expr.subs(Symbol('x'), val):
            val_valid = false
            break
    if format_valid == false:
        return WRONG_FORMAT
    elif val_valid == false:
        return WRONG_VAL
    elif simplified == false:
        return UNSIMPLIFIED
    else:
        return AC


if __name__ == "__main__":
    correct = true
    create_jar()
    with open(inputFile, 'r') as infile, open('out.txt', 'w') as outfile, open('judge_result.txt', 'w') as judge_file:
        for standard in infile:
            count += 1
            start_time = time.perf_counter()
            process = subprocess.Popen(['java', '-jar', 'main.jar'],
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
            input_str = standard + '\n'
            process.stdin.write(input_str)
            process.stdin.flush()
            output_str = process.stdout.readline().strip()
            process.stdin.close()
            process.stdout.close()
            process.wait()
            end_time = time.perf_counter()
            run_time = end_time - start_time
            outfile.write(output_str + '\n')
            judge_file.write(str(run_time) + '\n')
            program_run_time += run_time
            res = check(input_str, output_str)
            if res == AC and outputMode == 0:
                print("pass test " + str(count))
            elif res != AC:
                correct = false
                print("fail test {0} for {1}".format(str(count), judge_result[res]))
                print("input: " + str(standard), end="")
                print("expected [ {0} ], but got [ {1} ]".format(output_str[:-2],
                                                             expand(sympify(regex.sub(r'\b0+(\d+)', r'\1', standard)))))
    if correct == true:
        print("All tests passed!")
        print("Average running time: " + str(program_run_time / count))
