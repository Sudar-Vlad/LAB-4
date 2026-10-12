import re
from collections import Counter

# === Функції для базових операцій з рядками ===

def find_substring(text, substring):
    """
    Повертає індекс першого входження або -1, якщо підрядок не знайдено.
    """
    return text.find(substring)

def replace_substring(text, old, new):
    """
    Заміна підрядка в тексті.
    """
    return text.replace(old, new)

def split_text(text, delimiter=' '):
    """
    Розділення тексту за роздільником.
    """
    return text.split(delimiter)

def format_string_f(name, age):
    """
    Форматування рядка з використанням f-string.
    """
    return f"Мене звати {name} і мені {age} років."

def format_string_method(name, age):
    """
    Форматування рядка з використанням методу .format().
    """
    return "Мене звати {} і мені {} років.".format(name, age)

# === Функції для роботи з регулярними виразами ===

def extract_emails(text):
    """
    Витяг email адрес з тексту.
    """
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    return re.findall(pattern, text)

def validate_phone_number(number):
    """
    Валідація українського телефонного номера.
    Формат: +380xxxxxxxxx
    """
    return re.fullmatch(r'\+380\d{9}', number) is not None

def extract_hashtags(text):
    """
    Витяг хештегів з тексту.
    """
    pattern = r'(?<!\w)#[^\W\d_][\w]*'
    return re.findall(pattern, text, flags=re.UNICODE)

def extract_mentions(text):
    """
    Витяг згадувань користувачів з тексту (напр. @user).
    """
    pattern = r'(?<!\w)@[A-Za-zА-Яа-яІіЇїЄєҐґ0-9_]+'
    return re.findall(pattern, text, flags=re.UNICODE)

# === Функції для аналізу тексту ===

def count_words(text):
    """
    Підрахунок кількості слів у тексті.
    """
    pattern = r"[A-Za-zА-Яа-яІіЇїЄєҐґ0-9]+(?:['’\-][A-Za-zА-Яа-яІіЇїЄєҐґ0-9]+)*"
    return len(re.findall(pattern, text, flags=re.UNICODE))

def count_sentences(text):
    """
    Підрахунок кількості речень у тексті.
    """
    return len(re.findall(r'[^.!?…]+[.!?…]+', text))

def word_frequency(text):
    """
    Підрахунок частоти слів у тексті.
    Повертає об'єкт Counter.
    """
    pattern = r"[A-Za-zА-Яа-яІіЇїЄєҐґ0-9]+(?:['’\-][A-Za-zА-Яа-яІіЇїЄєҐґ0-9]+)*"
    words = re.findall(pattern, text, flags=re.UNICODE)
    return Counter(word.lower() for word in words)

def analyze_text(text):
    """
    Комплексний аналіз тексту.
    Повертає словник з результатами аналізу.
    """
    """Виконує комплексний аналіз тексту."""
    frequencies = word_frequency(text)

    return {
        'word_count': count_words(text),
        'sentence_count': count_sentences(text),
        'word_frequency': frequencies.most_common(10),
        'emails': extract_emails(text),
        'hashtags': extract_hashtags(text),
        'mentions': extract_mentions(text),
        'crypto_rate': extract_variant_data(
            text,
            r'\b1\s*NTC\s*=\s*\d+(?:[.,]\d+)?\s*USD\b'
        )
    }

def format_analysis_results(results):
    """
    Форматування результатів аналізу для зручного виведення.
    """
    output = "Результати аналізу тексту:\n"
    output += f"Кількість слів: {results['word_count']}\n"
    output += f"Кількість речень: {results['sentence_count']}\n"

    output += "10 найчастіших слів:\n"
    if results['word_frequency']:
        for word, count in results['word_frequency']:
            output += f"  {word}: {count}\n"
    else:
        output += "  Не знайдено\n"

    output += f"Email-адреси: {', '.join(results['emails']) or 'не знайдено'}\n"
    output += f"Хештеги: {', '.join(results['hashtags']) or 'не знайдено'}\n"
    output += f"Згадування: {', '.join(results['mentions']) or 'не знайдено'}\n"
    output += (
        "Курс криптовалюти до USD: "
        f"{', '.join(results['crypto_rate']) or 'не знайдено'}"
    )

    return output

# === Функція для вилучення даних за варіантом ===

def extract_variant_data(text, variant_pattern):
    """
    Вилучає дані з тексту за допомогою патерну, специфічного для варіанту.
    """
    return re.findall(variant_pattern, text, flags=re.IGNORECASE)

# === Головна частина програми ===

def read_file_content(filepath):
    """
    Читає вміст файлу.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Помилка: Файл не знайдено за шляхом {filepath}")
        return None

def main():
    """
    Головна функція, що керує виконанням програми.
    """
    print("Ласкаво просимо до аналізатора тексту!")

    # Шлях до файлу з текстом
    text_filepath = r'C:\Users\Admin\PycharmProjects\src\data\neoterra_text.txt'

    # Читання тексту з файлу
    text_to_analyze = read_file_content(text_filepath)
    if not text_to_analyze:
        return # Завершити, якщо файл не прочитано

    while True:
        try:
            print("\nОберіть опцію:")
            print("1. Аналіз тексту 'NeoTerra 3000'")
            print("2. Валідація телефонного номера")
            print("3. Вилучення даних за варіантом")
            print("4. Вихід")
            choice = input("Ваш вибір: ")

            if choice == '1':
                results = analyze_text(text_to_analyze)
                print(format_analysis_results(results))

            elif choice == '2':
                phone = input("Введіть номер телефону для валідації: ")
                if validate_phone_number(phone):
                    print("Номер телефону валідний.")
                else:
                    print("Номер телефону невалідний.")

            elif choice == '3':
                pattern = r'\b1\s*NTC\s*=\s*\d+(?:[.,]\d+)?\s*USD\b'
                variant_data = extract_variant_data(text_to_analyze, pattern)

                if variant_data:
                    print(f"Знайдений курс криптовалюти до USD: {variant_data[0]}")
                else:
                    print("Курс криптовалюти до USD не знайдено.")

            elif choice == '4':
                print("Дякуємо за використання аналізатора!")
                break

            else:
                print("Невірний вибір. Спробуйте ще раз.")

        except Exception as e:
            print(f"Виникла помилка: {e}")

if __name__ == '__main__':
    main()
