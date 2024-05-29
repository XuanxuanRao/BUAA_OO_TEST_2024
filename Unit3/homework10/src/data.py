import random
import numpy as np

from Person import Person

instructions = ['ap', 'ar', 'mr', 'qv', 'qci', 'qbs', 'qts', 'at', 'dt', 'att', 'dft', 'qtvs', 'qtav', 'qsp', 'qba', 'qcs']
probabilities1 = [0.05, 0.2, 0.1, 0.02, 0.02, 0.02, 0.02, 0.15, 0.02, 0.12, 0.03, 0.05, 0.00, 0.08, 0.02, 0.1]
probabilities2 = [0.05, 0.1, 0.1, 0.02, 0.02, 0.02, 0.02, 0.1, 0.02, 0.17, 0.08, 0.1, 0.00, 0.08, 0.02, 0.1]
persons = {}
name_list = ['Sakura', 'Keruberosu']


def load_network() -> str:
    n = random.randint(50, 100)
    instr = f"ln {n}\n"
    id_list = []
    for i in range(0, n):
        person_id = generate_person_id(1.0) if i > 1 else (0x7fffffff if i == 1 else -1)
        instr += str(person_id) + ' '
        id_list.append(person_id)
        if person_id not in persons:
            persons[person_id] = Person(person_id)
    instr += '\n'
    instr += " ".join(random.choice(name_list) for _ in range(n)) + "\n"
    instr += " ".join(str(random.randint(1, 200)) for _ in range(n)) + "\n"
    for i in range(1, n):
        line = ''
        for j in range(i):
            val = random.randint(0, 4)
            line += str(val) + ' '
            if val > 0:
                persons[id_list[i]].add_acquaintance(id_list[j])
                persons[id_list[j]].add_acquaintance(id_list[i])
        instr += line + '\n'
    return instr


def generate_person_id(new_id_probability: float) -> int:
    if random.random() < new_id_probability or len(persons) == 0:
        person_id = random.randint(-100000, 100000)
        while person_id in persons:
            person_id = random.randint(-100000, 100000)
    else:
        person_id = random.choice(list(persons.keys()))
    return person_id


def generate_tag_id(new_tag_probability: float, owner_id: int) -> int:
    if owner_id not in persons:
        return random.randint(-100000, 100000)
    if random.random() < new_tag_probability or persons[owner_id].get_a_tag() == 0x7fffffff:
        tag_id = random.randint(-100000, 100000)
        while persons[owner_id].has_tag(tag_id):
            tag_id = random.randint(-100000, 100000)
    else:
        tag_id = persons[owner_id].get_a_tag()
    return tag_id


def generate_query_tag_instr(valid_probability: float, instr_kind: str) -> str:
    owner_id = generate_person_id(0.0)
    tag_id = generate_tag_id(1.0 - valid_probability, owner_id)
    return f"{instr_kind} {owner_id} {tag_id}"


def generate_add_person_instr(valid_probability: float) -> str:
    person_id = generate_person_id(valid_probability)
    if person_id not in persons:
        persons[person_id] = Person(person_id)
    return f"ap {person_id} {random.choice(name_list)} {random.randint(1, 200)}"


def generate_add_tag_instr(valid_probability: float) -> str:
    if random.random() < valid_probability:
        owner_id = generate_person_id(0.0)
        tag_id = generate_tag_id(1.0, owner_id)
        persons[owner_id].add_tag(tag_id)
    else:
        owner_id = generate_person_id(0.5)
        tag_id = generate_tag_id(0.5, owner_id)
    return f"at {owner_id} {tag_id}"


def generate_delete_tag_instr(valid_probability: float) -> str:
    if random.random() < valid_probability:
        owner_id = generate_person_id(0.0)
        tag_id = generate_tag_id(0.0, owner_id)
        persons[owner_id].remove_tag(tag_id)
    else:
        owner_id = generate_person_id(0.05)
        tag_id = generate_tag_id(0.5, owner_id)
    return f"dt {owner_id} {tag_id}"


def generate_add_person_to_tag_instr(valid_probability: float) -> str:
    if random.random() < valid_probability:
        owner_id = generate_person_id(0.0)
        tag_id = generate_tag_id(0.0, owner_id)
        person_id = persons[owner_id].get_an_acquaintance()
        if person_id == 0x7fffffff:
            person_id = generate_person_id(0.5)
        else:
            chance = 5
            while chance > 0 and persons[owner_id].has_person_in_tag(tag_id, person_id):
                person_id = persons[owner_id].get_an_acquaintance()
                chance -= 1
            persons[owner_id].add_person_to_tag(tag_id, person_id)
    else:
        person_id = generate_person_id(0.05)
        owner_id = generate_person_id(0.05)
        tag_id = generate_tag_id(0.05, owner_id)
    return f"att {person_id} {owner_id} {tag_id}"


