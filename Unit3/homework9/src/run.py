import subprocess
from datetime import datetime


def diff(out1, out2) -> int:
    with open('out\\' + out1, 'r') as file1, open('out\\' + out2, 'r') as file2:
        for line_num, (line1, line2) in enumerate(zip(file1, file2), 1):
            line1 = line1.strip()
            line2 = line2.strip()
            if line1 != line2:
                s = out2[out2.find('_') + 1:-4]
                with open(f'record\\{out1[:-4]}_{s}.txt', 'w') as record_file:
                    record_file.write(f"{out1}, line {line_num}: {line1}\n")
                    record_file.write(f"{out2}, line {line_num}: {line2}\n")
                return line_num
        else:
            if len(list(file1)) != len(list(file2)):
                s = out2[out2.find('_') + 1:-4]
                with open(f'record\\{out1[:-4]}_{s}.txt', 'w') as record_file:
                    record_file.write(f'Output lengths differ, {out1}: {len(list(file1))}, {out2}: {len(list(file2))}')
                    return min(len(list(file1)), len(list(file2)))
            else:
                return -1


def run(jar_list: list[str], test_id: int) -> bool:
    correct = True

    input_file = 'in\\in' + str(test_id) + '.txt'

    for jar_name in jar_list:
        output_file = 'out\\out' + str(test_id) + '_' + jar_name[:-4] + '.txt'
        process = subprocess.Popen(
            ['run_code.bat', input_file, jar_name, output_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True)
        stdout, stderr = process.communicate()
        time_info = stdout.splitlines()
        start_time = time_info[-4]
        end_time = time_info[-1]
        time_format = "%H:%M:%S.%f"
        start_time = datetime.strptime(start_time.strip(), time_format)
        end_time = datetime.strptime(end_time.strip(), time_format)
        run_time = (end_time - start_time).total_seconds()
        if run_time >= 2.00:
            print(f"\033[93m#testcase{test_id}, {jar_name} may exceed time limit: {run_time} seconds\033[0m")
    for i in range(len(jar_list)):
        for j in range(i + 1, len(jar_list)):
            cmp_result = diff('out' + str(test_id) + '_' + jar_list[i][:-4] + '.txt',
                              'out' + str(test_id) + '_' + jar_list[j][:-4] + '.txt')
            if cmp_result != -1:
                print(f"\033[91m#testcase{test_id}, {jar_list[i]} and {jar_list[j]} are different in line {cmp_result}\033[0m")
                correct = False

    return correct
