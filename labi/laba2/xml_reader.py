import xml.dom.minidom as minidom
import os

project_folder_dir = os.path.dirname(os.path.abspath(__file__))


#ПАРСИНГ XML В СПИСОК ИМЕН ВАЛЮТ ЕСЛИ NOMINAL == 1
def one():
    try:
        xml_file = open(os.path.join(project_folder_dir, 'currency.xml'), 'r')
        xml_data = xml_file.read()

        dom = minidom.parseString(xml_data)
        dom.normalize()

        valutes = dom.getElementsByTagName('Valute')
        names = []

        for el in valutes:
            nominal = el.getElementsByTagName('Nominal')[0].firstChild.data
            if nominal == '1':
                name = el.getElementsByTagName('Name')[0].firstChild.data
                names.append(name)

        print(names)
    
    except FileNotFoundError:
        print('Файл не найден')


one()