import time, sys

RED = '\u001b[41m'
BLUE = '\u001b[44m'
WHITE = '\u001b[47m'

END = "\u001b[0m"
ERASE = "\x1B[2K"
BEGIN = "\x1B[1G"

line = " " * 4
n = 10


def flag():
    for i in range(n):
        if i < n // 2:
            print(f"{BLUE}{line * (i + 1)}{WHITE}{line * (n - i)}{END}")
        else:
            print(f"{BLUE}{line * (n - i)}{RED}{line * (i + 1)}{END}")


def loading():
    for i in range(100):
        time.sleep(0.03)
        print(f"\u001b[100D{i + 1}%", end='', flush=True)
    print(" Done!")


def loading_multiple(n):
    bar_width = 25
    for k in range(1, n + 1):
        for p in range(bar_width  + 1):
            filled = p
            bar = "#" * filled + "-" * (bar_width - filled)
            print(f"{BEGIN}{ERASE}Task {k}/{n} [{bar}] {p * 4}%", 
                  end='', flush=True)
            time.sleep(0.1)


def draw_line(offset=0, lenght=1, color=88):
    line = " " * lenght
    print(f"{" " * offset}\x1b[48;5;{color}m{line}\x1b[0m")


def draw_diamond():
    height = 15
    lenght = 1
    center = height // 2
    offset = height // 2
    step = 1
    colors = [88, 157, 165]
    
    while True:
        for color in colors:
            draw_line(offset, lenght, color)
            if line < color:
                offset -= step
                lenght += step
            else:
                offset += step
                lenght -= step
        print(f"\x1b[{height + 2}A")
        print(f"\x1b[{offset}D")
        lenght = 1
        offset = height // 2
        time.sleep(2)










import time, sys

RED = '\u001b[41m'
BLUE = '\u001b[44m'
WHITE = '\u001b[47m'
BLACK = '\u001b[40m'

END = "\u001b[0m"
ERASE = "\x1B[2K"
BEGIN = "\x1B[1G"


def one():
    line = " " * 4
    n = 12
    for i in range(n):
        if i < n // 3:
            print(f"{RED}{line * n}{END}")
        elif i < n // 3 * 2:
            print(f"{WHITE}{line * n}{END}")
        else:
            print(f"{BLUE}{line * n}{END}")


def two():
    n = 5
    line = " " * 3
    for i in range(n):
        for j in range(n * 2 - 1):
            time.sleep(0.05)
            if i == j or i == n - j - 1 or i == j - 4 or i == n - j + 3:
                print(f"{BLACK}{line}{END}", end='', flush=True)
            else:
                print(f"{WHITE}{line}{END}", end='', flush=True)
        print()
            
            
def three():
    y = 20
    line = " " * 3

    for i in range(y):
        for j in range(y // 2):
            if (y - i - 1) // 2 == j:
                print(f"\u001b[48;5;17m{line}{END}", end='')
            else:
                print(f"{WHITE}{line}{END}", end='')
        print()      
    print(f"\u001b[31mГрафик вида f(x) = 2x{END}")         


def four():
    seq = [float(line) for line in open(r"sequence.txt")]
    sm1 = 0
    sm2 = 0

    for i in range(len(seq)):
        if i % 2 == 1:
            sm1 += seq[i]
        else:
            sm2 += seq[i]
    sm1 = abs(sm1)
    sm2 = abs(sm2)
    sm = sm1 + sm2
    p1 = int(round(sm1 / sm, 2) * 100)
    p2 = int(round(sm2 / sm, 2) * 100)

    lenght = 100

    for i in range(max(p1, p2) + 1):
        if i + 1 <= min(p1, p2):
            bar = "#" * i + "-" * (lenght - i * 2) + "$" * i
            max_min_len = i + 1
            print(f"{BEGIN}{ERASE}{bar}", end='', flush=True)
        else:
            bar = "#" * i + "-" * (lenght - i - max_min_len) + "$" * max_min_len
            print(f"{BEGIN}{ERASE}{bar}", end='', flush=True)
        time.sleep(0.1)
    print()
    time.sleep(0.3)
    print(f"{"Сумма 1" if max(sm1, sm2) == sm1 else "Сумма 2"}{" " * 86}{"Сумма 1" if min(sm1, sm2) == sm1 else "Сумма 2"}")
    time.sleep(0.3)
    print(f"{str(p1) + " %" if max(sm1, sm2) == sm1 else str(p2) + " %"}{" " * (96 - len(str(p1) + str(p2)))}{str(p1) + " %" if min(sm1, sm2) == sm1 else str(p2) + " %"}")


one()
two()
three()
four()