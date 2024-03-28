import math

class Request:
    def __init__(self, person_id: int, elevator_id: int, from_floor: int, to_floor: int, timestamp: float):
        self.person_id = person_id
        self.elevator_id = elevator_id
        self.from_floor = from_floor
        self.to_floor = to_floor
        self.timestamp = timestamp
        self.cur_floor = -1

    def move(self, floor: int) -> bool:
        if math.fabs(floor - self.cur_floor) == 1:
            self.cur_floor = floor
            return True
        else:
            return False

    def get_off(self) -> bool:
        if self.cur_floor == self.to_floor and self.cur_floor != -1:
            self.cur_floor = -1
            return True
        else:
            return False

    def get_on(self, floor) -> bool:
        if self.from_floor == floor and self.cur_floor == -1:
            self.cur_floor = floor
            return True
        else:
            return False

    def __str__(self):
        return f'[{self.timestamp}]{self.person_id}-FROM-{self.from_floor}-TO-{self.to_floor}-BY-{self.elevator_id}'