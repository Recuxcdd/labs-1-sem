from itertools import combinations


def get_score(start_value, items, taken):
    total_value = sum(info['value'] for info in items.values())
    taken_value = sum(items[key]['value'] for key in taken)
    return start_value + taken_value - (total_value - taken_value)


def next_good_ij_and_axis(inv, item):
    size = items[item]['size']
    rows = len(inv)
    cols = len(inv[0])
    #поиск ij куда можно засунуть предмет в двух осях
    for i in range(rows):
        for j in range(cols):
            #1 и 0 в return - оси: 0 - x, 1 - y
            if inv[i][j] == '[ ]' and j + size <= cols: #ось x
                return i, j, 0
            if inv[i][j] == '[ ]' and i + size <= rows: #ось y
                return i, j, 1
    return False


def draw_inventory(inventory, rows, cols):
    inv = [['[ ]' for _ in range(cols)] for _ in range(rows)]
    #сортируем по размеру чтобы сначала точно вместить большие
    inventory_sorted = sorted(inventory, key=lambda x: items[x]['size'], reverse=True)

    for item in inventory_sorted:
        size = items[item]['size']
        good_place = next_good_ij_and_axis(inv, item)
        if good_place:
            row, col, axis = good_place
            for j in range(size):
                if axis == 0:
                    inv[row][col + j] = f'[{item}]'
                else:
                    inv[row + j][col] = f'[{item}]'
        else:
            print(f'{item} не умещается')

    print()
    for row in inv:
        print(','.join(row))   
    

def backpack_problem(items, inventory_size, illness, start_value, find_all=False):
    rows, cols = inventory_size
    capacity = rows * cols
    best_score = -float('inf')
    best_inventory = None
    if find_all:
        all_inventories = []
    
    for n_items in range(1, len(items) + 1):
        for inventory in combinations(items.keys(), n_items):
            size = sum(items[key]['size'] for key in inventory)
            if size <= capacity and (illness_items[illness] in inventory or illness is None):
                value = sum(items[key]['value'] for key in inventory)
                score = get_score(start_value, items, inventory)
                if score > best_score and score > 0:
                    best_score = score
                    best_inventory = inventory
                    if find_all:
                        all_inventories.append(inventory)
    
    #best_inventory будет None только если ни одного решения с положительным score не найдется
    if best_inventory is None:
        print('Нет решения')
        return
    
    inv = [['[ ]' for _ in range(cols)] for _ in range(rows)]
    #сортируем по размеру чтобы сначала точно вместить большие
    if find_all:
        for inventory in all_inventories:
            draw_inventory(inventory, rows, cols)
    else:
        best_inventory_sorted = sorted(best_inventory, key=lambda x: items[x]['size'], reverse=True)
        draw_inventory(best_inventory_sorted, rows, cols)
        print(f'\nИтоговые очки выживания: {best_score}')   
    


items = {
    'r': {'size': 3, 'value': 25},
    'p': {'size': 2, 'value': 15},
    'a': {'size': 2, 'value': 15},
    'm': {'size': 2, 'value': 20},
    'i': {'size': 1, 'value': 5},
    'k': {'size': 1, 'value': 15},
    'x': {'size': 3, 'value': 20},
    't': {'size': 1, 'value': 25},
    'f': {'size': 1, 'value': 15},
    'd': {'size': 1, 'value': 10},
    's': {'size': 2, 'value': 20},
    'c': {'size': 2, 'value': 20},
}

illness_items = {
    None: 0, #костыль чтобы illness_item[None] не вызывало ошибку
    'infection': 'd',
    'asthma': 'i'
}

inventory_size = (2, 4)
illness = 'infection'
start_value = 10

#решение 3 варианта
backpack_problem(items, inventory_size, illness, start_value)
print('-' * 50)

#допзадание для инвентаря (1, 7) или (7, 1). для моего кода одно и то же
#нет решения только если не нашлось ни одной комбинации предметов с положительным score
backpack_problem(items, (1, 7), illness, start_value)
print('-' * 50)

#найти все комбинации при score > 0
backpack_problem(items, inventory_size, illness, start_value, find_all=True)