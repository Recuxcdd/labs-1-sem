from csv import reader
from random import randint
import pandas as pd


#ПОЛУЧИТЬ КОЛ-ВО КНИГ С НАЗВАНИЯМИ ДЛИННЕЕ 30 СИМВОЛОВ
def one():
    try:
        with open('books.csv', 'r') as csvfile:
            table = reader(csvfile, delimiter=';')
            cnt = 0
            for row in table:
                if len(row[1]) > 30:
                    cnt += 1
        print(f'Строк длиннее 30 символов: {cnt}.')
    except FileNotFoundError:
            print("Файл не найден!")
            

def search_author(table, author):
    books_found = []
    for row in table:
        if row[3].lower() == author.lower().strip() and row[6].split(' ')[0].split('.')[2] in ['2014', '2016', '2017']: #ОГРАНИЧЕНИЕ ПО ВАРИАНТУ
            books_found.append(row)
    return books_found
    

#ПОИСК ПО АВТОРУ
def two():
    while True:
        author = input('Введите автора: ')
        if author in ['0', '']:
            return 0
        
        try:
            with open('books.csv', 'r') as csvfile:
                table = reader(csvfile, delimiter=';')
                books_found = search_author(table, author)
                
            if len(books_found) == 0:
                print('Книг этого автора не найдено.')
            else:
                print(f'Найдено совпадений: {len(books_found)}.')
                for book in books_found:
                    print(f'\nАвтор: {book[3]}\nНазвание: {book[1]}\nЖанр: {book[12]}\nЦена: {book[7]}')
        except FileNotFoundError:
            print("Файл не найден!")
            break


def get_n_random_rows(df, n):
    got = []
    lenght = df.index.max()
    while len(got) < n:
        rand_index = randint(0, lenght)
        if rand_index not in got:
            got.append(rand_index)
    return got


#СОХРАНИТЬ 20 СЛУЧАНЫХ ЗАПИСЕЙ В ФАЙЛ output_3_task.txt
def three():
    try:
        df = pd.read_csv('books.csv', encoding='cp1251', delimiter=';')
        got = get_n_random_rows(df, 20)
        with open('output_3_task.txt', 'w') as output:
            for ind in got:
                row = df.iloc[ind]
                output.write(f"{str(row['Автор']).replace('nan', 'Неизвестно')}. {row['Название']} - {row['Дата поступления'].split(' ')[0].split('.')[2]}\n")
            print('Файл output_3_task.txt готов.')
    except FileNotFoundError:
        print("Файл не найден!")





#ДОПЗАДАНИЕ

#ВЫВЕСТИ МНОЖЕСТВО ВСЕХ ТЕГОВ
def four():
    try:
        df = pd.read_csv('books.csv', encoding='cp1251', delimiter=';')
        tags = set()
        for row in df['Жанр книги']:
            row_tags = [s.strip() for s in row.split('#')]
            tags.update(row_tags)
        tags.discard('')
        print(list(tags))
    except FileNotFoundError:
        print("Файл не найден!")
        

#20 САМЫХ ПОПУЛЯРНЫХ КНИГ
def five():
    try:
        df = pd.read_csv('books.csv', encoding='cp1251', delimiter=';')
        df['Кол-во выдач'] = pd.to_numeric(df['Кол-во выдач'], errors='coerce').fillna(-1)
        df = df.sort_values(by='Кол-во выдач', ascending=False)
        df_popular = df.head(20)
        authors =  df_popular['Автор']
        names =  df_popular['Название']
        deliveries = df_popular['Кол-во выдач']
        for book in zip(authors, names, deliveries):
            print(f'{book[0]}. {book[1]}. Кол-во выдач: {book[2]};')
    except FileNotFoundError:
        print("Файл не найден!")


one()
print()
two()
print()
three()
print()
four()
print()
five()
