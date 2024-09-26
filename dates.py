import re
from collections import defaultdict

# Список місяців для regex
months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December',
    'Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Aug', 'Sep', 'Sept', 'Oct', 'Nov', 'Dec'
]

# Список порядкових числівників для днів
ordinal_numbers = [
    'First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh', 'Eighth', 'Ninth', 'Tenth',
    'Eleventh', 'Twelfth', 'Thirteenth', 'Fourteenth', 'Fifteenth', 'Sixteenth', 'Seventeenth',
    'Eighteenth', 'Nineteenth', 'Twentieth', 'Twenty[- ]First', 'Twenty[- ]Second', 'Twenty[- ]Third',
    'Twenty[- ]Fourth', 'Twenty[- ]Fifth', 'Twenty[- ]Sixth', 'Twenty[- ]Seventh', 'Twenty[- ]Eighth',
    'Twenty[- ]Ninth', 'Thirtieth', 'Thirty[- ]First'
]


# Функція для екранування слів у regex
def escape_words(words):
    return [re.escape(word) for word in words]


# regex для місяців
month_pattern = r'\b(?:' + '|'.join(escape_words(months)) + r')\b'

# Створення regex для порядкових числівників
ordinal_day_pattern = r'\b(?:' + '|'.join(escape_words(ordinal_numbers)) + r')\b'

# regex для числового дня з суфіксами
numeric_day_pattern = r'\b(?:0?[1-9]|[12][0-9]|3[01])(?:st|nd|rd|th)?\b'

# regex для числового місяця
numeric_month_pattern = r'\b(?:0?[1-9]|1[012])\b'

# regex для року (1-4 цифри)
year_pattern = r"\b\d{1,4}\b"

# regex для років з "BC" або "AD"
bc_ad_year_pattern = r"\b\d{1,4}\s*(?:BC|AD)\b"

# Роздільники для дат
date_separators = r'[/\.-]'

# Компіляція regex

# Шаблон для дат типу 01.01.1999, 7-7-777 і т.п
numeric_date_pattern = re.compile(
    r'\b(' + numeric_day_pattern + r')' + date_separators +
    r'(' + numeric_month_pattern + r')' + date_separators +
    r'(' + year_pattern + r')\b'
)

# Шаблон для дат типу 1999-01-01 (ISO формат)
iso_date_pattern = re.compile(
    r'\b(' + year_pattern + r')' + date_separators +
    r'(' + numeric_month_pattern + r')' + date_separators +
    r'(' + numeric_day_pattern + r')\b'
)

# Шаблон для американських дат типу MM/DD/YYYY
us_date_pattern = re.compile(
    r'\b(' + numeric_month_pattern + r')' + date_separators +
    r'(' + numeric_day_pattern + r')' + date_separators +
    r'(' + year_pattern + r')\b'
)

# Шаблон для дат типу July 7th, 2020
textual_date_pattern = re.compile(
    r'\b(' + month_pattern + r')\s+' +
    r'(' + numeric_day_pattern + r')(?:,\s*(' + year_pattern + r'))?\b'
)

# Шаблон для дат типу Third of September, 1999
ordinal_textual_date_pattern = re.compile(
    r'\b(' + ordinal_day_pattern + r')\s+of\s+(' + month_pattern + r')(?:,\s*(' + year_pattern + r'))?\b'
)

# Шаблон для дат типу 44 BC або 100 AD
bc_ad_date_pattern = re.compile(
    r'\b(' + r'\d{1,4}\s*(?:BC|AD)' + r')\b'
)


# Функція для читання тексту з файлу
def read_text_from_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Файл {filepath} не знайдено.")
        return None


filepath = 'input_dates.txt'
text = read_text_from_file(filepath)


