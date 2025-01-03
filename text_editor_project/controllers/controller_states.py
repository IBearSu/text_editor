import curses

from text_editor_project.models.helpers import decode_from_cp1251, encode_to_cp1251

class NavigationState:
    def __init__(self, controller):
        self.controller = controller

    def handle_input(self, key):
        if key == 10:
            handle_movement_key(self, curses.KEY_DOWN)
            return
        current_command = self.controller.cmd_buf.parse_command(str(chr(key)))
        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT,
                   curses.KEY_RIGHT, curses.KEY_PPAGE, curses.KEY_NPAGE]:
            handle_movement_key(self, key)
        else:
            self.handle_command(current_command)

    def handle_command(self, command):
        if command == "i_command":
            self.execute_i_command()
        elif command == "o_command":
            self.execute_o_command()
        elif command == "I_command":
            self.execute_big_i_command()
        elif command == "A_command":
            self.execute_big_a_command()
        elif command == "S_command":
            self.execute_big_s_command()
        elif command == "r_command":
            self.execute_r_command()
        elif command == "/_command":
            self.execute_forward_slash_sign_command()
        elif command == "?_command":
            self.execute_question_sign_command()
        elif command == ":_command":
            self.execute_colon_sign_command()
        elif command == "^_command":
            self.execute_circumflex_sign_command()
        elif command == "$_command":
            execute_dollar_sign_command(self)
        elif command == "w_command":
            self.execute_w_command()
        elif command == "b_command":
            self.execute_b_command()
        elif command == "x_command":
            self.execute_x_command()
        elif command == "diw_command":
            self.execute_diw_command()
        elif command == "dd_command":
            self.execute_dd_command()
        elif command == "yy_command":
            self.execute_yy_command()
        elif command == "p_command":
            self.execute_p_command()
        elif command == "gg_command":
            self.execute_gg_command()
        elif command == "G_command":
            self.execute_big_g_command()
        elif command == "NG_command":
            self.execute_big_n_big_g_command()

    def execute_i_command(self):
        self.controller.set_state(InsertState(self.controller))

    def execute_o_command(self):
        handle_movement_key(self, curses.KEY_RIGHT)
        self.controller.set_state(InsertState(self.controller))

    def execute_big_i_command(self):
        self.execute_circumflex_sign_command()
        self.controller.set_state(InsertState(self.controller))

    def execute_big_a_command(self):
        execute_dollar_sign_command(self)
        self.controller.set_state(InsertState(self.controller))

    def execute_big_s_command(self):
        self.execute_dd_command()
        self.controller.set_state(InsertState(self.controller))

    def execute_r_command(self):
        if len(self.controller.model.lines) > 0:
            model = self.controller.model
            position_x = model.get_cursor_x()
            position_y = model.get_cursor_y()
            key_to_insert = self.controller.cmd_buf.get_last_command()
            model.delete_key_at_position(position_x, position_y)
            model.insert_char(position_y, position_x, key_to_insert)

    def execute_forward_slash_sign_command(self):
        self.controller.set_state(SearchState(self.controller, "/"))

    def execute_question_sign_command(self):
        self.controller.set_state(SearchState(self.controller, "?"))

    def execute_colon_sign_command(self):
        self.controller.set_state(CommandState(self.controller))

    def execute_circumflex_sign_command(self):
        model = self.controller.model
        model.set_cursor_x(0)
        new_offset_x = 0
        view_subscribers = model.get_view_subscribers()
        view_subscribers[0].set_scroll_offset_x(new_offset_x)


    def execute_w_command(self):
        self.move_cursor_to_next_word()
        model = self.controller.model
        line_length = model.lines[model.cursor.y_position].length()
        screen_x = model.view_subscribers[0].screen_x
        screen_y = model.view_subscribers[0].screen_y
        x_position = model.get_cursor_x()
        y_position = model.get_cursor_y()
        view_subscribers = model.get_view_subscribers()
        if x_position > screen_x:
            new_offset_x = line_length - screen_x
            view_subscribers[0].set_scroll_offset_x(new_offset_x)
        else:
            new_offset_x = 0
            view_subscribers[0].set_scroll_offset_x(new_offset_x)
        if y_position >= screen_y:
            new_offset_y = y_position - screen_y + 2
            view_subscribers[0].set_scroll_offset_y(new_offset_y)
        elif y_position < screen_y - 1:
            new_offset_y = 0
            view_subscribers[0].set_scroll_offset_y(new_offset_y)

    def execute_b_command(self):
        self.move_cursor_to_previous_word()
        model = self.controller.model
        line_length = model.lines[model.cursor.y_position].length()
        screen_x = model.view_subscribers[0].screen_x
        screen_y = model.view_subscribers[0].screen_y
        x_position = model.get_cursor_x()
        y_position = model.get_cursor_y()
        view_subscribers = model.get_view_subscribers()
        if x_position > screen_x:
            new_offset_x = line_length - screen_x
            view_subscribers[0].set_scroll_offset_x(new_offset_x)
        else:
            new_offset_x = 0
            view_subscribers[0].set_scroll_offset_x(new_offset_x)
        if y_position >= screen_y:
            new_offset_y = y_position - screen_y + 2
            view_subscribers[0].set_scroll_offset_y(new_offset_y)
        elif model.cursor.y_position < screen_y - 1:
            new_offset_y = 0
            view_subscribers[0].set_scroll_offset_y(new_offset_y)

    def execute_x_command(self):
        model = self.controller.model
        position_x = model.get_cursor_x() + 1
        position_y = model.get_cursor_y()
        if len(model.lines) > 0 and model.lines[position_y].length() - 1 > position_x:
            model.delete_key_at_position(position_x, position_y)
            model.set_is_modified()

    def execute_diw_command(self):
        model = self.controller.model
        position_x = model.get_cursor_x()
        position_y = model.get_cursor_y()
        model.delete_word_at_position(position_y, position_x)
        position_x = model.get_cursor_x()
        view_subscribers = model.get_view_subscribers()
        model.set_is_modified()
        if position_x < view_subscribers[0].screen_x:
            view_subscribers[0].scroll_offset_x = 0

    def execute_dd_command(self):
        model = self.controller.model
        position_x = model.get_cursor_x()
        position_y = model.get_cursor_y()
        view_subscribers = model.get_view_subscribers()
        line = model.lines[position_y]
        if line.length() > 0:
            self.controller.cmd_buf.clipboard_buffer = line.c_strb()
            if self.controller.cmd_buf.clipboard_buffer.endswith(b'\n'):
                self.controller.cmd_buf.clipboard_buffer = self.controller.cmd_buf.clipboard_buffer[:-1]
            model.set_cursor_x(0)
            view_subscribers[0].scroll_offset_x = 0
            model.delete_all_text_on_the_line(position_y)
            model.set_is_modified()

    def execute_yy_command(self):
        position_y = self.controller.model.get_cursor_y()
        line = self.controller.model.lines[position_y]
        self.controller.cmd_buf.clipboard_buffer = line.c_strb()
        if self.controller.cmd_buf.clipboard_buffer.endswith(b'\n'):
            self.controller.cmd_buf.clipboard_buffer = self.controller.cmd_buf.clipboard_buffer[:-1]

    def execute_p_command(self):
        model = self.controller.model
        position_x = model.get_cursor_x()
        position_y = model.get_cursor_y()
        line_to_insert = self.controller.cmd_buf.clipboard_buffer
        model.insert_text(position_y, position_x, line_to_insert)
        model.lines[position_y].shrink_to_fit()
        model.set_is_modified()

    def execute_gg_command(self):
        model = self.controller.model
        model.set_cursor_y(0)
        model.set_cursor_x(0)
        view_subscribers = model.get_view_subscribers()
        view_subscribers[0].set_scroll_offset_y(0)
        view_subscribers[0].set_scroll_offset_x(0)

    def execute_big_g_command(self):
        model = self.controller.model
        x_position = model.get_cursor_x()
        y_position = model.get_cursor_y()
        view_subscribers = model.get_view_subscribers()
        last_line_index = len(model.lines) - 1
        model.cursor.y_position = last_line_index
        last_line_length = model.lines[last_line_index].length()
        print(last_line_length)
        if last_line_length > 0:
            model.set_cursor_x(last_line_length - 1)
        else:
            model.set_cursor_x(last_line_length)
        screen_x = view_subscribers[0].screen_x
        screen_y = view_subscribers[0].screen_y
        x_position = model.get_cursor_x()
        y_position = model.get_cursor_y()
        if x_position > screen_x:
            new_offset_x = last_line_length - screen_x
            view_subscribers[0].set_scroll_offset_x(new_offset_x)
        else:
            new_offset_x = 0
            view_subscribers[0].set_scroll_offset_x(new_offset_x)
        if y_position >= screen_y:
            new_offset_y = model.cursor.y_position - screen_y + 2
            view_subscribers[0].set_scroll_offset_y(new_offset_y)
        elif y_position < screen_y - 1:
            new_offset_y = 0
            view_subscribers[0].set_scroll_offset_y(new_offset_y)

    def execute_big_n_big_g_command(self):
        last_command = self.controller.cmd_buf.get_last_command()
        line_number_to_go_on = int(last_command.split('G')[0]) - 1
        model = self.controller.model
        view_subscribers = model.get_view_subscribers()
        if line_number_to_go_on > len(model.lines) - 1:
            return
        last_line_index = len(model.lines) - 1
        model.set_cursor_y(last_line_index)
        last_line_length = model.lines[last_line_index].length()
        model.set_cursor_x(last_line_length - 1)
        screen_x = view_subscribers[0].screen_x
        screen_y = view_subscribers[0].screen_y

        if -1 < line_number_to_go_on < len(model.lines):
            model.set_cursor_y(line_number_to_go_on)
            model.set_cursor_x(0)

        x_position = model.get_cursor_x()

        if x_position > screen_x:
            new_offset_x = last_line_length - screen_x
            view_subscribers[0].set_scroll_offset_x(new_offset_x)
        else:
            new_offset_x = 0
            view_subscribers[0].set_scroll_offset_x(new_offset_x)
        y_position = model.get_cursor_y()
        if y_position >= screen_y:
            new_offset_y = y_position - screen_y + 2
            view_subscribers[0].set_scroll_offset_y(new_offset_y)
        elif y_position < screen_y - 1:
            new_offset_y = 0
            view_subscribers[0].set_scroll_offset_y(new_offset_y)

    def move_cursor_to_next_word(self):
        model = self.controller.model
        x_position = model.get_cursor_x()
        y_position = model.get_cursor_y()
        line_index = y_position
        current_pos = x_position
        next_pos, line_index = model.find_next_word(line_index, current_pos)
        if next_pos == model.lines[line_index].length():
            next_pos -= 1
        model.set_cursor_x(next_pos)
        model.set_cursor_y(line_index)

    def move_cursor_to_previous_word(self):
        model = self.controller.model
        line_index = model.get_cursor_y()
        current_pos = model.get_cursor_x()
        prev_pos, line_index = model.find_previous_word(line_index, current_pos)
        model.set_cursor_x(prev_pos)
        model.set_cursor_y(line_index)

