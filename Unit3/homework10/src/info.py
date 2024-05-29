import os


def get_jar_info():
    jar_list = []
    with open("jar.txt", "r") as f:
        for line in f.readlines():
            jar_list.extend(line.split())
    if not all(ele.endswith('.jar') for ele in jar_list):
        print("invalid jar name")
        return None
    else:
        for jar in jar_list:
            if not os.path.exists(jar):
                print(f"{jar} not found")
                return None
        return jar_list
