import curses
from text_editor_project.controllers.main_controller import ICAdapter
from text_editor_project.views.curses_view import IVAdapter

class CursesAdapter(ICAdapter, IVAdapter):
    def __init__(self):
        # Initialize the main window and set initial parameters
        self.stdscr = None
        self.command_window = None
        self.help_window = None

    def start(self):
        # Initialize the curses library

        # Creates and returns the main curses window object.
        # This object manages all drawing and input operations.
        self.stdscr = curses.initscr()
        self.stdscr.clear()  # Clear the screen before proceeding
        height, width = self.stdscr.getmaxyx()
        self.command_window = curses.newwin(1, width, height - 1, 0)
        self.help_window = curses.newwin(height, width, 0, 0)
        self.command_window.clear()
        self.help_window.clear()

        # Switches the terminal to "cbreak" mode,
        # allowing user input to be processed immediately without waiting for Enter.
        curses.cbreak()

        # Disables automatic echoing of typed characters,
        # so that user input is not duplicated on the screen.
        curses.noecho()

        # Enables keypad mode,
        # allowing special keys (such as arrow keys) to be processed as separate events.
        self.stdscr.keypad(True)
        self.command_window.keypad(True)
        self.help_window.keypad(True)

        # Checks if the terminal supports colored output.
        if curses.has_colors():
            # Enables color attributes for text
            curses.start_color()
            # Creates a color pair with ID 1, where the text is cyan and the background is black
            curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
            # This color can be used later with curses.color_pair(1).

    def stop(self):
        # Terminate the curses session
        # Disables "cbreak" mode, restoring standard input buffering.
        curses.nocbreak()
        # Disables keypad mode.
        self.stdscr.keypad(False)
        # Enables automatic echoing of typed characters.
        curses.echo()
        # Ends the curses session and clears the interface.
        curses.endwin()

    def clear_screen(self):
        # Clear the screen
        self.stdscr.clear()

    def clear_command_window(self):
        self.command_window.clear()

    def refresh_screen(self):
        # Refresh the screen
        self.stdscr.refresh()
        self.command_window.refresh()

    def display_text(self, y, x, text, color_pair=0):
        # Display text on the screen at a specified position
        self.stdscr.addstr(y, x, text, curses.color_pair(color_pair))

    def display_text_on_help_window(self, y, x, text, color_pair=2):
        self.help_window.addstr(y, x, text, curses.color_pair(color_pair))

    def get_key_input(self):
        # Read user input
        key = self.stdscr.getch()
        # print(key)
        return key

    def move_cursor(self, y, x):
        # Move the cursor
        self.stdscr.move(y, x)

    def display_status_bar(self, controller_state_str, name_of_file, cursor, total_lines, command):
        controller_state_str = controller_state_str
        name_of_file = name_of_file
        cursor = cursor
        total_lines = total_lines
        height, width = self.stdscr.getmaxyx()
        self.command_window.mvwin(height - 1, 0)
        # Enable color pair 1 to change the text color in the status bar
        self.command_window.attron(curses.color_pair(1))
        str_to_display = ("[" + str(cursor.y_position + 1) + "/" + str(total_lines)
                          + ", "+ str(cursor.x_position + 1) + "] ")
        str_to_display += "[" + name_of_file + "] "
        if len(command) > width - len(str_to_display) - len(controller_state_str) - 6:
            command = command[width - len(str_to_display) - len(controller_state_str) - 6:]
            str_to_display += "[" + command + "]"
        else:
            str_to_display += "[" + command + "]"
        # str_to_display += "[" + controller_state_str + "] "
        self.command_window.addstr(0, 0, str_to_display)
        self.command_window.addstr(0, width - len(controller_state_str) - 3, "[" + controller_state_str + "]")

        # Disable the color pair, returning to the default text color.
        self.command_window.attroff(curses.color_pair(1))
        # Clears the remaining part of the line to the end of the screen so that the status bar is displayed correctly.
        self.command_window.clrtoeol()
