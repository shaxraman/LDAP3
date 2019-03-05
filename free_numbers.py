#        Поиск свободных номеров из списка
#        v 1.0
#        ищет построчно из файла. без букв и пустрых пробелов, энтеров

file_name = 'number.txt'  # Имя файла, где смотреть номера
free_num = list(range(700, 861))  # 161 номер   # Диапазон номеров для поиска
def main():
    with open(file_name, 'r', encoding='utf8') as file:
        for i in file.readlines():
            if int(i) in free_num:
                free_num.remove(int(i))
    print(free_num)
    print('free numbers - ', len(free_num))

if __name__ == '__main__':
    main()
