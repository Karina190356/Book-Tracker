import json
import os

# Переменная для пути к папке с данными (согласовано с README)
DATA_DIR_DEFAULT = 'data'
DATA_FILE_DEFAULT_NAME = 'books.json'

def _get_data_path():
    """
    Возвращает полный путь к файлу данных.
    Приоритет: Переменная окружения -> Значение по умолчанию.
    """
    env_path = os.getenv('BOOKS_DATA_PATH')
    if env_path:
        return env_path
    
    os.makedirs(DATA_DIR_DEFAULT, exist_ok=True) # Создаем папку по умолчанию при необходимости
    return os.path.join(DATA_DIR_DEFAULT, DATA_FILE_DEFAULT_NAME)

def init_data_file(custom_path=None):
    """
    Создает файл данных и директорию (если их нет).
    Позволяет указать кастомный путь для тестов.
    Обрабатывает ошибки файловой системы.
    """
    path_to_use = custom_path if custom_path is not None else _get_data_path()
    
    dir_name = os.path.dirname(path_to_use)
    
    try:
        os.makedirs(dir_name, exist_ok=True)
        
        if not os.path.exists(path_to_use):
            with open(path_to_use, 'w', encoding='utf-8') as f:
                json.dump([], f)
                
    except OSError as e: # Обрабатываем любые ошибки ОС (разрешения диска и т.д.)
        print(f"Ошибка файловой системы при инициализации ({path_to_use}): {e}")

def load_books(custom_path=None) -> list:
    """
    Загружает список книг из JSON-файла.
    Обеспечивает обработку ошибок чтения/декодирования JSON.
    Возвращает пустой список при любой ошибке.
    """
    path_to_use = custom_path if custom_path is not None else _get_data_path()
    
    try:
        with open(path_to_use, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    except FileNotFoundError:
        print(f"Файл данных не найден по пути {path_to_use}. Будет создан при первом сохранении.")
        return []
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON в файле {path_to_use}: {e}. Файл может быть поврежден.")
        return []
    except PermissionError as e:
        print(f"Нет прав на чтение файла {path_to_use}: {e}")
        return []
    except OSError as e: # Обрабатываем любые ошибки ОС при чтении
        print(f"Ошибка чтения файла {path_to_use}: {e}")
        return []

def validate_book_data(book: dict):
     """
     Валидирует структуру и типы данных одной книги.
     Генерирует исключение ValueError или TypeError при некорректных данных.
     """
     required_fields = ['id', 'title', 'author', 'genre', 'pages']
     for field in required_fields:
         if field not in book:
             raise ValueError(f"Отсутствует обязательное поле '{field}' в объекте книги.")
     
     if not isinstance(book['id'], int):
         raise TypeError(f"Поле 'id' должно быть целым числом (int), а не {type(book['id']).__name__}.")
     
     for field in ['title', 'author', 'genre']:
         value = book[field]
         if not isinstance(value, str) or len(value.strip()) == 0:
             raise ValueError(f"Поле '{field}' должно быть непустой строкой.")
     
     pages = book['pages']
     if not isinstance(pages, int):
         raise TypeError(f"Поле 'pages' должно быть целым числом (int), а не {type(pages).__name__}.")
     if pages <= 0:
         raise ValueError(f"Поле 'pages' должно быть положительным числом (> 0), получено {pages}.")

def save_books(books: list, custom_path=None):
     """
     Сохраняет список книг в JSON-файл.
     Валидирует каждый объект перед сохранением.
     Обеспечивает обработку ошибок записи/кодирования JSON.
     """
     path_to_use = custom_path if custom_path is not None else _get_data_path()
     
     # Валидация данных ПЕРЕД записью в файл
     for book in books:
         validate_book_data(book) 
     
     try:
          with open(path_to_use, 'w', encoding='utf-8') as f:
              json.dump(books, f, ensure_ascii=False, indent=2)
              
          print(f"Данные успешно сохранены в {path_to_use}")
          
      except PermissionError as e:
          print(f"Ошибка: Нет прав на запись в файл {path_to_use}. Проверьте права доступа.")
          raise # Пробрасываем ошибку дальше в main.py для показа пользователю
      except TypeError as e: # Ошибка сериализации объекта в JSON (не должна возникнуть из-за валидации)
          print(f"Ошибка кодирования объектов в JSON: {e}. Объект не может быть сериализован.")
          raise
      except OSError as e: # Ошибки ввода-вывода (например диск переполнен или защищен от записи)
          print(f"Ошибка ввода-вывода при сохранении в {path_to_use}: {e}")
          raise

def generate_unique_id(existing_books: list) -> int:
      """
      Генерирует уникальный ID для новой книги.
      """
      if not existing_books:
          return 1
      return max(book['id'] for book in existing_books) + 1
