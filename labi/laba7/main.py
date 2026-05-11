import requests
import json
import os
from random import choice
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


def one(): #ДЛЯ ГОРОДА МОСКВА
    api_key = 'fb3a99c4cb521f7800a44cb8367ddc17'
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={55.75396}&lon={37.620393}&appid={api_key}'
    response = requests.get(url, timeout=5)
    data = json.loads(response.text)
    
    with open(os.path.join(PROJECT_DIR, 'weather_api.json'), 'w') as jf:
        json.dump(data, jf, indent=4)
        
    if response.status_code == 200:
        print('-' * 20)
        print('City: Moscow')
        print(f'Weather: {data['weather'][0]['description']}')
        print(f'Humidity: {data['main']['humidity']} %')
        print(f'Atmospheric pressure: {data['main']['pressure']} hPa')
        print('-' * 20)
    else:
        print('Smth is wrong,', response.status_code)
    

def two():
    api_key = 'b871d7debaed4475873d01e9890eba67'
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
    response = requests.get(url, timeout=5)
    data = json.loads(response.text)
    
    with open(os.path.join(PROJECT_DIR, 'news_api.json'), 'w') as jf:
        json.dump(data, jf, indent=4)

    if response.status_code == 200:
        random_news = choice(data['articles'])
        print('-' * 20)
        print(f'Found results: {data['totalResults']}')
        print()
        print('Random news:')
        print(f'Title: {random_news['title']}')
        print(f'Published at: {random_news['publishedAt'].replace('-', '.').replace('T', ' ').replace('Z', ' UTC')}')
        print(f'Author: {random_news['author']}')
        print(f'Text: {random_news['content']}')
        print('-' * 20)
    else:
        print('Smth is wrong,', response.status_code)


def additional():
    url = 'https://cataas.com/cat'
    
    class App:
        
        def __init__(self):
            self.root = tk.Tk()
            self.root.title('Additional by Егорик')
            self.width = self.root.winfo_screenwidth()
            self.height = self.root.winfo_screenheight()
            self.root.geometry(f'{self.width // 2}x{self.height // 2}')
            self.root.resizable(False, False)
            
            #кнопка генерации
            self.button = tk.Button(self.root,  text='🔥Получить картинку кошки бесплатно прямо сейчас🔥', font=('Arial', 16), command=self.get_n_show_pussy)
            self.button.place(relx=0.5, rely=0.9, anchor='center')
            
            #картинка
            self.label = tk.Label(self.root)
            self.label.place(relx=0.5, rely=0.43, anchor='center')
            
        def get_n_show_pussy(self):
            response = requests.get(url, timeout=5)
            with open(os.path.join(PROJECT_DIR, 'cat.png'), 'wb') as f:
                f.write(response.content)
            img = Image.open(BytesIO(response.content))
            w, h = img.size
            ratio = w / h
            if ratio >= self.width / self.height:
                new_w = int(self.width // 2 * 0.9)
                new_h = int(new_w / ratio)
            else:
                new_h = int(self.height // 2 * 0.8)
                new_w = int(new_h * ratio)
                
            self.tk_img = ImageTk.PhotoImage(img.resize((new_w, new_h)))
            self.label.config(image=self.tk_img)
            
        def run(self):
            self.root.mainloop()

        
    app = App()
    app.run()


one()
two()
additional()