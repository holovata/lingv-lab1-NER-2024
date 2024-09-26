import re
from extract_cities import load_unique_cities
from collections import defaultdict

# Список країн
countries = ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua & Deps", "Argentina", "Armenia", "Australia",
             "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin",
             "Bhutan", "Bolivia", "Bosnia Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina", "Burundi",
             "Cambodia", "Cameroon", "Canada", "Cape Verde", "Central African Rep", "Chad", "Chile", "China", "Colombia",
             "Comoros", "Congo", "Congo {Democratic Rep}", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic",
             "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor", "Ecuador", "Egypt", "El Salvador",
             "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia",
             "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti",
             "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland {Republic}", "Israel", "Italy",
             "Ivory Coast", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea North", "Korea South",
             "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein",
             "Lithuania", "Luxembourg", "Macedonia", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta",
             "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia",
             "Montenegro", "Morocco", "Mozambique", "Myanmar, {Burma}", "Namibia", "Nauru", "Nepal", "Netherlands",
             "New Zealand", "Nicaragua", "Niger", "Nigeria", "Norway", "Oman", "Pakistan", "Palau", "Panama",
             "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania",
             "Russian Federation", "Rwanda", "St Kitts & Nevis", "St Lucia", "Saint Vincent & the Grenadines", "Samoa",
             "San Marino", "Sao Tome & Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone",
             "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Sudan", "Spain",
             "Sri Lanka", "Sudan", "Suriname", "Swaziland", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan",
             "Tanzania", "Thailand", "Togo", "Tonga", "Trinidad & Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu",
             "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan",
             "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"]

# Список повних назв штатів
states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida",
          "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
          "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska",
          "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
          "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas",
          "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

# Список скорочень штатів
state_abbreviations = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL",
                       "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA",
                       "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE",
                       "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
                       "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT",
                       "VA", "WA", "WV", "WI", "WY"]


# Функція для екранування назв у regex
def escape_words(words):
    escaped_words = []
    for word in words:
        escaped_word = re.escape(word)
        escaped_word = escaped_word.replace(r'\ ', r'\s+')
        escaped_words.append(escaped_word)
    return escaped_words


# Перетворення списків країн, штатів та їхніх скорочень у рядки для regex
country_pattern = r'\b(?:' + '|'.join(escape_words(countries)) + r')\b'
state_pattern = r'\b(?:' + '|'.join(escape_words(states)) + r')\b'
state_abbrev_pattern = r'\b(?:' + '|'.join(state_abbreviations) + r')\b'

# regex для компонентів адреси
zip_pattern = r"\b\d{5}(?:-\d{4})?\b"  # Пошук як 5-значних, так і розширених ZIP-кодів

# regex для вулиці з різними суфіксами
street_suffixes = ['Avenue', 'Ave', 'Lane', 'Ln', 'Road', 'Rd', 'Boulevard', 'Blvd', 'Street', 'St', 'Drive', 'Dr', 'Court',
                   'Ct', 'Place', 'Pl', 'Terrace', 'Ter', 'Way', 'Wy', 'Circle', 'Cir', 'Broadway', 'Pine', 'Parkway',
                   'Pkwy', 'Square', 'Sq', 'Boulevard', 'Blvd', 'Street', 'St']

street_suffix_pattern = r'\b(?:' + '|'.join(street_suffixes) + r')\.?\b'

# regex для назви вулиці без номеру будинку
street_name_pattern = r"\b(?:[A-Z][a-zA-Z0-9.-]+\s+)+" + street_suffix_pattern

# regex для вулиці з числовим номером
street_pattern = r"\b\d+\s+(?:[A-Za-z0-9.-]+\s+){0,3}" + r"(?:{}(?:\.|))\b".format(street_suffix_pattern)

# Компіляція regex
country_re = re.compile(country_pattern)
street_re = re.compile(street_pattern)
street_name_re = re.compile(street_name_pattern)
state_re = re.compile(state_pattern)
state_abbrev_re = re.compile(state_abbrev_pattern)
zip_re = re.compile(zip_pattern)

# Завантаження списку міст
cities = load_unique_cities("us_cities_states_counties.csv")  # Завантажуємо список міст


# Функція для екранування назв міст у регулярних виразах
def escape_cities(cities):
    escaped_cities = []
    for city in cities:
        escaped_city = re.escape(city)
        escaped_city = escaped_city.replace(r'\ ', r'\s+')
        escaped_cities.append(escaped_city)
    return escaped_cities