def generate_delete_person_from_tag_instr(valid_probability: float) -> str:
    if random.random() < valid_probability:
        owner_id = generate_person_id(0.0)
        tag_id = generate_tag_id(0.0, owner_id)
        person_id = persons[owner_id].get_a_person_in_tag(tag_id)
        if person_id == 0x7fffffff:
            person_id = generate_person_id(0.5)
        else:
            persons[owner_id].remove_person_from_tag(tag_id, person_id)
    else:
        person_id = generate_person_id(0.05)
        owner_id = generate_person_id(0.05)
        tag_id = generate_tag_id(0.05, owner_id)
    return f"dft {person_id} {owner_id} {tag_id}"


def generate_query_best_instr(valid_probability: float) -> str:
    person_id = generate_person_id(1.0 - valid_probability)
    return f"qba {person_id}"


def generate_query_shortest_path_instr(valid_probability: float) -> str:
    person_id1 = generate_person_id(1.0 - valid_probability)
    person_id2 = generate_person_id(1.0 - valid_probability)
    return f"qsp {person_id1} {person_id2}"


def generate_add_relation_instr(valid_probability: float) -> str:
    def can_add_edge(id1: int, id2: int) -> bool:
        if id1 not in persons or id2 not in persons:
            return False
        return not persons[id1].has_acquaintance(id2) and not persons[id2].has_acquaintance(id1)

    person_id1, person_id2 = generate_person_id(0.05), generate_person_id(0.05)
    chance = int(valid_probability * 5.0) + 1
    while not can_add_edge(person_id1, person_id2) and chance > 0:
        person_id1, person_id2 = generate_person_id(0.05), generate_person_id(0.05)
        chance -= 1
    if person_id1 in persons and person_id2 in persons:
        persons[person_id1].add_acquaintance(person_id2)
        persons[person_id2].add_acquaintance(person_id1)
    return f"ar {person_id1} {person_id2} {random.randint(1, 20)}"


def generate_modify_relation_instr(valid_probability: float, delete_probability: float) -> str:
    def edge_exist(id1: int, id2: int) -> bool:
        if id1 not in persons or id2 not in persons:
            return False
        return persons[id1].has_acquaintance(id2) and persons[id2].has_acquaintance(id1)

    person_id1, person_id2 = generate_person_id(0.05), generate_person_id(0.05)
    if random.random() < 0.1:
        person_id1 = generate_person_id(0.0)
        person_id2 = persons[person_id1].get_a_person_in_tag()
    else:
        chance = int(valid_probability * 5.0) + 1
        if not edge_exist(person_id1, person_id2) and chance > 0:
            person_id1, person_id2 = generate_person_id(0.05), generate_person_id(0.05)
            chance -= 1
    if random.random() < delete_probability:
        if person_id1 in persons and person_id2 in persons:
            persons[person_id1].remove_acquaintance(person_id2)
            persons[person_id2].remove_acquaintance(person_id1)
        return f"mr {person_id1} {person_id2} -200"
    else:
        return f"mr {person_id1} {person_id2} {random.randint(-5, 15)}"


function_dict = {
    'ap': generate_add_person_instr,
    'ar': generate_add_relation_instr,
    'mr': generate_modify_relation_instr,
    'at': generate_add_tag_instr,
    'dt': generate_delete_tag_instr,
    'att': generate_add_person_to_tag_instr,
    'dft': generate_delete_person_from_tag_instr,
    'qtvs': generate_query_tag_instr,
    'qtav': generate_query_tag_instr,
    'qsp': generate_query_shortest_path_instr,
    'qba': generate_query_best_instr,
    'qbs': lambda: 'qbs',
    'qts': lambda: 'qts',
    'qcs': lambda: 'qcs',
    'qv': lambda: f"qv {generate_person_id(0.1)} {generate_person_id(0.1)}",
    'qci': lambda: f"qci {generate_person_id(0.1)} {generate_person_id(0.1)}"
}


def generate_instr(instr_kind: str, *args) -> str:
    func = function_dict.get(instr_kind)
    return func(*args)


def generate_stage1() -> str:
    kind = np.random.choice(instructions, p=probabilities1)
    if kind == 'mr':
        return generate_instr(kind, 0.95, 0.3)
    elif kind == 'qtvs' or kind == 'qtav':
        return generate_instr(kind, 0.95, kind)
    elif kind == 'qbs' or kind == 'qts' or kind == 'qcs' or kind == 'qv' or kind == 'qci':
        return generate_instr(kind)
    else:
        return generate_instr(kind, 0.95)


def generate_stage2() -> str:
    kind = np.random.choice(instructions, p=probabilities2)
    if kind == 'mr':
        return generate_instr(kind, 0.95, 0.6)
    elif kind == 'qtvs' or kind == 'qtav':
        return generate_instr(kind, 0.95, kind)
    elif kind == 'qbs' or kind == 'qts' or kind == 'qcs' or kind == 'qv' or kind == 'qci':
        return generate_instr(kind)
    else:
        return generate_instr(kind, 0.95)


def generate(num: int, test_id: int):
    persons.clear()
    with open('in\\in' + str(test_id) + '.txt', 'w') as f:
        f.write(load_network())
        for i in range(num - 1):
            if i < num // 5:
                f.write(generate_stage1() + '\n')
            else:
                f.write(generate_stage2() + '\n')

