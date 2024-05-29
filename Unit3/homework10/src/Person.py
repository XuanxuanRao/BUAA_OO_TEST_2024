import random


class Person:
    def __init__(self, m_id: int):
        self.id = m_id
        self.acquaintances = set()
        self.tags = {}

    def add_acquaintance(self, person_id: int) -> None:
        self.acquaintances.add(person_id)

    def remove_acquaintance(self, person_id: int) -> None:
        if person_id in self.acquaintances:
            self.acquaintances.remove(person_id)

    def add_tag(self, tag_id: int) -> None:
        if tag_id not in self.tags:
            self.tags[tag_id] = set()

    def remove_tag(self, tag_id: int) -> None:
        if tag_id in self.tags:
            self.tags.pop(tag_id)

    def add_person_to_tag(self, tag_id: int, person_id: int) -> None:
        if tag_id in self.tags:
            self.tags[tag_id].add(person_id)

    def remove_person_from_tag(self, tag_id: int, person_id: int) -> None:
        if tag_id in self.tags:
            self.tags[tag_id].remove(person_id)

    def has_tag(self, tag_id: int) -> bool:
        return tag_id in self.tags

    def has_acquaintance(self, person_id: int) -> bool:
        return person_id in self.acquaintances

    def get_a_tag(self) -> int:
        if len(self.tags) == 0:
            return 0x7fffffff
        return random.choice(list(self.tags.keys()))

    def get_an_acquaintance(self) -> int:
        if len(self.acquaintances) == 0:
            return 0x7fffffff
        return random.choice(list(self.acquaintances))

    def get_a_person_in_tag(self, tag_id=0x7fffffff) -> int:
        if tag_id != 0x7fffffff:
            if tag_id not in self.tags or len(self.tags[tag_id]) == 0:
                return 0x7fffffff
            else:
                return random.choice(list(self.tags[tag_id]))
        else:
            if len(self.tags) == 0:
                return 0x7fffffff
            chance = 5
            tag_id = random.choice(list(self.tags.keys()))
            while chance > 0 and len(self.tags[tag_id]) == 0:
                tag_id = random.choice(list(self.tags.keys()))
                chance -= 1
            return 0x7fffffff if len(self.tags[tag_id]) == 0 else random.choice(list(self.tags[tag_id]))

    def has_person_in_tag(self, tag_id: int, person_id: int) -> bool:
        return tag_id in self.tags and person_id in self.tags[tag_id]

    def __hash__(self):
        return self.id
