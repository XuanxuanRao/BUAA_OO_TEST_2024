import subprocess
import re as regex
import time
import os
import calc
from sympy import *

'''
    [ run the evaluation machine according to the following steps ]
    1.  If you hava already packaged the code into a JAR file, modify [jarName] to the name of JAR file and modify [need_to_pack] to false.
        Else place the folder containing your source code in the current directory, Modify [codeSrcDirectory] to the name of your source code folder and
        modify [MainClass] to the name of your main class
        
    2.  Modify [inputFile] to the name of your input file that stores test data
    
    3.  If you only want to see evaluation information about errors, set [outputMode] to 1 (Optional)
'''

# here are some variables that you need to modify based on your code
# true: you have already packaged the code into a JAR file; false: you place src file in the current directory
need_to_pack = true
# the folder containing your source code
codeSrcDirectory = 'src'
# the name of your main class
MainClassName = 'Main'
# the name of your input file that stores test data
inputFile = 'in.txt'
# 1: only show the evaluation information about errors; 0: show the evaluation information about all
outputMode = 0
# the name of your JAR file
jarName = 'main.jar'



program_run_time = 0.0
count = 0


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


def is_valid_val(a, b) -> bool:
    if Max(a, b) == 0:
        return Abs(a - b) < 0.01
    else:
        return Abs(a - b) / Abs(Max(a, b)) < 0.0001


def check(standard: str, functions: list, output: str) -> (bool, str):
    """
    if outputExpr has (), return WRONG_FORMAT;
    if outputExpr is not equal to inputExpr, return WRONG_VAL; otherwise, return AC(correct answer)
    """
    expr = regex.sub(r'\^', r'**', regex.sub(r'\b0+(\d+)', r'\1', standard).replace("dx", "diff"))
    standard_expr = calc.calc(expr, [regex.sub(r'\^', r'**', function) for function in functions])
    output_expr = simplify(output)
    return output_expr.equals(standard_expr), standard_expr


if __name__ == "__main__":
    correct = true
    if need_to_pack == true:
        create_jar()
    with open(inputFile, 'r') as infile, open('out.txt', 'w') as outfile, open('judge_result.txt', 'w') as judge_file:
        while True:
            n_str = infile.readline().strip()
            if not n_str:
                break
            n = int(n_str)
            count += 1
            functions = []
            for _ in range(n):
                functions.append(infile.readline().strip())
            standard = infile.readline().strip()
            start_time = time.perf_counter()
            process = subprocess.Popen(['java', '-jar', jarName],
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
            input_str = str(n) + '\n'
            for func in functions:
                input_str += func + '\n'
            input_str += standard + '\n'
            process.stdin.write(input_str)
            process.stdin.flush()
            output_str = process.stdout.readline().strip()
            process.stdin.close()
            process.stdout.close()
            process.wait()
            end_time = time.perf_counter()
            run_time = end_time - start_time
            # 写入输出结果
            outfile.write(output_str + '\n')
            judge_file.write(str(run_time) + '\n')
            program_run_time += run_time
            res, standard_expr = check(standard, functions, output_str)
            if res == true and outputMode == 0:
                print("pass test " + str(count))
            elif res == false:
                correct = false
                print("fail test " + str(count))
                print("input: " + str(standard))
                print("output: " + str(output_str))
                print("expected: " + regex.sub(r'\*\*', '^', regex.sub(r'\*\*', '^', str(standard_expr))))
    if correct == true:
        print("All tests passed!")
        print("Average running time: " + str(program_run_time / count))