class InsertState:
    def __init__(self, controller):
        self.controller = controller

    def handle_input(self, key):
        if key == 27:  # 27 == ESC
            self.handle_escape_key()

        elif key == 8: # 8 == BACKSPACE
            self.handle_backspace_key()

        elif key == 330: # 330 == DELETE
            self.handle_delete_key()

        elif key == 10: # 10 == ENTER
            self.handle_enter_key()

        elif key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            handle_movement_key(self, key)

        else:
            self.handle_insert_char(key)

    def handle_insert_char(self, key):
        model = self.controller.model
        x_position = model.get_cursor_x()
        y_position = model.get_cursor_y()
        model.insert_char(y_position, x_position, key)
        handle_movement_key(self, curses.KEY_RIGHT)

    def handle_enter_key(self):
        model = self.controller.model
        x_position = model.get_cursor_x()
        y_position = model.get_cursor_y()

        if x_position == 0:
            model.add_new_line(y_position, '\n')
            handle_movement_key(self, curses.KEY_DOWN)
        elif x_position == model.lines[y_position].length() - 1:
            model.add_new_line(y_position + 1, '\n')
            handle_movement_key(self, curses.KEY_DOWN)
        else:
            current_line = decode_from_cp1251(model.lines[y_position].c_strb())
            left_part = current_line[:x_position]  + '\n'
            model.lines[y_position].clear()
            encoded_left_part = encode_to_cp1251(left_part)
            model.insert_text(y_position, 0, encoded_left_part)
            right_part = current_line[x_position:]
            model.add_new_line(y_position + 1, right_part)
            model.set_cursor_x(0)
            handle_movement_key(self, curses.KEY_DOWN)

    def handle_escape_key(self):
        self.controller.set_state(NavigationState(self.controller))

    def handle_backspace_key(self):
        if len(self.controller.model.lines) > 0:
            model = self.controller.model
            position_x = model.get_cursor_x()
            position_y = model.get_cursor_y()
            if position_x != 0:
                model.delete_key_at_position(position_x - 1, position_y)
                model.set_is_modified()
                handle_movement_key(self, curses.KEY_LEFT)

            elif model.lines[position_y].length() == 1 and position_y != 0:
                model.lines.pop(position_y)
                model.set_is_modified()
                handle_movement_key(self, curses.KEY_UP)
                execute_dollar_sign_command(self)

            elif position_y != 0:
                model.delete_key_at_position(model.lines[position_y - 1].length() - 1, position_y - 1)
                handle_movement_key(self, curses.KEY_UP)
                execute_dollar_sign_command(self)
                model.lines[position_y - 1] += model.lines[position_y]
                model.lines.pop(position_y)
                model.set_is_modified()
                handle_movement_key(self, curses.KEY_RIGHT)

    def handle_delete_key(self):
        if len(self.controller.model.lines) > 0:
            model = self.controller.model
            position_x = model.get_cursor_x()
            position_y = model.get_cursor_y()
            model.delete_key_at_position(position_x, position_y)
            model.set_is_modified()


