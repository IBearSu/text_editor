from text_editor_project.models.MyString import MyString
from text_editor_project.models.cursor import Cursor
from text_editor_project.models.helpers import *
from text_editor_project.views.curses_view import Subscriber

from abc import ABC, abstractmethod

class Publisher(ABC):
    @abstractmethod
    def add_subscriber(self, view_subscriber):
        """
        Добавляет подписчика (представление).
        """
        pass

    @abstractmethod
    def remove_subscriber(self, subscriber):
        """
        Удаляет подписчика.
        """
        pass

    @abstractmethod
    def notify_subscribers(self):
        """
        Уведомляет всех подписчиков об изменении данных.
        """
        pass

class ITextModel(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def add_new_line(self, line_index, content=""):
        pass

    @abstractmethod
    def append_line(self, content=""):
        """
        Кодирует текст в cp1251, а потом
        добавляет строку в конец текста.
        :param content: Содержимое строки.
        """
        pass

    @abstractmethod
    def append_line_without_notifications(self, content=""):
        """
        Кодирует текст в cp1251, а потом
        добавляет строку в конец текста.
        :param content: Содержимое строки.
        """
        pass

    @abstractmethod
    def append_help_line_without_notifications(self, content=""):
        """
        Кодирует текст в cp1251, а потом
        добавляет строку в конец текста.
        :param content: Содержимое строки.
        """
        pass

    @abstractmethod
    def get_all_lines(self):
        """
        Возвращает все объекты строки как список объектов строк (MyString).
        :return: Список строк.
        """
        pass

    @abstractmethod
    def insert_char(self, line_index, char_index, char_to_insert):
        """
        Вставляет символ по номеру строки и индексу.
        Если строки по индексу нет, она создается.

        :param line_index: Индекс строки.
        :param char_index: Индекс символа в строке.
        :param char_to_insert: Символ для вставки.
        :return: None
        """
        pass

    @abstractmethod
    def insert_text(self, line_index, char_index, text):
        """
        Кодирует текст в cp1251, а потом вставляет текст в указанное место строки.
        :param line_index: Индекс строки.
        :param char_index: Индекс символа в строке.
        :param text: Текст для вставки.
        """
        pass

    @abstractmethod
    def insert_text_without_notifications(self, line_index, char_index, text):
        """
        Кодирует текст в cp1251, а потом вставляет текст в указанное место строки.
        :param line_index: Индекс строки.
        :param char_index: Индекс символа в строке.
        :param text: Текст для вставки.
        """
        # Преобразуем каждый символ в кодировку cp1251 и вставляем по очереди
        pass

    @abstractmethod
    def delete_all_text_on_the_line(self, the_line_index):
        """
        Удаляет весь текст из строки.
        :param the_line_index: Индекс строки.
        """
        pass

    @abstractmethod
    def find_text(self, query, start_line=0, start_char=0):
        """
        Ищет текст в документе.
        :param query: Строка для поиска.
        :param start_line: Начальный индекс строки для поиска.
        :param start_char: Начальный индекс символа в строке для поиска.
        :return: (line_index, char_index) или None, если не найдено.
        """
        pass

    @abstractmethod
    def clear(self):
        """
        Очищает весь текст.
        """
        pass

    @abstractmethod
    def find_next_word(self, line_index, current_pos):
        """Найти начало следующего слова после текущей позиции в текущей или следующей строке"""
        pass

    @abstractmethod
    def find_previous_word(self, line_index, current_pos):
        """Найти начало предыдущего слова до текущей позиции в текущей или предыдущей строке"""
        pass

    @abstractmethod
    def delete_word_at_position(self, line_index, current_pos):
        pass

    @abstractmethod
    def delete_key_at_position(self, x, y):
        pass

    @abstractmethod
    def save_to_file(self, filename):
        """
        Сохраняет содержимое lines в текстовый файл.
        :param filename: Имя файла для сохранения.
        """
        pass

    @abstractmethod
    def load_help_file(self, help_filename = "help.txt"):
        pass

    @abstractmethod
    def load_from_file(self, filename):
        """
        Загружает содержимое текстового файла в lines, добавляя символ конца файла в конец последней строки.
        :param filename: Имя файла для загрузки.
        """
        pass

class TextModel(ITextModel, Publisher):
    def __init__(self):
        """
        Инициализация текстовой модели.
        Хранит текст в виде списка объектов MyString.
        """
        self.cursor = Cursor()
        self.lines = []  # Список строк текста (MyString)
        self.view_subscribers : Subscriber
        self.view_subscribers = [] # Список подписчиков (паттерн Pub-Sub)
        self.controller_state_str = ""
        self.opened_file = ""
        self.is_modified = False
        self.help_lines = []
        self.temp_buff = []

    def get_lines(self):
        return self.lines

    def get_help_lines(self):
        return self.help_lines

    def set_lines(self, lines):
        self.lines = lines

    def get_cursor(self):
        return self.cursor

    def get_opened_filename(self):
        return self.opened_file

    def get_cursor_x(self):
        return self.cursor.x_position

    def get_cursor_y(self):
        return self.cursor.y_position

    def set_cursor_x(self, x):
        self.cursor.x_position = x

    def set_cursor_y(self, y):
        self.cursor.y_position = y

    def get_view_subscribers(self):
        return self.view_subscribers

    def get_controller_state_str(self):
        return self.controller_state_str

    def set_controller_state_str(self, state):
        self.controller_state_str = state

    def get_is_modified(self):
        return self.is_modified

    def set_is_modified(self):
        self.is_modified = True

    def unset_is_modified(self):
        self.is_modified = False

    def get_temp_buff(self):
        return self.temp_buff

    def set_temp_buff(self, buff):
        self.temp_buff = buff

    def add_subscriber(self, view_subscriber : Subscriber):
        """
        Добавляет подписчика (представление).
        """
        if view_subscriber not in self.view_subscribers:
            self.view_subscribers.append(view_subscriber)

    def remove_subscriber(self, subscriber : Subscriber):
        """
        Удаляет подписчика.
        """
        if subscriber in self.view_subscribers:
            self.view_subscribers.remove(subscriber)

    def notify_subscribers(self):
        """
        Уведомляет всех подписчиков об изменении данных.
        """
        for view_subscriber in self.view_subscribers:
            view_subscriber.update(self)

    def add_new_line(self, line_index, content=""):
        encoded_content = encode_to_cp1251(content, encoding='cp1251')
        self.lines.insert(line_index, MyString(encoded_content))
        self.notify_subscribers()  # Уведомляем подписчиков об изменении


    def append_line(self, content=""):
        """
        Кодирует текст в cp1251, а потом
        добавляет строку в конец текста.
        :param content: Содержимое строки.
        """
        encoded_content = encode_to_cp1251(content, encoding='cp1251')
        self.lines.append(MyString(encoded_content))
        self.notify_subscribers()  # Уведомляем подписчиков об изменении

    def append_line_without_notifications(self, content=""):
        """
        Кодирует текст в cp1251, а потом
        добавляет строку в конец текста.
        :param content: Содержимое строки.
        """
        encoded_content = encode_to_cp1251(content, encoding='cp1251')
        self.lines.append(MyString(encoded_content))

    def append_help_line_without_notifications(self, content=""):
        """
        Кодирует текст в cp1251, а потом
        добавляет строку в конец текста.
        :param content: Содержимое строки.
        """
        encoded_content = encode_to_cp1251(content, encoding='cp1251')
        self.help_lines.append(MyString(encoded_content))


    def get_all_lines(self):
        """
        Возвращает все объекты строки как список объектов строк (MyString).
        :return: Список строк.
        """
        return [line for line in self.lines]

    def insert_char(self, line_index, char_index, char_to_insert):
        """
        Вставляет символ по номеру строки и индексу.
        Если строки по индексу нет, она создается.

        :param line_index: Индекс строки.
        :param char_index: Индекс символа в строке.
        :param char_to_insert: Символ для вставки.
        :return: None
        """
        # Удостоверимся, что список строк достаточно длинный
        while len(self.lines) <= line_index:  # Пока длина списка меньше индекса строки
            self.lines.append(MyString())  # Добавляем новые строки в список

        # Кодируем символ для вставки
        if isinstance(char_to_insert, int):
            char_to_insert_str = chr(char_to_insert)
        else:
            char_to_insert_str = char_to_insert
        encoded_text_to_insert = encode_to_cp1251(char_to_insert_str, encoding='cp1251')

        # Вставляем символ в строку на нужную позицию
        self.lines[line_index].insert(char_index, encoded_text_to_insert)

    def insert_text(self, line_index, char_index, text):
        """
        Кодирует текст в cp1251, а потом вставляет текст в указанное место строки.
        :param line_index: Индекс строки.
        :param char_index: Индекс символа в строке.
        :param text: Текст для вставки.
        """
        # Преобразуем каждый символ в кодировку cp1251 и вставляем по очереди
        text = decode_from_cp1251(text)
        for char_to_insert in text:
            # Вставляем символ в строку на нужную позицию
            self.insert_char(line_index, char_index, char_to_insert)
            # После вставки одного символа, индекс символа в строке увеличивается на 1
            char_index += 1
        self.notify_subscribers()  # Уведомляем подписчиков об изменении

    def insert_text_without_notifications(self, line_index, char_index, text):
        """
        Кодирует текст в cp1251, а потом вставляет текст в указанное место строки.
        :param line_index: Индекс строки.
        :param char_index: Индекс символа в строке.
        :param text: Текст для вставки.
        """
        # Преобразуем каждый символ в кодировку cp1251 и вставляем по очереди
        text = decode_from_cp1251(text)
        for char_to_insert in text:
            # Вставляем символ в строку на нужную позицию
            self.insert_char(line_index, char_index, char_to_insert)
            # После вставки одного символа, индекс символа в строке увеличивается на 1
            char_index += 1

    def delete_all_text_on_the_line(self, the_line_index):
        """
        Удаляет весь текст из строки.
        :param the_line_index: Индекс строки.
        """
        line = self.lines[the_line_index]
        line.clear()
        line.append("\n")
        self.notify_subscribers()  # Уведомляем подписчиков об изменении

    def find_text(self, query, start_line=0, start_char=0):
        """
        Ищет текст в документе.
        :param query: Строка для поиска.
        :param start_line: Начальный индекс строки для поиска.
        :param start_char: Начальный индекс символа в строке для поиска.
        :return: (line_index, char_index) или None, если не найдено.
        """
        for line_index in range(start_line, len(self.lines)):
            start_index = start_char if line_index == start_line else 0
            position = self.lines[line_index].find(query, start_index)
            if position != -1:
                return line_index, position
        return None

    def clear(self):
        """
        Очищает весь текст.
        """
        self.lines.clear()
        self.notify_subscribers()  # Уведомляем подписчиков об изменении

    def find_next_word(self, line_index, current_pos):
        """Найти начало следующего слова после текущей позиции в текущей или следующей строке"""
        # Ищем в текущей строке
        started_search_on_space_or_tabulation = False
        line = self.lines[line_index]

        # Пропускаем пробелы до слова
        while current_pos < line.length() and line[current_pos] in "    \n\t":
            current_pos += 1
            started_search_on_space_or_tabulation = True

        # Ищем конец слова
        if not started_search_on_space_or_tabulation:
            while current_pos < line.length() and line[current_pos] not in "    \n\t":
                current_pos += 1

        # Пропускаем пробелы после слова
        while current_pos < line.length() and line[current_pos] in "    \n\t":
            current_pos += 1

        # Если в текущей строке больше нет слов, переходим к следующей строке
        if current_pos == line.length() and line_index < len(self.lines) - 1:
            line_index += 1
            current_pos = 0
            line = self.lines[line_index]
            # Пропускаем пустые строки
            while line_index < len(self.lines) and self.lines[line_index].length() == 1:
                line_index += 1
                line = self.lines[line_index]
            while current_pos < self.lines[line_index].length() and line[current_pos] in "    \n\t":
                current_pos += 1

        return current_pos, line_index

    def find_previous_word(self, line_index, current_pos):
        """Найти начало предыдущего слова до текущей позиции в текущей или предыдущей строке"""
        line = self.lines[line_index]
        found_word = False
        # Пропускаем пробелы до слова
        while current_pos > 0 and line[current_pos - 1] in "    \n\t":
            current_pos -= 1

        # Ищем начало слова
        while current_pos > 0 and line[current_pos - 1] not in "    \n\t":
            current_pos -= 1
            found_word = True

        while not found_word and line_index > 0:
            line_index -= 1
            line = self.lines[line_index]
            current_pos = self.lines[line_index].length()
            while current_pos > 0 and line[current_pos - 1] in "    \n\t":
                current_pos -= 1

            # Ищем начало слова
            while current_pos > 0 and line[current_pos - 1] not in "    \n\t":
                current_pos -= 1
                found_word = True

        return current_pos, line_index

    def delete_word_at_position(self, line_index, current_pos):
        line = self.lines[line_index]
        if line[current_pos] not in " ":
            while current_pos > 0 and line[current_pos - 1] not in "    \n\t":
                current_pos -= 1
            while line[current_pos] not in "    \n\t":
                self.delete_key_at_position(current_pos, line_index)
            if line[current_pos] in " ":
                self.delete_key_at_position(current_pos, line_index)
            self.cursor.x_position = current_pos

    def delete_key_at_position(self, x, y):
        if 0 <= x < self.lines[y].length():
            self.lines[y].erase(x, 1)
            self.lines[y].shrink_to_fit()

    def save_to_file(self, filename):
        """
        Сохраняет содержимое lines в текстовый файл.
        :param filename: Имя файла для сохранения.
        """
        try:
            with open(filename, 'w', encoding='cp1251') as file:
                for line in self.lines:
                    # Преобразуем строку в читаемый текст
                    file.write(decode_from_cp1251(line.c_strb()))
            print(f"Содержимое успешно сохранено в файл: {filename}")
        except Exception as e:
            print(f"Ошибка при сохранении в файл {filename}: {e}")

    def load_help_file(self, help_filename = "help.txt"):
        try:
            with open(help_filename, 'r', encoding='cp1251') as file:
                self.clear()  # Очищаем текущие строки
                lines = file.readlines()
                for line in lines:
                    line = line.replace("\t", "    ")  # Заменяем табуляции на 4 пробела
                    self.append_help_line_without_notifications(line)


            print(f"Содержимое успешно загружено из файла: {help_filename}")
        except Exception as e:
            print(f"Ошибка при загрузке из файла {help_filename}: {e}")

    def load_from_file(self, filename):
        """
        Загружает содержимое текстового файла в lines, добавляя символ конца файла в конец последней строки.
        :param filename: Имя файла для загрузки.
        """
        self.cursor.x_position = 0
        self.cursor.y_position = 0
        self.view_subscribers[0].scroll_offset_x = 0
        self.view_subscribers[0].scroll_offset_y = 0
        try:
            with open(filename, 'r', encoding='cp1251') as file:
                self.clear()  # Очищаем текущие строки
                lines = file.readlines()
                for line in lines:
                    line = line.replace("\t", "    ")  # Заменяем табуляции на 4 пробела
                    self.append_line_without_notifications(line)

                # Добавляем символ конца файла (EOF) к последней строке
            last_line = self.lines[len(self.lines) - 1]
            if last_line.length() == 0:
                self.insert_char(len(self.lines) - 1, last_line.length(), '\n')

            print(f"Содержимое успешно загружено из файла: {filename}")
        except Exception as e:
            print(f"Ошибка при загрузке из файла {filename}: {e}")

