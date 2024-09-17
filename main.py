import re


# Функція для завантаження лексикону з файлу
def load_lexicon(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lexicon = set(line.strip() for line in file)
    return lexicon


# Функція для пошуку сутностей за допомогою регулярних виразів, включаючи абревіатури
def find_entities_by_regex(text):
    # Шукаємо сутності, що починаються з великої літери, і складаються з одного або кількох слів або абревіатур (послідовність великих літер)
    pattern = r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b|\b[A-Z]{2,}\b'
    return re.findall(pattern, text)


# Функція для пошуку сутностей за допомогою лексикону
def find_entities_by_lexicon(text, lexicon):
    words = text.split()
    found_entities = set()
    # Убираем найденные слова из текста и сохраняем их в найденные сущности
    remaining_words = []
    for word in words:
        if word in lexicon:
            found_entities.add(word)
        else:
            remaining_words.append(word)  # Оставляем только те слова, которые не были найдены
    return found_entities, ' '.join(remaining_words)  # Возвращаем оставшийся текст


# Функція для читання тексту з файлу
def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


# Об'єднання результатів
def find_entities(text, lexicon):
    # Спочатку шукаємо за допомогою лексикону, залишаючи решту тексту для обробки регулярними виразами
    entities_by_lexicon, remaining_text = find_entities_by_lexicon(text, lexicon)

    # Пошук за допомогою регулярних виразів тільки в частинах, які залишилися
    entities_by_regex = find_entities_by_regex(remaining_text)

    # Об'єднуємо результати
    return entities_by_lexicon | set(entities_by_regex)


# Приклад роботи програми
if __name__ == "__main__":
    # Читання тексту з файлу (наприклад, "input.txt")
    text = load_text("input.txt")

    # Завантажуємо лексикон з файлу (наприклад, "lexicon.txt")
    lexicon = load_lexicon("lexicon.txt")

    # Знаходимо сутності
    entities = find_entities(text, lexicon)

    # Виводимо результат
    print(f"Found entities: {entities}")
