from text_editor_project.models.command_buffer import CommandBuffer
from text_editor_project.models.helpers import *
from abc import ABC, abstractmethod

class IVAdapter(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def clear_screen(self):
        pass

    @abstractmethod
    def clear_command_window(self):
        pass

    @abstractmethod
    def refresh_screen(self):
        pass

    @abstractmethod
    def display_text(self, y, x, text, color_pair=0):
        pass

    @abstractmethod
    def display_text_on_help_window(self, y, x, text, color_pair=2):
        pass

    @abstractmethod
    def get_key_input(self):
        pass

    @abstractmethod
    def move_cursor(self, y, x):
        pass

    @abstractmethod
    def display_status_bar(self, controller_state_str, name_of_file, cursor, total_lines, command):
        pass

class Subscriber(ABC):
    @abstractmethod
    def update(self, model):
        pass

class CursesView(Subscriber):
    def __init__(self):
        from text_editor_project.adapters.curses_adapter import CursesAdapter
        self.adapter : IVAdapter
        self.adapter = CursesAdapter()
        self.adapter.start()
        self.text = []
        self.cursor = None  # cursor должен быть объектом Cursor
        self.cmd_buf = CommandBuffer()
        self.screen_y, self.screen_x = self.adapter.stdscr.getmaxyx()
        self.controller_state_str = ""
        self.scroll_offset_x = 0  # Смещение для горизонтальной прокрутки
        self.scroll_offset_y = 0  # Смещение для вертикальной прокрутки
        self.opened_file = ""

        self.max_scroll = len(self.text) - self.screen_y  # Максимальное смещение

    def update_screen_size(self):
        # Получаем текущие размеры окна
        self.screen_y, self.screen_x = self.adapter.stdscr.getmaxyx()
        # Обновляем размер основного окна
        #self.adapter.stdscr.resize(self.screen_y, self.screen_x)
        # Обновляем размер командного окна (одно строка внизу экрана)
        #self.adapter.command_window.resize(1, self.screen_x)
        #self.adapter.command_window.mvwin(self.screen_y, - 1, 0)  # Перемещаем командное окно внизу экрана

    def update(self, model):
        """
        Обновление данных представления (при изменении модели).
        """
        # Обновляем содержимое текста
        self.text = [decode_from_cp1251(line.c_strb()) for line in model.get_all_lines()]
        self.controller_state_str = model.get_controller_state_str()
        self.opened_file = model.get_opened_filename()
        self.cursor = model.get_cursor()
        self.render()

    def render(self):
        """
        Отображает текст и строку состояния.
        """
        # Обновление размеров окна
        self.update_screen_size()

        # Очистка экрана
        self.adapter.clear_screen()
        self.adapter.clear_command_window()

        # Отображение текста с учетом прокрутки
        for i, line in enumerate(self.text[self.scroll_offset_y:self.scroll_offset_y + self.screen_y - 1]):
            # Обрезаем строку, если она длиннее ширины экрана с учетом прокрутки
            line_to_display = line[self.scroll_offset_x:self.scroll_offset_x + self.screen_x]
            self.adapter.display_text(i, 0, line_to_display)

        # Отображение строки состояния

        """
        self.adapter.display_status_bar(
            f"_:({curs_pos_y}, {curs_pos_x}), ↓→: ({self.scroll_offset_y},{self.scroll_offset_x}) "
            f"cmd: {self.cmd_buf.get_last_command()} mode: {self.controller_state_str}"
        )
        """

        self.adapter.display_status_bar(self.controller_state_str,
                                        self.opened_file,
                                        self.cursor, len(self.text), self.cmd_buf.get_last_command())

        # Перемещение курсора
        self.adapter.move_cursor(self.cursor.y_position - self.scroll_offset_y, self.cursor.x_position - self.scroll_offset_x)

        # Обновление экрана
        self.adapter.refresh_screen()

    def set_scroll_offset_y(self, new_offset_y):
        self.scroll_offset_y = new_offset_y

    def set_scroll_offset_x(self, new_offset_x):
        self.scroll_offset_x = new_offset_x

    def scroll_down(self):
        """Прокрутка вниз."""
        if self.scroll_offset_y < len(self.text) - self.screen_y + 1:
            self.scroll_offset_y += 1

    def scroll_up(self):
        """Прокрутка вверх."""
        if self.scroll_offset_y > 0:
            self.scroll_offset_y -= 1

    def scroll_right(self):
        """Прокрутка вправо."""
        if self.scroll_offset_x < max(len(line) for line in self.text) - self.screen_x:
            self.scroll_offset_x += 1

    def scroll_left(self):
        """Прокрутка влево."""
        if self.scroll_offset_x > 0:
            self.scroll_offset_x -= 1