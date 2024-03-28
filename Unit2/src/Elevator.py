from decimal import Decimal

from Request import Request
import math

open_time = '0.2'
close_time = '0.2'
move_time = '0.4'


class Elevator:
    def __init__(self, id: int, floor=1):
        self.floor = floor
        self.requests = []
        self.is_open = False
        self.capacity = 6
        self.id = id
        self.last_open_time = '0.0'
        self.last_move_time = '0.0'
        self.last_close_time = '0.0'

    def move(self, floor, timestamp: str) -> bool:
        if self.is_open or Decimal(timestamp) - Decimal(self.last_move_time) < Decimal(move_time) or floor <= 0 or floor >= 12 \
            or math.fabs(floor - self.floor) != 1 or Decimal(timestamp) - Decimal(self.last_close_time) < Decimal(move_time):
            return False
        self.floor = floor
        for request in self.requests:
            if not request.move(floor):
                return False
        self.last_move_time = timestamp
        return True

    def get_on(self, request: Request) -> bool:
        if not self.is_open or len(self.requests) >= self.capacity:
            return False
        if request.get_on(self.floor):
            self.requests.append(request)
            return True
        else:
            return False

    def get_off(self, request: Request) -> bool:
        if not self.is_open:
            return False
        if request.get_off():
            self.requests.remove(request)
            return True
        else:
            return False

    def open(self, timestamp: str) -> bool:
        if self.is_open:
            return False
        else:
            self.is_open = True
            self.last_open_time = timestamp
            return True

    def close(self, timestamp: str) -> bool:
        if self.is_open and Decimal(timestamp) - Decimal(self.last_open_time) >= Decimal(open_time) + Decimal(close_time):
            self.is_open = False
            self.last_close_time = timestamp
            return True
        else:
            return False
