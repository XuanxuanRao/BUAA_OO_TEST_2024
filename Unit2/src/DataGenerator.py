import random
from Request import Request
from enum import Enum
import numpy as np


class Strategy(Enum):
    FOCUSED = 1
    MIXED = 2


peoples_id = {int}
max_time_bound = 20.0
max_request_number = 10


def generate_focused_timestamps(num_points=50, focus_points=[3.0, 7.0, 10.0], std_dev=1.0):
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


def generate_mixed_timestamps(num_points=50, threshold=10.0, large_points_ratio=0.1):
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
    small_timestamps = list(np.random.uniform(low=0.0, high=threshold, size=num_small_points))
    large_timestamps = list(np.random.uniform(low=threshold, high=50.0, size=num_large_points))
    timestamps = small_timestamps + large_timestamps
    return [round(ts, 1) for ts in timestamps]


def generate_timestamps(number: int, strategy: Strategy):
    if strategy == Strategy.FOCUSED:
        return sorted(generate_focused_timestamps(number))
    elif strategy == Strategy.MIXED:
        return sorted(generate_mixed_timestamps(number))
    else:
        raise ValueError('Invalid strategy!')


def generate_request(timestamp: float) -> Request:
    if random.random() > 0.05:
        people_id = random.randint(1, max_request_number)
    else:
        people_id = random.randint(max_request_number * 100, 0x7fffffff)
    while people_id in peoples_id:
        if random.random() > 0.05:
            people_id = random.randint(1, max_request_number)
        else:
            people_id = random.randint(max_request_number * 100, 0x7fffffff)
    peoples_id.add(people_id)
    elevator_id = random.randint(1, 6)
    from_floor = random.randint(1, 11)
    to_floor = random.randint(1, 11)
    while to_floor == from_floor:
        to_floor = random.randint(1, 11)
    return Request(people_id, elevator_id, from_floor, to_floor, timestamp)


def generate_requests(request_number) -> dict[int, Request]:
    requests = {}
    timestamps = generate_timestamps(request_number, random.choice([Strategy.MIXED, Strategy.FOCUSED]))
    for i in range(request_number):
        request = generate_request(timestamps[i])
        requests[request.person_id] = request
    return requests
