from itertools import combinations


def get_score(start_value, items, taken):
    total_value = sum(info['value'] for info in items.values())
    taken_value = sum(items[key]['value'] for key in taken)
    return start_value + taken_value - (total_value - taken_value)


def next_good_ij(inv, item):
    size = items[item]['size']
    rows = len(inv)
    cols = len(inv[0])
    for i in range(rows):
        for j in range(cols):
            if inv[i][j] == '[ ]' and j + size <= cols and i < rows:
                return i, j
    return False


items = {
    'r': {'name': 'rifle', 'size': 3, 'value': 25},
    'p': {'name': 'pistol', 'size': 2, 'value': 15},
    'a': {'name': 'ammo', 'size': 2, 'value': 15},
    'm': {'name': 'medkit', 'size': 2, 'value': 20},
    'i': {'name': 'inhaler', 'size': 1, 'value': 5},
    'k': {'name': 'knife', 'size': 1, 'value': 15},
    'x': {'name': 'axe', 'size': 3, 'value': 20},
    't': {'name': 'talisman', 'size': 1, 'value': 25},
    'f': {'name': 'flask', 'size': 1, 'value': 15},
    'd': {'name': 'antidote', 'size': 1, 'value': 10},
    's': {'name': 'supplies', 'size': 2, 'value': 20},
    'c': {'name': 'crossbow', 'size': 2, 'value': 20},
}

illness_items = {
    'infection': 'd',
    'asthma': 'i'
}

inventory_size = (2, 4)
illness = "infection"
start_value = 10

capacity = inventory_size[0] * inventory_size[1]

best_score = -float('inf')
best_inventory = None

for n_items in range(1, len(items) + 1):
    for inventory in combinations(items.keys(), n_items):
        size = sum(items[key]['size'] for key in inventory)
        if size <= capacity and illness_items[illness] in inventory:
            value = sum(items[key]['value'] for key in inventory)
            score = get_score(start_value, items, inventory)
            if score > best_score:
                best_score = score
                best_inventory = inventory

rows, cols = sorted(inventory_size)

inv = [['[ ]' for _ in range(cols)] for _ in range(rows)]
best_inventory_sorted = sorted(best_inventory, key=lambda x: items[x]['size'], reverse=True)

for item in best_inventory_sorted:
    size = items[item]['size']
    good_place = next_good_ij(inv, item)
    if good_place:
        row, col = good_place
        for j in range(size):
            inv[row][col + j] = f'[{item}]'
    else:
        print(f'{item} не умещается')
    
for row in inv:
    print(','.join(row))
print(f'\nИтоговые очки выживания: {best_score}')