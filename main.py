import os
import tkinter as tk
from tkinter import ttk, messagebox

# Попытка импортировать ttkthemes. Если не получится, используем стандартный ttk.
try:
    import ttkthemes as themes
    THEMES_AVAILABLE = True
except ImportError:
    print("Библиотека ttkthemes не найдена. Используется стандартный стиль Tk.")
    THEMES_AVAILABLE = False

from data_manager import load_books, save_books, init_data_file, generate_unique_id

class BookTrackerApp:
    def __init__(self, root):
        # Используем тему из ttkthemes, если она доступна
        if THEMES_AVAILABLE:
            self.root = themes.ThemedTk()
            self.root.get_themes()  # Получаем список тем
            self.root.set_theme("arc")  # Устанавливаем тему "arc"
        else:
            self.root = root

        self.root.title("Book Tracker: Учёт прочитанных книг")
        self.root.geometry("800x500")
        
        # Инициализация данных
        init_data_file()
        self.books = load_books()
        self.filtered_books = self.books.copy()
        
        self.create_widgets()
        self.update_treeview()
    
    def create_widgets(self):
        """
        Метод для создания всех виджетов GUI.
        Все строки внутри метода имеют одинаковый уровень отступа.
        """
        # --- Фрейм ввода данных ---
        input_frame = ttk.LabelFrame(self.root, text="Добавить новую книгу")
        input_frame.pack(pady=10, fill='x', padx=10)
        
        # Название книги
        ttk.Label(input_frame, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(input_frame, textvariable=self.title_var, width=40)
        self.title_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5)
        
        # Автор
        ttk.Label(input_frame, text="Автор:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.author_var = tk.StringVar()
        self.author_entry = ttk.Entry(input_frame, textvariable=self.author_var, width=40)
        self.author_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5)
        
        # Жанр
        ttk.Label(input_frame, text="Жанр:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.genre_var = tk.StringVar()
        self.genre_entry = ttk.Entry(input_frame, textvariable=self.genre_var)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Количество страниц
        ttk.Label(input_frame, text="Страниц:").grid(row=2, column=2, padx=5, pady=5)
        self.pages_var = tk.StringVar()
        self.pages_entry = ttk.Entry(input_frame, textvariable=self.pages_var, width=8)
        self.pages_entry.grid(row=2, column=3, padx=5, pady=5)
        
        # Кнопка добавления
        self.add_btn = ttk.Button(input_frame, text="Добавить книгу", command=self.add_book)
        self.add_btn.grid(row=3, column=0, columnspan=4, pady=15)
        
        # --- Фрейм фильтрации ---
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация")
        filter_frame.pack(pady=10, fill='x', padx=10)
        
         # Фильтр по жанру
         ttk.Label(filter_frame, text="Жанр:").grid(row=0, column=0, padx=5)
         self.filter_genre_var = tk.StringVar()
         self.filter_genre_entry = ttk.Entry(filter_frame, textvariable=self.filter_genre_var)
         self.filter_genre_entry.grid(row=0, column=1, padx=5)
         
         # Фильтр по страницам (больше чем...)
         ttk.Label(filter_frame, text="Страниц >").grid(row=0, column=2)
         self.filter_pages_var = tk.StringVar()
         self.filter_pages_entry = ttk.Entry(filter_frame, textvariable=self.filter_pages_var)
         self.filter_pages_entry.grid(row=0, column=3)
         
         self.filter_btn = ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
         self.filter_btn.grid(row=0, column=4, padx=10)
         
         # Кнопка сброса фильтра
         self.reset_btn = ttk.Button(filter_frame, text="Сбросить", command=self.reset_filter)
         self.reset_btn.grid(row=0, column=5)
         
         # --- Таблица с книгами ---
         columns = ("id", "title", "author", "genre", "pages")
         
         self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
         
          # Настройка ширины колонок и заголовков
          self.tree.column("id", width=30)
          self.tree.column("title", width=200)
          self.tree.column("author", width=150)
          self.tree.column("genre", width=100)
          self.tree.column("pages", width=80)
          
          self.tree.heading("id", text="ID")
          self.tree.heading("title", text="Название")
          self.tree.heading("author", text="Автор")
          self.tree.heading("genre", text="Жанр")
          self.tree.heading("pages", text="Страниц")
          
          self.tree.pack(fill='both', expand=True, padx=10)
    
    def add_book(self):
       """Обрабатывает добавление новой книги с валидацией."""
       title = self.title_var.get().strip()
       author = self.author_var.get().strip()
       genre = self.genre_var.get().strip()
       
       pages_str = self.pages_var.get().strip()
       
       if not title or not author or not genre or not pages_str:
           messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
           return
       
       try:
           pages = int(pages_str)
           if pages <= 0:
               raise ValueError("Количество страниц должно быть положительным.")
       except ValueError as e:
           messagebox.showerror("Ошибка", str(e))
           return

       try:
           new_id = generate_unique_id(self.books)
           new_book = {
               "id": new_id,
               "title": title,
               "author": author,
               "genre": genre,
               "pages": pages
           }
           
           self.books.append(new_book)
           save_books(self.books) 
           self.update_treeview() 

           for var in [self.title_var, self.author_var, self.genre_var, self.pages_var]:
               var.set("")
           
           messagebox.showinfo("Успех", "Книга добавлена!")
       except Exception as e:
           messagebox.showerror("Критическая ошибка", f"Не удалось сохранить книгу: {e}")
    
    def update_treeview(self):
       """Обновляет данные в таблице Treeview."""
       for i in self.tree.get_children():
           self.tree.delete(i)
       
       for book in (self.filtered_books if hasattr(self, 'filtered_books') else self.books):
           self.tree.insert("", 'end', values=(book['id'], book['title'], book['author'], book['genre'], book['pages']))
    
    def apply_filter(self):
       """Применяет фильтры по жанру и количеству страниц."""
       filter_genre = self.filter_genre_var.get().lower()
       filter_pages_str = self.filter_pages_var.get()
       
       filtered_books = []
       
       for book in self.books:
           match_genre = filter_genre in book['genre'].lower() if filter_genre else True
           
           match_pages = True
           if filter_pages_str:
               try:
                   filter_pages_val = int(filter_pages_str)
                   match_pages = book['pages'] > filter_pages_val
               except ValueError:
                   messagebox.showerror("Ошибка", "В фильтре страниц введите целое число.")
                   return

           if match_genre and match_pages:
               filtered_books.append(book)
       
       self.filtered_books = filtered_books
       self.update_treeview()
    
    def reset_filter(self):
       """Сбрасывает фильтр и показывает все книги."""
       self.filtered_books = self.books.copy()
       for var in [self.filter_genre_var, self.filter_pages_var]:
           var.set("")
       self.update_treeview()

# --- Точка входа ---
if __name__ == "__main__":
    try:
        if 'THEMES_AVAILABLE' in globals() and THEMES_AVAILABLE:
            root = themes.ThemedTk()
            app = BookTrackerApp(root)  # Передаем уже созданный root
            root.mainloop()
        else:
            root = tk.Tk()  # Если нет — обычный Tk.
            app = BookTrackerApp(root)  # Передаем уже созданный root
            root.mainloop()
    except NameError:
        root = tk.Tk()
        app = BookTrackerApp(root)
        root.mainloop()
