import random
from Request import Request
from enum import Enum
import numpy as np


class TimestampStrategy(Enum):
    FOCUSED = 1
    MIXED = 2


class ElevatorIdStrategy(Enum):
    RANDOM = 1
    FULL_ATTACK = 2



peoples_id = {int}
max_time_bound = 30.0
max_request_number = 100
requests_elevator = [[] for _ in range(6)]
elevator_capacity = 6


def generate_focused_timestamps(num_points, focus_points, std_dev=1.0):
    """
    生成集中在几个点附近的时间戳。

    Parameters:
    - num_points: 要生成的时间戳数量。
    - focus_points: 集中分布的中心点列表。
    - std_dev: 每个中心点的标准差，决定了分布的宽度。

    Returns:
    - 一个时间戳列表。
    """
    timestamps = []
    points_per_focus = num_points // len(focus_points)
    for point in focus_points:
        timestamps += list(np.random.normal(loc=point, scale=std_dev, size=points_per_focus))
    if len(timestamps) < num_points:
        extra_points = num_points - len(timestamps)
        timestamps += list(np.random.normal(loc=focus_points[-1], scale=std_dev, size=extra_points))
    return [round(ts, 1) for ts in timestamps]


def generate_mixed_timestamps(num_points: int, threshold, large_points_ratio=0.1):
    """
    生成大部分时间戳均匀分布在较小范围内，少数几个大值分布的时间戳。

    Parameters:
    - num_points: 要生成的时间戳数量。
    - threshold: 分割大值和小值的阈值。
    - large_points_ratio: 大值时间戳占总时间戳的比例。

    Returns:
    - 一个时间戳列表。
    """
    num_large_points = int(num_points * large_points_ratio)
    num_small_points = num_points - num_large_points
    small_timestamps = list(np.random.uniform(low=1.0, high=threshold, size=num_small_points))
    large_timestamps = list(np.random.uniform(low=threshold, high=max_time_bound, size=num_large_points))
    timestamps = small_timestamps + large_timestamps
    return [round(ts, 1) for ts in timestamps]


def generate_timestamps(number: int, timestamp_strategy: TimestampStrategy):
    if timestamp_strategy == TimestampStrategy.FOCUSED:
        focused_point = [random.uniform(1.5, 13.0) for _ in range(3)]
        return sorted(generate_focused_timestamps(number, focused_point))
    elif timestamp_strategy == TimestampStrategy.MIXED:
        return sorted(generate_mixed_timestamps(number, random.choice([6.5, 8.75, 11.5, 14.0])))
    else:
        raise ValueError('Invalid strategy!')


def generate_request(timestamp: float) -> Request:
    people_id = generate_people_id()
    while people_id in peoples_id:
        people_id = generate_people_id()
    peoples_id.add(people_id)
    elevator_id = (generate_elevator_id(random.choice([ElevatorIdStrategy.RANDOM, ElevatorIdStrategy.FULL_ATTACK]),
                                        timestamp))
    from_floor = random.randint(1, 11)
    to_floor = random.randint(1, 11)
    while to_floor == from_floor:
        to_floor = random.randint(1, 11)
    return Request(people_id, elevator_id, from_floor, to_floor, timestamp)


def generate_people_id():
    if random.random() < 0.95:
        people_id = random.randint(1, max_request_number)
    else:
        people_id = random.randint(max_request_number * 100, 0x7fffffff)
    return people_id


def generate_elevator_id(elevator_id_strategy: ElevatorIdStrategy, now_timestamp: float):
    if elevator_id_strategy == ElevatorIdStrategy.RANDOM:
        return random.randint(1, 6)
    elif elevator_id_strategy == ElevatorIdStrategy.FULL_ATTACK:
        candidate_elevators = random.sample(range(1, 7), 3)
        for candidate_elevator in candidate_elevators:
            if candidate_elevator not in requests_elevator:
                continue
            elif len(requests_elevator[candidate_elevator]) + 2 >= elevator_capacity:
                requests_elevator[candidate_elevator] = \
                    [request for request in requests_elevator[candidate_elevator] if now_timestamp - request.timestamp <= 7.0]
                return candidate_elevator
        return random.choice(candidate_elevators)


def generate_requests(request_number) -> dict[int, Request]:
    requests = {}
    timestamps = generate_timestamps(request_number, random.choice([TimestampStrategy.MIXED, TimestampStrategy.FOCUSED]))
    for i in range(request_number):
        request = generate_request(timestamps[i])
        requests[request.person_id] = request
        requests_elevator[request.elevator_id-1].append(request)
    peoples_id.clear()
    for i in range(6):
        requests_elevator[i].clear()
    return requests