class CommandState:
    def __init__(self, controller):
        self.controller = controller
        self.command_buffer = ""
        self.is_in_help_mode = False
        self.original_lines = None

    def handle_input(self, key):
        if key == 27:  # 27 == ESC
            if self.is_in_help_mode:
                self.controller.model.set_lines(self.original_lines)
                self.controller.model.notify_subscribers()
                self.is_in_help_mode = False
            else:
                self.controller.set_state(NavigationState(self.controller))
        elif key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT,
                   curses.KEY_RIGHT, curses.KEY_PPAGE, curses.KEY_NPAGE]:
            handle_movement_key(self, key)

        elif key == 10:  # 10 == ENTER
            self.execute_command()

        elif chr(key).isprintable():
            self.command_buffer += chr(key)
            self.controller.cmd_buf.command_history.append(self.command_buffer)

        elif key == 8:
            self.command_buffer = self.command_buffer[:-1]
            self.controller.cmd_buf.command_history.append(self.command_buffer)

    def execute_command(self):
        command = self.command_buffer.strip()
        self.controller.cmd_buf.command_history.append(command)
        model = self.controller.model
        if command.startswith("o "):
            filename = command[2:].strip()
            model.opened_file = filename
            model.load_from_file(filename)
            model.set_cursor_y(0)
            model.set_cursor_x(0)
        elif command == "x":
            model.save_to_file(model.opened_file)
            exit()
        elif command == "w":
            model.save_to_file(model.opened_file)
        elif command.startswith("w "):
            filename = command[2:].strip()
            model.save_to_file(filename)
        elif command == "q":
            if model.get_is_modified():
                print("Файл был изменён. Для выхода используйте 'q!' или сохраните файл.")
            else:
                exit()
        elif command == "q!":
            exit()
        elif command == "wq!":
            model.save_to_file(model.filename)
            exit()
        elif command == "h":
            if not self.is_in_help_mode:
                self.is_in_help_mode = True
                self.original_lines = self.controller.model.lines.copy()
                if len(self.controller.model.help_lines) == 0:
                    self.controller.model.load_help_file()
                self.controller.model.set_temp_buff(self.controller.model.get_lines())
                self.controller.model.set_lines(self.controller.model.get_help_lines())
        elif command.isdigit():
            line_number = int(command)
            self.goto_line(line_number)
        else:
            print("Неизвестная команда.")

    def goto_line(self, line_number):
        line_number_to_go_on = line_number - 1
        model = self.controller.model
        if line_number_to_go_on > len(model.lines) - 1:
            return
        last_line_index = len(model.lines) - 1
        model.set_cursor_y(last_line_index)
        last_line_length = model.lines[last_line_index].length()
        model.set_cursor_x(last_line_length - 1)
        screen_x = model.view_subscribers[0].screen_x
        screen_y = model.view_subscribers[0].screen_y

        if -1 < line_number_to_go_on < len(model.lines):
            model.set_cursor_y(line_number_to_go_on)
            model.set_cursor_x(0)
        else:
            return

        x_position = model.get_cursor_x
        y_position = model.get_cursor_y
        view_subscribers = model.get_view_subscribers()

        if x_position > screen_x:
            new_offset_x = last_line_length - screen_x
            view_subscribers[0].set_scroll_offset_x(new_offset_x)
        else:
            new_offset_x = 0
            view_subscribers[0].set_scroll_offset_x(new_offset_x)

        if y_position >= screen_y:
            new_offset_y = y_position - screen_y + 2
            view_subscribers[0].set_scroll_offset_y(new_offset_y)
        elif y_position < screen_y - 1:
            new_offset_y = 0
            view_subscribers[0].set_scroll_offset_y(new_offset_y)



