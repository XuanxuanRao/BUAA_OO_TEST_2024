import re
import os
import DataGenerator
from Request import Request
from Elevator import Elevator
from enum import Enum


class RESULT(Enum):
    VALID_OUTPUT = 0,
    INVALID_CLOSE = 1,
    INVALID_OPEN = 2,
    INVALID_MOVE = 3,
    INVALID_GET_ON = 4,
    INVALID_GET_OFF = 5,
    REQUEST_NOT_ASSIGN = 6
    REQUEST_NOT_FINISH = 7
    DOOR_NOT_CLOSE = 8


def parse_request(input_str: str) -> Request:
    pattern = r'\[(\d+\.\d+)\](\d+)-FROM-(\d+)-TO-(\d+)-BY-(\d+)'
    match = re.match(pattern, input_str)
    # 如果匹配成功，则提取各个部分
    if match:
        timestamp, person_id, from_floor, to_floor, elevator_id = map(float, match.groups())
        return Request(int(person_id), int(elevator_id), int(from_floor), int(to_floor), timestamp)
    else:
        raise ValueError("输入格式不正确")


def read_requests(input_file: str) -> dict:
    requests_dict = {}
    with open(input_file, 'r') as f:
        for line in f:
            request = parse_request(line.strip())
            requests_dict[request.person_id] = request
    return requests_dict


def read_commands(output_file: str) -> list[str]:
    with open(output_file, 'r') as f:
        return [line.strip() for line in f.readlines()]


def parse_command(command_str, requests: dict, elevators: list[Elevator]):
    pattern1 = r'\[(\s*\d+\.\d+)\](ARRIVE|OPEN|CLOSE)-(\d+)-(\d+)'
    pattern2 = r'\[(\s*\d+\.\d+)\](IN|OUT)-(\d+)-(\d+)-(\d+)'
    match1 = re.match(pattern1, command_str)
    match2 = re.match(pattern2, command_str)
    if match1:
        timestamp, action, floor, elevator_id = match1.groups()
        if action == 'ARRIVE':
            if elevators[int(elevator_id)-1].move(int(floor), timestamp):
                return RESULT.VALID_OUTPUT
            else:
                return RESULT.INVALID_MOVE
        elif action == 'OPEN':
            if elevators[int(elevator_id)-1].open(timestamp):
                return RESULT.VALID_OUTPUT
            else:
                return RESULT.INVALID_OPEN
        elif action == 'CLOSE':
            if elevators[int(elevator_id)-1].close(timestamp):
                return RESULT.VALID_OUTPUT
            else:
                return RESULT.INVALID_CLOSE
    if match2:
        timestamp, action, person_id, floor, elevator_id = match2.groups()
        if action == 'IN':
            request = requests[int(person_id)]
            if elevators[int(elevator_id)-1].get_on(request):
                return RESULT.VALID_OUTPUT
            else:
                return RESULT.INVALID_GET_ON
        elif action == 'OUT':
            request = requests[int(person_id)]
            if elevators[int(elevator_id)-1].get_off(request):
                requests.pop(int(person_id))
                return RESULT.VALID_OUTPUT
            else:
                return RESULT.INVALID_GET_OFF
    else:
        print("无法识别的指令格式")


if __name__ == '__main__':
    test_case_number = int(input("Please input the number of test cases: "))
    request_number = int(input("Please input the number of requests in each test case: "))
    os.makedirs('test_cases', exist_ok=True)
    for cnt in range(test_case_number):
        input_file_name = 'in' + str(cnt + 1) + '.txt'
        out_file_name = 'out' + str(cnt + 1) + '.txt'
        requests = DataGenerator.generate_requests(request_number)
        with open('test_cases\\' + input_file_name, 'w') as file:
            file.writelines(f'{request}\n' for request in requests.values())
        os.system('type ' + 'test_cases\\' + input_file_name + ' > stdin.txt')
        print('Running test case ' + str(cnt + 1) + '...')
        os.system('.\datainput_student_win64.exe | java -jar code.jar >' + 'test_cases\\' + out_file_name)
        commands = read_commands('test_cases\\' + out_file_name)
        elevators = [Elevator(i+1) for i in range(6)]
        res = RESULT.VALID_OUTPUT
        run_time = 0.0
        for command in commands:
            res = parse_command(command, requests, elevators)
            run_time = command.split('[')[1].split(']')[0]
            if res != RESULT.VALID_OUTPUT:
                break
        if res == RESULT.VALID_OUTPUT:
            if not all([len(e.requests) == 0 for e in elevators]):
                res = RESULT.REQUEST_NOT_FINISH
            elif not all(not e.is_open for e in elevators):
                res = RESULT.DOOR_NOT_CLOSE
            elif len(requests) > 0:
                res = RESULT.REQUEST_NOT_ASSIGN
        if res == RESULT.VALID_OUTPUT:
            print("Valid output, run time: " + run_time + "s")
        else:
            print(res.name)
    os.remove('stdin.txt')
    input('Press Enter to exit')
