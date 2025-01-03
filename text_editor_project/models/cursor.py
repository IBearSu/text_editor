class Cursor:
    def __init__(self, x=0, y=0):
        self.x_position = x
        self.y_position = y

    def set_y_position(self, new_y_position):
        self.y_position = new_y_position

    def set_x_position(self, new_x_position):
        self.x_position = new_x_position

    def move_up(self):
        """
        Двигает курсор на 1 единицу вверх.
        y_position -= 1
        """
        self.y_position -= 1

    def move_down(self):
        """
        Двигает курсор на 1 единицу вниз.
        y_position += 1
        """
        self.y_position += 1

    def move_left(self):
        """
        Двигает курсор на 1 единицу влево.
        x_position -= 1
        """
        self.x_position -= 1

    def move_right(self):
        """
        Двигает курсор на 1 единицу вправо.
        x_position += 1
        """
        self.x_position += 1