class SearchState:
    def __init__(self, controller, search_type):
        self.controller = controller
        self.search_buffer = search_type
        self.last_direction = None

    def handle_input(self, key):
        x_position = self.controller.model.get_cursor_x()
        y_position = self.controller.model.get_cursor_y()
        if key == 27:  # ESC keycode
            self.controller.set_state(NavigationState(self.controller))
        elif key == 10:  # ENTER
            if self.search_buffer[0] == '/':
                self.controller.cmd_buf.command_history.append(self.search_buffer)
                self.perform_search_to_end_of_file(y_position, x_position)
                self.last_direction = 'forward'
            elif self.search_buffer[0] == '?':
                self.controller.cmd_buf.command_history.append(self.search_buffer)
                self.perform_search_to_start_of_file(y_position, x_position)
                self.last_direction = 'backward'
        elif key == ord('n') and self.last_direction:
            if self.last_direction == 'forward':
                self.perform_search_to_end_of_file(y_position, x_position + 1)
            elif self.last_direction == 'backward':
                self.perform_search_to_start_of_file(y_position, x_position)
        elif key == ord('N') and self.last_direction:  # Повторить поиск в обратном направлении
            if self.last_direction == 'forward':
                self.perform_search_to_start_of_file(y_position, x_position)
            elif self.last_direction == 'backward':
                self.perform_search_to_end_of_file(y_position, x_position + 1)
        elif key == 8: # 8 == BACKSPACE
            self.search_buffer = self.search_buffer[:-1]
            self.controller.cmd_buf.command_history.append(self.search_buffer)
        else:
            self.search_buffer += chr(key)
            self.controller.cmd_buf.command_history.append(self.search_buffer)

    def perform_search_to_end_of_file(self, start_line_index, start_char_index):
        model = self.controller.model
        screen_x = model.view_subscribers[0].screen_x
        screen_y = model.view_subscribers[0].screen_y
        string_to_search = self.search_buffer[1:]
        start_line_index = start_line_index
        start_char_index = start_char_index
        # print(f"Searching for: {string_to_search}")

        decoded_my_string = decode_from_cp1251(model.lines[start_line_index].c_strb())
        found_at_index = decoded_my_string.find(string_to_search, start_char_index)

        if found_at_index != -1:  # Если нашли на текущей строке, то проверяем на смещение и устанавливаем курсор
            # print(f"Found at: {start_line_index, found_at_index}")
            model.set_cursor_x(found_at_index)
        else:
            start_char_index = 0
            for line_index in range(start_line_index + 1, len(model.lines)):
                decoded_my_string = decode_from_cp1251(model.lines[line_index].c_strb())
                found_at_index = decoded_my_string.find(string_to_search, start_char_index)
                if found_at_index != -1:
                    model.set_cursor_x(found_at_index)
                    model.set_cursor_y(line_index)
                    break
        if model.get_cursor_x() > screen_x:
            line_length = model.lines[model.get_cursor_y()].length()
            new_offset_x = line_length - screen_x
            model.view_subscribers[0].set_scroll_offset_x(new_offset_x)
        else:
            new_offset_x = 0
            model.view_subscribers[0].set_scroll_offset_x(new_offset_x)
        if model.cursor.y_position >= screen_y - 1:
            new_offset_y = model.cursor.y_position - screen_y + 2
            model.view_subscribers[0].set_scroll_offset_y(new_offset_y)
        elif model.cursor.y_position < screen_y - 1:
            new_offset_y = 0
            model.view_subscribers[0].set_scroll_offset_y(new_offset_y)

    def perform_search_to_start_of_file(self, start_line_index, start_char_index):
        model = self.controller.model
        screen_x = model.view_subscribers[0].screen_x
        screen_y = model.view_subscribers[0].screen_y
        string_to_search = self.search_buffer[1:]
        start_line_index = start_line_index
        start_char_index = start_char_index
        # print(f"Searching for: {string_to_search}")

        decoded_my_string = decode_from_cp1251(model.lines[start_line_index].c_strb())
        found_at_index = decoded_my_string.rfind(string_to_search, 0, start_char_index)

        if found_at_index != -1:  # Если нашли на текущей строке, то проверяем на смещение и устанавливаем курсор
            # print(f"Found at: {start_line_index, found_at_index}")
            model.set_cursor_x(found_at_index)
        elif start_line_index > 0:
            line_index = start_line_index - 1
            start_char_index = model.lines[line_index].length()
            while line_index >= 0 and found_at_index == -1:
                decoded_my_string = decode_from_cp1251(model.lines[line_index].c_strb())
                found_at_index = decoded_my_string.rfind(string_to_search, 0, start_char_index)
                if found_at_index != -1:
                    model.set_cursor_x(found_at_index)
                    model.set_cursor_y(line_index)
                    break
                line_index -= 1
                start_char_index = model.lines[line_index].length()

        if model.get_cursor_x() > screen_x:
            line_length = model.lines[model.get_cursor_y()].length()
            new_offset_x = line_length - screen_x
            model.view_subscribers[0].set_scroll_offset_x(new_offset_x)
        else:
            new_offset_x = 0
            model.view_subscribers[0].set_scroll_offset_x(new_offset_x)
        if model.get_cursor_y() >= screen_y:
            new_offset_y = model.get_cursor_y() - screen_y + 2
            model.view_subscribers[0].set_scroll_offset_y(new_offset_y)
        elif model.get_cursor_y() < screen_y - 1:
            new_offset_y = 0
            model.view_subscribers[0].set_scroll_offset_y(new_offset_y)


