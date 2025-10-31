import tkinter as tk
from tkinter import PhotoImage
import os
from random import choice, shuffle   
from math import gcd

    
class TKKeyGen:
    
    def __init__(self):
        
        self.ALPHA = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        
        self.root = tk.Tk()
        self.root.title('KeyGen by Егорик')
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.geometry(f'{width // 2}x{height // 2}')
        self.root.resizable(False, False)
        #Сначала хотел использовать в будущем соотношение сторон экрана, но теперь как будто и не надо, но стирать жалко
        nod = gcd(width, height)
        self.screen_ratio = (width // nod, height // nod, width // nod / (height // nod))
        self.key = False
        
        #ИНИЦИАЛИЗАЦИЯ ВИДЖЕТОВ
        
        #Надпись введите семя
        self.label = tk.Label(self.root, text='Введите семечко:', font=('Arial', 18))
        self.label.place(relx=0.5, rely=0.3, anchor='center')
        
        #поле для ввода
        self.seed_entry = tk.Entry(self.root, font=('Arial', 18))
        self.seed_entry.place(relx=0.5, rely=0.4, anchor='center')
        
        #кнопка генерации
        self.button = tk.Button(self.root,  text='Сгенерировать ключ', font=('Arial', 16), command=self.generate_key)
        self.button.place(relx=0.5, rely=0.5, anchor='center')
        
        #надпись неправильного семени
        self.incorrect_seed_label = tk.Label(self.root, text='Некорректное семечко', font=('Arial', 8), fg='red')
        
        #вывод сген ключа
        self.generated_key = tk.Entry(self.root, font=('Arial', 18), justify='center', width=25)
        
        #конпка копировать с иконкой
        project_folder_dir = os.path.dirname(os.path.abspath(__file__))
        icon_copy_dir = os.path.join(project_folder_dir, 'images', 'icon_copy.png')
        
        icon_copy = PhotoImage(file=icon_copy_dir)
        resize_coef = int(512 / (height // 2 * 0.067) * 1.5)
        resized_icon_copy = icon_copy.subsample(resize_coef, resize_coef)
        self.copy_button = tk.Button(self.root, image=resized_icon_copy, command=self.get_key_to_boof)
        self.copy_button.image = resized_icon_copy
        
        #надпись скопировано
        self.copied = tk.Label(self.root, text='Скопировано', font=('Arial', 8), fg='green')
        

    def is_valid_seed(self, seed):
        try:
            dec_seed = int(str(seed), 16)
            if len(str(dec_seed)) >= 3 and 'x' not in seed.lower():
                return True
            else:
                return False
        except Exception:
            return False
        
    def generate_key(self):
        seed = self.seed_entry.get()
        
        if self.is_valid_seed(seed):
            dec_seed = str(int(str(seed), 16))
            key = ''
            for i in range(3):
                chars = [dec_seed[i]] + [choice(self.ALPHA) for _ in range(4)]
                shuffle(chars)
                key += ''.join(chars)
                if i != 2:
                    key += '-'
            key += f' {dec_seed[-2:]}'
            self.incorrect_seed = False
            self.key = key
        else:
            self.incorrect_seed = True
            self.key = False
            
        self.update_window()
        
    def update_window(self):
        self.copied.place_forget()
        if self.incorrect_seed:
            self.generated_key.place_forget()
            self.copy_button.place_forget()
            self.incorrect_seed_label.place(relx=0.5, rely=0.57, anchor='center')
        else:
            self.incorrect_seed_label.place_forget()
            self.generated_key.config(state='normal')
            self.generated_key.delete(0, tk.END)
            self.generated_key.insert(0, self.key)
            self.generated_key.selection_range(0, tk.END)
            self.generated_key.config(state='readonly')
            self.generated_key.place(relx=0.5, rely=0.7, anchor='center')
            self.copy_button.place(relx=0.75, rely=0.7, anchor='center', relwidth=0.067 / self.screen_ratio[2], relheight=0.067)
    
    def get_key_to_boof(self):
        key = self.key
        if key:
            self.root.clipboard_clear()
            self.root.clipboard_append(key)
            self.root.update()
            self.copied.place(relx=0.75, rely=0.76, anchor='center')
    
    def start(self):
        self.root.mainloop()


keygen = TKKeyGen()
keygen.start()