# ПЕРШИЙ ПРОХІД: Маркування окремих компонентів
def first_pass(text):
    patterns = [
        ('NUMERIC_DATE', numeric_date_pattern),
        ('ISO_DATE', iso_date_pattern),
        ('US_DATE', us_date_pattern),
        ('TEXTUAL_DATE', textual_date_pattern),
        ('ORDINAL_TEXTUAL_DATE', ordinal_textual_date_pattern),
        ('BC_AD_DATE', bc_ad_date_pattern),
        ('MONTH', re.compile(month_pattern)),
        ('ORDINAL_DAY', re.compile(ordinal_day_pattern)),
        ('NUMERIC_DAY', re.compile(numeric_day_pattern)),
        ('NUMERIC_MONTH', re.compile(numeric_month_pattern)),
        ('YEAR', re.compile(year_pattern)),
    ]

    matches = []
    for tag, regex in patterns:
        for match in regex.finditer(text):
            matches.append({
                'text': match.group(),
                'start': match.start(),
                'end': match.end(),
                'tag': tag
            })

    # Сортуємо та видаляємо перекриття
    matches.sort(key=lambda x: (x['start'], -x['end']))
    non_overlapping = []
    occupied = [False] * len(text)
    for match in matches:
        if not any(occupied[match['start']:match['end']]):
            non_overlapping.append(match)
            for i in range(match['start'], match['end']):
                occupied[i] = True

    return non_overlapping


# ДРУГИЙ ПРОХІД: Об'єднання послідовних компонентів у ланцюжки
def second_pass(matches, text):
    date_tags = ['NUMERIC_DATE', 'ISO_DATE', 'US_DATE', 'TEXTUAL_DATE', 'ORDINAL_TEXTUAL_DATE', 'BC_AD_DATE']

    combined_matches = []
    i = 0
    while i < len(matches):
        match = matches[i]
        if match['tag'] in date_tags:
            combined_matches.append(match)
            i += 1
        else:
            # Намагаємося об'єднати день, місяць і рік у дату
            date_components = [match]
            i += 1
            while i < len(matches):
                next_match = matches[i]
                gap_text = text[date_components[-1]['end']:next_match['start']]
                if next_match['tag'] in ['NUMERIC_DAY', 'ORDINAL_DAY', 'NUMERIC_MONTH', 'MONTH', 'YEAR'] and \
                   re.match(r'^\s*(of\s+|,\s*|\s+)\s*$', gap_text):
                    date_components.append(next_match)
                    i += 1
                else:
                    break
            if len(date_components) > 1:
                start = date_components[0]['start']
                end = date_components[-1]['end']
                combined_text = text[start:end]
                combined_matches.append({
                    'text': combined_text,
                    'start': start,
                    'end': end,
                    'tag': 'DATE',
                    'components': date_components
                })
            else:
                combined_matches.append(match)
    return combined_matches


# ТРЕТІЙ ПРОХІД: Нормалізація і групування дат
def third_pass(matches):
    date_entities = []
    for match in matches:
        if match['tag'] in ['NUMERIC_DATE', 'ISO_DATE', 'US_DATE', 'TEXTUAL_DATE', 'ORDINAL_TEXTUAL_DATE', 'DATE', 'BC_AD_DATE']:
            normalized_date = normalize_date(match)
            if normalized_date:
                date_entities.append(normalized_date)
    return date_entities


# Функція для нормалізації дат у єдиний формат (YYYY-MM-DD)
def normalize_date(match):
    text = match['text']
    tag = match['tag']

    try:
        day = month = year = None

        if tag == 'NUMERIC_DATE':
            result = numeric_date_pattern.match(text)
            if result:
                day, month, year = result.group(1), result.group(2), result.group(3)

        elif tag == 'ISO_DATE':
            result = iso_date_pattern.match(text)
            if result:
                year, month, day = result.group(1), result.group(2), result.group(3)

        elif tag == 'US_DATE':
            result = us_date_pattern.match(text)
            if result:
                month, day, year = result.group(1), result.group(2), result.group(3)

        elif tag == 'TEXTUAL_DATE':
            result = textual_date_pattern.match(text)
            if result:
                month_text, day, year = result.group(1), result.group(2), result.group(3)
                month = month_to_number(month_text)
                year = year if year else '0000'  # Встановлюємо рік за замовчуванням, якщо його немає

        elif tag == 'ORDINAL_TEXTUAL_DATE':
            result = ordinal_textual_date_pattern.match(text)
            if result:
                day_text, month_text, year = result.group(1), result.group(2), result.group(3)
                day = ordinal_to_number(day_text)
                month = month_to_number(month_text)
                year = year if year else '0000'

        elif tag == 'BC_AD_DATE':
            year_text = bc_ad_date_pattern.match(text).group(1)
            return {'original': text, 'normalized': year_text.strip()}

        elif tag == 'DATE':
            # Обробка зібраних дат із окремих компонентів
            components = match['components']
            for comp in components:
                if comp['tag'] in ['NUMERIC_DAY', 'ORDINAL_DAY']:
                    day = ordinal_to_number(comp['text'])
                elif comp['tag'] in ['NUMERIC_MONTH', 'MONTH']:
                    month = month_to_number(comp['text'])
                elif comp['tag'] == 'YEAR':
                    year = comp['text']

        # Перевіряємо наявність всіх компонентів, якщо відсутні — встановлюємо значення за замовчуванням
        if not day:
            day = '00'
        if not month:
            month = '0'
        if not year:
            year = '0000'

        # Видаляємо суфікси з дня, прибираємо зайві нулі з місяця та року
        day = day.rstrip('stndrdth')
        month = month.lstrip('0')

        # Виправляємо нормалізацію для двозначних років
        if len(year) == 2:
            year = '00' + year

        normalized = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
        return {'original': text, 'normalized': normalized}
    except Exception as e:
        print(f"Помилка при нормалізації дати '{text}': {e}")
        return None