def execute_dollar_sign_command(state):
    model = state.controller.model
    line_length = model.lines[model.cursor.y_position].length()
    model.set_cursor_x(line_length - 1)
    screen_x = model.view_subscribers[0].screen_x

    if line_length > screen_x:
        new_offset_x = line_length - screen_x
        model.view_subscribers[0].set_scroll_offset_x(new_offset_x)

def handle_movement_key(state, key):
    cursor = state.controller.model.cursor
    model = state.controller.model
    lines = state.controller.model.lines
    screen_y = state.controller.model.view_subscribers[0].screen_y
    screen_x = state.controller.model.view_subscribers[0].screen_x
    scroll_offset_x = state.controller.model.view_subscribers[0].scroll_offset_x
    scroll_offset_y = state.controller.model.view_subscribers[0].scroll_offset_y
    line_length = lines[cursor.y_position].length()
    lines_in_total = len(lines)
    top_line_length = lines[cursor.y_position - 1].length()

    if lines_in_total > 0:
        if key == curses.KEY_UP and cursor.y_position != 0:
            if cursor.y_position <= scroll_offset_y:
                model.view_subscribers[0].scroll_up()
            if top_line_length - 1 < model.get_cursor_x():
                if top_line_length - 1 > screen_x:
                    new_offset_x = top_line_length - screen_x
                    model.view_subscribers[0].set_scroll_offset_x(new_offset_x)
                else:
                    new_offset_x = 0
                    model.view_subscribers[0].set_scroll_offset_x(new_offset_x)
                cursor.set_x_position(top_line_length - 1)
                cursor.move_up()
            else:
                cursor.move_up()

        elif key == curses.KEY_DOWN and cursor.y_position < lines_in_total - 1:
            bottom_line_length = lines[cursor.y_position + 1].length()
            if cursor.y_position >= screen_y - 2 + scroll_offset_y:
                model.view_subscribers[0].scroll_down()
            if bottom_line_length - 1 < model.get_cursor_x():
                if bottom_line_length - 1 > screen_x:
                    new_offset_x = bottom_line_length - screen_x
                    model.view_subscribers[0].set_scroll_offset_x(new_offset_x)
                else:
                    new_offset_x = 0
                    model.view_subscribers[0].set_scroll_offset_x(new_offset_x)
                cursor.set_x_position(bottom_line_length - 1)
                cursor.move_down()
            else:
                cursor.move_down()

        elif key == curses.KEY_LEFT and model.get_cursor_x() > 0:
            if model.get_cursor_x() <= scroll_offset_x:
                model.view_subscribers[0].scroll_left()
                cursor.move_left()
            elif model.get_cursor_x() > scroll_offset_x:
                cursor.move_left()

        elif key == curses.KEY_RIGHT:
            if model.get_cursor_x() == screen_x - 1 + scroll_offset_x:
                model.view_subscribers[0].scroll_right()
                if model.get_cursor_x() < line_length - 1:
                    cursor.move_right()
            # Если курсор не на последнем доступном символе в строке, двигаем его вправо
            elif model.get_cursor_x() < line_length - 1 and model.get_cursor_x() < screen_x - 1 + scroll_offset_x:
                cursor.move_right()

        elif key == curses.KEY_PPAGE:  # Page Up
            previous_x_position = model.get_cursor_x()
            if model.view_subscribers[0].scroll_offset_y > 0:  # Проверяем, если есть куда прокручивать
                cursor.move_up()  # Перемещаем курсор вверх
                model.view_subscribers[0].scroll_up()  # Прокручиваем экран вверх
                # Если новая строка короче, чем предыдущая, перемещаем курсор в конец строки
                new_x_position = model.lines[cursor.y_position].length() - 1
                if new_x_position < previous_x_position:
                    cursor.set_x_position(new_x_position)
            # Если курсор выходит за пределы экрана, прокручиваем экран по горизонтали
            if model.get_cursor_x() > model.view_subscribers[0].screen_x - 1:
                new_offset_x = model.get_cursor_x() - model.view_subscribers[0].screen_x + 1
                model.view_subscribers[0].set_scroll_offset_x(new_offset_x)
            else:
                model.view_subscribers[0].set_scroll_offset_x(0)
            # Обеспечиваем, что курсор не выйдет за левую границу
            if model.get_cursor_x() < 0:
                model.set_cursor_x(0)
                model.view_subscribers[0].scroll_offset_x = 0

        elif key == curses.KEY_NPAGE:  # Page Down
            previous_x_position = model.get_cursor_x()
            if (model.view_subscribers[0].scroll_offset_y <
                    len(model.lines) - model.view_subscribers[0].screen_y):  # Если есть куда прокручивать
                cursor.move_down()  # Перемещаем курсор вниз
                model.view_subscribers[0].scroll_down()  # Прокручиваем экран вниз
                # Если новая строка короче, чем предыдущая, перемещаем курсор в конец строки
                new_x_position = model.lines[cursor.y_position].length() - 1
                if new_x_position < previous_x_position:
                    cursor.set_x_position(new_x_position)
            # Если курсор выходит за пределы экрана, прокручиваем экран по горизонтали
            if model.get_cursor_x() > model.view_subscribers[0].screen_x - 1:
                new_offset_x = model.get_cursor_x() - model.view_subscribers[0].screen_x + 1
                model.view_subscribers[0].set_scroll_offset_x(new_offset_x)
            else:
                model.view_subscribers[0].set_scroll_offset_x(0)
            # Обеспечиваем, что курсор не выйдет за левую границу
            if model.get_cursor_x() < 0:
                cursor.set_x_position(0)
                model.view_subscribers[0].scroll_offset_x = 0
