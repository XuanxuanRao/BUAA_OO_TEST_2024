import random

instr_list1 = ['ap', 'ap', 'ap', 'ar', 'ar', 'ar', 'mr', 'qv', 'qci', 'qbs', 'qts']
instr_list2 = ['ap', 'ar', 'ar', 'ar', 'ar', 'ar', 'mr', 'mr', 'qv', 'qv', 'qci', 'qci', 'qbs', 'qbs', 'qts', 'qts']
instr_list3 = ['ap', 'ar', 'ar', 'ar', 'mr', 'mr', 'mr', 'mr', 'mr', 'qv', 'qci', 'qbs', 'qbs', 'qts', 'qts']
G = {}
name_list = ['rcx', 'wdy', 'zjq', 'yyw']
ids = set()


def load_network() -> str:
    n = random.randint(30, 100)
    instr = 'ln ' + str(n) + '\n'
    line = ''
    id_list = []
    for _ in range(0, n):
        person_id = generate_person_id(1.0)
        line += str(person_id) + ' '
        ids.add(person_id)
        id_list.append(person_id)
        if person_id not in G:
            G[person_id] = set()
    instr += line + '\n'
    line = ''
    for _ in range(0, n):
        line += random.choice(name_list) + ' '
    instr += line + '\n'
    line = ''
    for _ in range(0, n):
        line += str(random.randint(1, 200)) + ' '
    instr += line + '\n'
    for i in range(1, n):
        line = ''
        for j in range(i):
            val = random.randint(0, 4)
            line += str(val) + ' '
            if val > 0:
                G[id_list[i]].add(id_list[j])
                G[id_list[j]].add(id_list[i])
        instr += line + '\n'
    return instr


def generate_person_id(new_id_probability: float) -> int:
    if random.random() < new_id_probability or len(ids) == 0:
        person_id = random.randint(1, 0x7fffffff)
        while person_id in ids:
            person_id = random.randint(1, 0x7fffffff)
    else:
        person_id = random.choice(list(ids))
    return person_id


def edge_exist(person_id1: int, person_id2: int) -> bool:
    if person_id1 not in G or person_id2 not in G:
        return False
    return person_id2 in G[person_id1] and person_id1 in G[person_id2]


def can_add_edge(person_id1: int, person_id2: int) -> bool:
    if person_id1 not in G or person_id2 not in G:
        return False
    return person_id1 not in G[person_id2] and person_id2 not in G[person_id1]


def generate_stage1() -> str:
    """
        Generate the instr to fill the network(add person and relationship)
    """
    instr = random.choice(instr_list1 if len(ids) < 1000 else instr_list2)
    if len(ids) >= 1000 and instr != 'ar':
        instr = random.choice(instr_list2)
    if instr == 'ap':
        person_id = generate_person_id(0.95)
        instr += f" {person_id} {random.choice(name_list)} {random.randint(1, 50)}"
        ids.add(person_id)
        if person_id not in G:
            G[person_id] = set()
    elif instr == 'ar' or instr == 'mr':
        person_id1, person_id2 = generate_person_id(0.05), generate_person_id(0.05)
        if instr == 'ar':
            chance = 5
            while not can_add_edge(person_id1, person_id2) and chance > 0:
                person_id1, person_id2 = generate_person_id(0.05), generate_person_id(0.05)
                chance -= 1
            if person_id1 in G and person_id2 in G:
                G[person_id1].add(person_id2)
                G[person_id2].add(person_id1)
            instr += f" {person_id1} {person_id2} {random.randint(1, 20)}"
        else:
            instr += f" {person_id1} {person_id2} {random.randint(-50, 10)}"
    elif instr == 'qv' or instr == 'qci':
        person_id1, person_id2 = generate_person_id(0.1), generate_person_id(0.1)
        instr += f" {person_id1} {person_id2}"
    elif instr == 'qbs' or instr == 'qts':
        instr += ""
    return instr


def generate_stage2() -> str:
    instr = random.choice(instr_list3)
    if instr == 'ap':
        person_id = generate_person_id(0.05)
        instr += f" {person_id} {random.choice(name_list)} {random.randint(1, 200)}"
        ids.add(person_id)
    elif instr == 'ar' or instr == 'mr':
        person_id1, person_id2 = generate_person_id(0.05), generate_person_id(0.05)
        if instr == 'ar':
            instr += f" {person_id1} {person_id2} {random.randint(1, 10)}"
        else:
            chance = 3
            if not edge_exist(person_id1, person_id2) and chance > 0:
                person_id1, person_id2 = generate_person_id(0.05), generate_person_id(0.05)
                chance -= 1
            instr += f" {person_id1} {person_id2} {random.randint(-200, 10)}"
    elif instr == 'qv' or instr == 'qci':
        person_id1, person_id2 = generate_person_id(0.1), generate_person_id(0.1)
        instr += f" {person_id1} {person_id2}"
    elif instr == 'qbs' or instr == 'qts':
        instr += ""
    return instr


def generate(num: int, test_id: int):
    ids.clear()
    G.clear()
    with open('in\\in' + str(test_id) + '.txt', 'w') as f:
        if test_id % 2 == 0:
            f.write(load_network())
        for i in range(num - 1):
            if i < num // 10:
                f.write(generate_stage1() + '\n')
            else:
                f.write(generate_stage2() + '\n')
