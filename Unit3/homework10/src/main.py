import os
import shutil
import info
import data
import run
import sys
import time
import hashlib


def check(key: int, decode_info) -> bool:
    current_time = int(time.time()) // 1800 * 1800
    message_to_encrypt = str(current_time) + str(key)
    ciphertext = hashlib.sha256(message_to_encrypt.encode()).hexdigest()
    return ciphertext == decode_info


def save(test_id: int):
    bug_log_prefix = "bug_log_"
    max_number = 0

    for item in os.listdir('record'):
        if item.startswith(bug_log_prefix) and os.path.isdir(os.path.join('record', item)):
            try:
                number = int(item[len(bug_log_prefix):])
                max_number = max(max_number, number)
            except ValueError:
                continue

    new_folder_name = f"{bug_log_prefix}{max_number + 1}"
    new_folder_path = os.path.join('record', new_folder_name)

    os.makedirs(new_folder_path, exist_ok=True)
    # diff.txt
    for item in os.listdir('record'):
        if item.endswith(".txt") and os.path.isfile(os.path.join('record', item)):
            new_file_name = item.replace(f"out{test_id}_", "diff_")
            shutil.move(os.path.join('record', item), os.path.join(new_folder_path, new_file_name))
    # in.txt
    shutil.copy(os.path.join('in', f"in{test_id}.txt"), os.path.join(new_folder_path, "in.txt"))
    # out.txt
    for item in os.listdir('out'):
        if item.startswith(f"out{test_id}_") and item.endswith(".txt") and os.path.isfile(os.path.join('out', item)):
            base_name = item.replace(f"out{test_id}_", "").replace(".txt", "")
            shutil.copy(os.path.join('out', item), os.path.join(new_folder_path, f"out_{base_name}.txt"))


if __name__ == '__main__':
    # if not check(0x1BDB94D699A3E76732CF02FE57E9D1D3, sys.argv[1]):
    #     print("Invalid key")
    #     time.sleep(3)
    #     sys.exit(-1)
    jar_list = info.get_jar_info()
    if os.path.exists('in'):
        shutil.rmtree('in')
    if os.path.exists('out'):
        shutil.rmtree('out')
    os.makedirs('in', exist_ok=True)
    os.makedirs('out', exist_ok=True)
    os.makedirs('record', exist_ok=True)
    if jar_list is None:
        time.sleep(3)
        sys.exit(-1)
    print("Testing...")
    correct = True
    for i in range(1, 11):
        data.generate(3000, i)
        if not run.run(jar_list, i):
            correct = False
            save(i)
    if correct:
        print("All tests passed")
    else:
        print("Some tests failed")
    input("Press Enter to exit\n")