# Створення regex для міст
def city_pattern():
    escaped_cities = escape_cities(cities)
    # Сортуємо міста за довжиною у зворотному порядку, щоб довші назви збігалися першими
    escaped_cities.sort(key=len, reverse=True)
    city_regex = r'\b(?:' + '|'.join(escaped_cities) + r')\b'
    return city_regex


city_re = re.compile(city_pattern())


# Функція для читання тексту з файлу
def read_text_from_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print(f"Файл {filepath} не знайдено.")
        return None


filepath = 'input.txt'
text = read_text_from_file(filepath)


# Перший прохід: Розмітка простих NE
def first_pass(text):
    patterns = [
        ('STREET', street_re),
        ('STREET_NAME', street_name_re),
        ('STATE', state_re),
        ('STATE_ABBREV', state_abbrev_re),
        ('ZIP', zip_re),
        ('COUNTRY', country_re),
        ('CITY', city_re),
    ]

    matches = []
    for tag, regex in patterns:
        for match in regex.finditer(text):
            # Пропускаємо CITY, якщо воно не починається з великої літери
            if tag == 'CITY' and not match.group()[0].isupper():
                continue
            matches.append({
                'text': match.group(),
                'start': match.start(),
                'end': match.end(),
                'tag': tag
            })

    # Сортуємо та видаляємо перекриття
    matches.sort(key=lambda x: x['start'])
    non_overlapping = []
    last_end = -1
    for match in matches:
        if match['start'] >= last_end:
            non_overlapping.append(match)
            last_end = match['end']

    for i in range(len(non_overlapping) - 1):
        non_overlapping[i]['next'] = non_overlapping[i + 1]['start']
    non_overlapping[-1]['next'] = len(text)

    return non_overlapping


# Застосовуємо 1 прохід
first_pass_matches = first_pass(text)
print("ПЕРШИЙ ПРОХІД: Знайдені сутності")
for match in first_pass_matches:
    print(f"[{match['tag']}] {match['text']} (позиції {match['start']}–{match['end']})")


# Другий прохід: Об'єднання послідовних адресних компонентів в адреси
def second_pass(matches, text):
    # Список тегів, що належать до адресних компонентів
    address_components = ['STREET', 'STREET_NAME', 'CITY', 'STATE', 'STATE_ABBREV', 'ZIP', 'COUNTRY']
    combined_matches = []
    i = 0
    while i < len(matches):
        match = matches[i]
        if match['tag'] in address_components:
            address = [match]
            i += 1
            # Збираємо суміжні адресні компоненти
            while i < len(matches):
                next_match = matches[i]
                gap_text = text[address[-1]['end']:next_match['start']]
                if next_match['tag'] in address_components and re.match(r'^\s*,?\s*$', gap_text):
                    address.append(next_match)
                    i += 1
                else:
                    break
            # Об'єднуємо компоненти, якщо довжина ланцюжка більше 1
            if len(address) > 1:
                start = address[0]['start']
                end = address[-1]['end']
                combined_text = text[start:end]
                combined_matches.append({
                    'text': combined_text,
                    'start': start,
                    'end': end,
                    'tag': 'ADDRESS',
                    'components': address
                })
            else:
                # Якщо компонент один, додаємо його без змін
                combined_matches.append(match)
        else:
            combined_matches.append(match)
            i += 1
    return combined_matches


# Застосовуємо 2 прохід
combined_matches = second_pass(first_pass_matches, text)
print("\nДРУГИЙ ПРОХІД: Об'єднані адреси")
for match in combined_matches:
    if match['tag'] == 'ADDRESS':
        print(f"[ADDRESS] {match['text']} (позиції {match['start']}–{match['end']})")
    else:
        print(f"[{match['tag']}] {match['text']} (позиції {match['start']}–{match['end']})")

# Створюємо словники для еквівалентності назв вулиць та штатів
street_equivalents = {
    "St": "Street",
    "Ave": "Avenue",
    "Ln": "Lane",
    "Rd": "Road",
    "Blvd": "Boulevard",
    "Dr": "Drive",
    "Ct": "Court",
    "Pl": "Place",
    "Ter": "Terrace",
    "Wy": "Way",
    "Cir": "Circle",
    "Pkwy": "Parkway",
    "Sq": "Square"
}
state_equivalents = dict(zip(state_abbreviations, states))