# Функція для перетворення назви місяця на номер
def month_to_number(month_name):
    month_name = month_name.lower()
    month_map = {
        'january': '1', 'jan': '1',
        'february': '2', 'feb': '2',
        'march': '3', 'mar': '3',
        'april': '4', 'apr': '4',
        'may': '5',
        'june': '6', 'jun': '6',
        'july': '7', 'jul': '7',
        'august': '8', 'aug': '8',
        'september': '9', 'sept': '9', 'sep': '9',
        'october': '10', 'oct': '10',
        'november': '11', 'nov': '11',
        'december': '12', 'dec': '12',
    }
    return month_map.get(month_name.lower(), '1')


# Функція для перетворення порядкового числівника на число
def ordinal_to_number(ordinal):
    ordinal = ordinal.lower().replace('-', ' ')
    ordinal_map = {
        'first': '1', 'second': '2', 'third': '3', 'fourth': '4', 'fifth': '5',
        'sixth': '6', 'seventh': '7', 'eighth': '8', 'ninth': '9', 'tenth': '10',
        'eleventh': '11', 'twelfth': '12', 'thirteenth': '13', 'fourteenth': '14',
        'fifteenth': '15', 'sixteenth': '16', 'seventeenth': '17', 'eighteenth': '18',
        'nineteenth': '19', 'twentieth': '20', 'twenty first': '21',
        'twenty second': '22', 'twenty third': '23',
        'twenty fourth': '24', 'twenty fifth': '25',
        'twenty sixth': '26', 'twenty seventh': '27',
        'twenty eighth': '28', 'twenty ninth': '29',
        'thirtieth': '30', 'thirty first': '31',
    }
    return ordinal_map.get(ordinal.lower(), ordinal.rstrip('stndrdth'))


# Застосовуємо 1 прохід
first_pass_matches = first_pass(text)
print("ПЕРШИЙ ПРОХІД: Знайдені сутності")
for match in first_pass_matches:
    print(f"[{match['tag']}] '{match['text']}' (позиції {match['start']}-{match['end']})")

# Застосовуємо 2 прохід
combined_matches = second_pass(first_pass_matches, text)
print("\nДРУГИЙ ПРОХІД: Об'єднані дати")
for match in combined_matches:
    if 'components' in match:
        components = ', '.join([comp['text'] for comp in match['components']])
        print(f"[{match['tag']}] '{match['text']}' з компонентів [{components}]")
    else:
        print(f"[{match['tag']}] '{match['text']}'")

# Застосовуємо 3 прохід
final_entities = third_pass(combined_matches)
print("\nТРЕТІЙ ПРОХІД: Нормалізовані дати")
for entity in final_entities:
    print(f"Оригінал: '{entity['original']}', Нормалізовано: '{entity['normalized']}'")


# Групування дат за нормалізованими значеннями
def group_dates(entities):
    grouped = defaultdict(list)
    for entity in entities:
        key = entity['normalized']
        grouped[key].append(entity['original'])
    return grouped


grouped_dates = group_dates(final_entities)
print("\nЗГРУПОВАНІ ДАТИ:")
for key, dates in grouped_dates.items():
    print(f"\nДата: {key}")
    for date in dates:
        print(f" - {date}")
