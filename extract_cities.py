def load_unique_cities(filepath):
    cities = set()  # Используем множество для автоматического удаления дубликатов
    with open(filepath, 'r') as file:
        for line in file:
            columns = line.strip().split('|')  # Разделяем строку по символу '|'
            if columns:  # Проверяем, что строка не пустая
                city = columns[0]  # Берем первый столбик (город)
                cities.add(city)  # Добавляем город в множество
    return list(cities)  # Преобразуем множество обратно в список и возвращаем

if "__main__" == __name__:
    # Пример использования
    filepath = 'us_cities_states_counties.csv'  # Укажите путь к вашему файлу
    load_unique_cities = load_unique_cities(filepath)
    print(load_unique_cities)