# Функція для заміни скорочених версій на повні
def normalize_component(text, tag):
    if tag == 'STREET' or tag == 'STREET_NAME':
        for short, full in street_equivalents.items():
            pattern = r'\b{}\b\.?'.format(re.escape(short))
            text = re.sub(pattern, full, text)
        return text
    if tag == 'STATE_ABBREV':
        return state_equivalents.get(text, text)
    return text


def third_pass(matches):
    final_entities = []
    seen_addresses = set()
    for match in matches:
        # Обробляємо кожен компонент адреси
        if match['tag'] == 'ADDRESS':
            normalized_components = []
            component_dict = {}
            for component in match['components']:
                normalized_text = normalize_component(component['text'], component['tag'])
                normalized_components.append(normalized_text)
                # Зберігаємо компоненти в словник
                if component['tag'] == 'STREET' or component['tag'] == 'STREET_NAME':
                    # Витягуємо номер будинку та назву вулиці
                    street_match = re.match(r'^(\d+)\s+(.*)$', normalized_text)
                    if street_match:
                        component_dict['house_number'] = street_match.group(1).lower()
                        component_dict['street_name'] = street_match.group(2).lower()
                    else:
                        component_dict['street_name'] = normalized_text.lower()
                elif component['tag'] == 'CITY':
                    component_dict['city'] = normalized_text.lower()
                elif component['tag'] == 'STATE' or component['tag'] == 'STATE_ABBREV':
                    component_dict['state'] = normalized_text.lower()
                elif component['tag'] == 'ZIP':
                    component_dict['zip'] = normalized_text.lower()
            # Формуємо нормалізовану адресу
            final_address = ", ".join(normalized_components)
            if final_address not in seen_addresses:
                seen_addresses.add(final_address)
                final_entities.append((final_address, component_dict))
    return final_entities


# Застосовуємо 3 прохід
final_entities = third_pass(combined_matches)


# Функція generate_keys створює унікальні ключі для кожної адреси на основі її компонентів.
# Вона використовує компоненти адреси (назва вулиці, місто, штат, (ZIP-код),
# щоб згенерувати можливі комбінації ключів для порівняння і групування адрес
# 1. Якщо є ZIP-код, додаємо його до набору ключів
# 2. Якщо є і назва вулиці, і місто, створюється комбінація цих двох компонентів
# 3. Якщо є лише назва вулиці, вона використовується як ключ
# 4. Якщо назви вулиці немає, але є місто і штат, створюється комбінація цих компонентів
# Кожен ключ додається до набору keys, який повертається функцією
def generate_keys(component_dict):
    keys = set()
    street_name = component_dict.get('street_name', '').lower()
    city = component_dict.get('city', '').lower()
    state = component_dict.get('state', '').lower()
    zip_code = component_dict.get('zip', '')

    # Якщо є ZIP-код, використовуємо його в ключі
    if zip_code:
        keys.add(f"{zip_code}")

    # Створюємо комбінації компонентів, що включають назву вулиці та місто
    if street_name and city:
        keys.add(f"{street_name}|{city}")
    elif street_name:
        keys.add(street_name)
    else:
        # Якщо назви вулиці немає, використовуємо комбінацію міста та штату
        if city and state:
            keys.add(f"{city}|{state}")

    return keys


# Функція для групування адрес
def group_addresses(entities):
    key_to_addresses = defaultdict(set)
    address_to_keys = {}

    for address, components in entities:
        keys = generate_keys(components)
        address_to_keys[address] = keys
        for key in keys:
            key_to_addresses[key].add(address)

    # Об'єднуємо групи на основі перетину ключів
    groups = []
    visited = set()

    for address in address_to_keys:
        if address in visited:
            continue
        stack = [address]
        group = set()
        while stack:
            current_address = stack.pop()
            if current_address in visited:
                continue
            visited.add(current_address)
            group.add(current_address)
            current_keys = address_to_keys[current_address]
            for key in current_keys:
                neighbors = key_to_addresses[key]
                for neighbor in neighbors:
                    if neighbor not in visited:
                        stack.append(neighbor)
        groups.append(group)
    return groups


groups = group_addresses(final_entities)
print("\nЗГРУПОВАНІ АДРЕСИ:")
for i, group in enumerate(groups, 1):
    print(f"\nГрупа {i}:")
    for address, _ in final_entities:
        if address in group:
            print(f" - {address}")
