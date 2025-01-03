import curses

class CommandBuffer:
    def __init__ (self):
        self.command_history = []
        self.clipboard_buffer = ""

    def parse_command(self, command):
        """Добавляет команду в буфер истории."""

        if ord(command) == curses.KEY_UP:
            self.command_history.append("↑")
            return "UP_command"

        if ord(command) == curses.KEY_DOWN:
            self.command_history.append("↓")
            return "DOWN_command"

        if ord(command) == curses.KEY_RIGHT:
            self.command_history.append("→")
            return "RIGHT_command"

        if ord(command) == curses.KEY_LEFT:
            self.command_history.append("←")
            return "LEFT_command"

        if command == "/":
            self.command_history.append(command)
            return "/_command"

        if command == "?":
            self.command_history.append(command)
            return "?_command"

        if command == ":":
            self.command_history.append(command)
            return ":_command"

        if command == "^":
            self.command_history.append(command)
            return "^_command"

        if command == "$":
            self.command_history.append(command)
            return "$_command"

        if command == "b":
            self.command_history.append(command)
            return "b_command"

        if command == "x":
            self.command_history.append(command)
            return "x_command"

        if len(self.command_history) > 0:
            last_command = self.command_history[len(self.command_history) - 1]
            if last_command == "g" and command == "g":
                self.command_history[len(self.command_history) - 1] = "gg"
                return "gg_command"

            if last_command.isdigit() and command.isdigit():
                self.command_history[len(self.command_history) - 1] += command
                return "number_command"

            if last_command.isdigit() and command == "G":
                self.command_history[len(self.command_history) - 1] += command
                return "NG_command"

            if last_command == "d" and command == "i":
                self.command_history[len(self.command_history) - 1] += command
                return "unknown_command"

            if last_command == "di" and command == "w":
                self.command_history[len(self.command_history) - 1] += command
                return "diw_command"

            if last_command == "d" and command == "d":
                self.command_history[len(self.command_history) - 1] += command
                return "dd_command"

            if last_command == "y" and command == "y":
                self.command_history[len(self.command_history) - 1] += command
                return "yy_command"

            if last_command == "y" and command == "w":
                self.command_history[len(self.command_history) - 1] += command
                return "yw_command"

            if last_command == "r":
                self.command_history.append(command)
                return "r_command"

        if command == "i":
            self.command_history.append(command)
            return "i_command"

        if command == "o":
            self.command_history.append(command)
            return "o_command"

        if command == "I":
            self.command_history.append(command)
            return "I_command"

        if command == "A":
            self.command_history.append(command)
            return "A_command"

        if command == "S":
            self.command_history.append(command)
            return "S_command"

        if command == "w":
            self.command_history.append(command)
            return "w_command"

        if command == "p":
            self.command_history.append(command)
            return "p_command"

        if command == "G":
            self.command_history.append(command)
            return "G_command"
        # Если условия не сработали, просто добавляем команду
        self.command_history.append(command)
        return "unknown_command"

    def get_last_command(self):
        if len(self.command_history) > 0:
            return self.command_history[len(self.command_history)-1]
        else:
            return " "