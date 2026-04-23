import unittest
import os
import json
import shutil
from data_manager import load_books, save_books, init_data_file

# Путь к тестовому файлу данных (в отдельной папке tests/data_test)
TEST_DATA_DIR = 'tests/data_test'
TEST_DATA_FILE = os.path.join(TEST_DATA_DIR, 'test_books.json')
DATA_DIR_ORIG = 'data' # Оригинальная папка данных приложения

class TestDataManager(unittest.TestCase):
     @classmethod
     def setUpClass(cls):
          """Создает тестовую директорию перед всеми тестами."""
          os.makedirs(TEST_DATA_DIR, exist_ok=True)
          
     @classmethod
     def tearDownClass(cls):
          """Удаляет тестовую директорию после всех тестов."""
          shutil.rmtree(TEST_DATA_DIR)
          
     def setUp(self):
          """Подготавливает окружение перед каждым тестом."""
          # Если папка данных приложения существует (например от предыдущих запусков), переименуем её,
          # чтобы тесты не портили реальные данные пользователя.
          if os.path.exists(DATA_DIR_ORIG):
              shutil.move(DATA_DIR_ORIG, DATA_DIR_ORIG + '_backup')
              
     def tearDown(self):
          """Восстанавливает окружение после каждого теста."""
          # Удаляем тестовый файл после теста (если он был создан)
          if os.path.exists(TEST_DATA_FILE):
              os.remove(TEST_DATA_FILE)
              
          # Восстанавливаем оригинальную папку данных приложения из бэкапа (если она была)
          backup_dir = DATA_DIR_ORIG + '_backup'
          if os.path.exists(backup_dir):
              shutil.move(backup_dir, DATA_DIR_ORIG)
    
     def test_load_and_save_empty_list(self):
          """Тест загрузки и сохранения пустого списка."""
          init_data_file(TEST_DATA_FILE) # Инициализация файла для теста
          
          save_books([], custom_path=TEST_DATA_FILE)
          loaded_books = load_books(custom_path=TEST_DATA_FILE)
          
          self.assertEqual(loaded_books, [])
     
     def test_load_and_save_single_book(self):
          """Тест сохранения и загрузки одной книги."""
          init_data_file(TEST_DATA_FILE) # Инициализация файла для теста

          test_book = {"id": 1234567890123456789012345678901234567890,
                       "title": "Test Book",
                       "author": "Test Author",
                       "genre": "Test",
                       "pages": 100}
          
          save_books([test_book], custom_path=TEST_DATA_FILE)
          loaded_books = load_books(custom_path=TEST_DATA_FILE)
          
          self.assertEqual(len(loaded_books), 1)
          self.assertDictEqual(loaded_books[0], test_book) 
     
     def test_generate_unique_id_empty_list(self):
          """Генерация ID для первого элемента в пустом списке."""
          books = []
          
          from data_manager import generate_unique_id # Импортируем функцию для теста
          
          new_id = generate_unique_id(books) 
          
          self.assertEqual(new_id, 1) 
     
     def test_generate_unique_id_non_empty_list(self):
          """Генерация уникального ID на основе существующего списка."""
          books = [
              {"id": 1},
              {"id": 5},
              {"id": 3}
          ]
          
          from data_manager import generate_unique_id
          
          new_id = generate_unique_id(books)
          
          self.assertEqual(new_id, 6) 
     
     def test_validation_negative_pages_raises_error(self):
      """Юнит-тест для проверки валидации количества страниц (должно быть > 0)."""
      init_data_file(TEST_DATA_FILE) 
      
      invalid_book_1 = {"id": 1234567890123456789012345678901234567890,
                        "title": "Test Book",
                        "author": "Test Author",
                        "genre": "Test",
                        "pages": -1} # Отрицательное число!
      
      invalid_book_2 = {"id": 1234567890123456789012345678901234567891,
                        "title": "Test Book",
                        "author": "Test Author",
                        "genre": "Test",
                        "pages": 0} # Ноль!
      
      valid_book   = {"id": 1234567890123456789012345678901234567892,
                     "title": "Test Book",
                     "author": "Test Author",
                     "genre": "Test",
                     "pages": 1} # Корректное значение

      save_books([valid_book], custom_path=TEST_DATA_FILE) 
      loaded_books_1_valid_only = load_books(custom_path=TEST_DATA_FILE) 
      self.assertEqual(len(loaded_books_1_valid_only), 1) 
      
      try:
           save_books([invalid_book_1], custom_path=TEST_DATA_FILE) 
      except Exception as e: 
           pass 
      loaded_after_invalid_1_attempt = load_books(custom_path=TEST_DATA_FILE) 
      self.assertEqual(len(loaded_after_invalid_1_attempt), 1) 
      
      try: 
           save_books([invalid_book_2], custom_path=TEST_DATA_FILE) 
      except Exception as e: 
           pass 
      loaded_after_invalid_2_attempt = load_books(custom_path=TEST_DATA_FILE) 
      self.assertEqual(len(loaded_after_invalid_2_attempt), 1)
