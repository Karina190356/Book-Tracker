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
     
     def test_validation_correct_book_saves_successfully(self):
      """Тест сохранения корректной книги."""
      init_data_file(TEST_DATA_FILE) 
      
      valid_book   = {"id": 1234567890123456789012345678901234567892,
                     "title": "Test Book",
                     "author": "Test Author",
                     "genre": "Test",
                     "pages": 1} 
      
      save_books([valid_book], custom_path=TEST_DATA_FILE) 
      loaded_after_valid_attempt = load_books(custom_path=TEST_DATA_FILE) 
      
      self.assertEqual(len(loaded_after_valid_attempt), 1) 
      self.assertDictEqual(loaded_after_valid_attempt[0], valid_book) 
     
     def test_validation_missing_field_raises_error(self):
      """Тест валидации: отсутствие обязательного поля вызывает исключение."""
      from data_manager import validate_book_data 
      
      invalid_book_missing_title = {"id": 1,
                                   "author": "Test Author",
                                   "genre": "Test",
                                   "pages": 1}
                                   
      with self.assertRaises(ValueError) as context:
           validate_book_data(invalid_book_missing_title) 
      self.assertIn("Отсутствует обязательное поле", str(context.exception)) 
     
     def test_validation_wrong_type_id_raises_error(self):
      """Тест валидации: неправильный тип поля id вызывает исключение."""
      from data_manager import validate_book_data 
      
      invalid_book_wrong_id_type = {"id": "not_an_int",
                                    "title": "Test Book",
                                    "author": "Test Author",
                                    "genre": "Test",
                                    "pages": 1}
                                    
      with self.assertRaises(TypeError) as context:
           validate_book_data(invalid_book_wrong_id_type) 
      self.assertIn("должно быть целым числом", str(context.exception)) 
     
     def test_validation_negative_pages_raises_error(self):
      """Тест валидации: отрицательное количество страниц вызывает исключение."""
      from data_manager import validate_book_data 
      
      invalid_book_negative_pages_1 = {"id": 1,
                                      "title": "Test Book",
                                      "author": "Test Author",
                                      "genre": "Test",
                                      "pages": -1} 
                                      
      invalid_book_negative_pages_2 = {"id": 1,
                                      "title": "Test Book",
                                      "author": "Test Author",
                                      "genre": "Test",
                                      "pages": 0} 
                                      
      with self.assertRaises(ValueError) as context_1:
           validate_book_data(invalid_book_negative_pages_1) 
           
      with self.assertRaises(ValueError) as context_2:
           validate_book_data(invalid_book_negative_pages_2) 
           
      err_msg_1_expected_part = "должно быть положительным числом"
      err_msg_2_expected_part = err_msg_1_expected_part 
      
      err_msg_1_actual_part_found_in_error_msg_1 = err_msg_1_expected_part in str(context_1.exception) 
      err_msg_2_actual_part_found_in_error_msg_2 = err_msg_2_expected_part in str(context_2.exception) 
      
      assert err_msg_1_actual_part_found_in_error_msg_1 and err_msg_2_actual_part_found_in_error_msg_2
