import json
import os

# Переменная для пути к папке с данными (согласовано с README)
DATA_DIR = 'data'
DATA_FILE = os.path.join(DATA_DIR, 'books.json')

def init_data_file():
    """Создает папку и файл данных, если их нет."""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)
    except OSError as e:
        print(f"Ошибка при создании директории/файла данных: {e}")
        raise

def load_books() -> list:
    """Загружает список книг из JSON-файла."""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Если файла нет или он поврежден, возвращаем пустой список
        return []
    except Exception as e:
        print(f"Неизвестная ошибка при чтении файла: {e}")
        return []

def save_books(books: list):
    """
    Сохраняет список книг в JSON-файл.
    Обеспечивает обработку ошибок записи.
    """
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(books, f, ensure_ascii=False, indent=2)
    except PermissionError:
        print("Ошибка: Нет прав на запись в файл. Проверьте права доступа.")
        raise
    except IOError as e:
        print(f"Ошибка ввода-вывода при сохранении: {e}")
        raise

def generate_unique_id(existing_books: list) -> int:
    """
    Генерирует уникальный ID для новой книги.
    Находит максимальный существующий ID и прибавляет 1.
    Если список пуст, возвращает 1.
    """
    if not existing_books:
        return 1
    return max(book['id'] for book in existing_books) + 1
