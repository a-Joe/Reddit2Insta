
# Holds the positional data for where to paste/print onto image 

class Position:
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos

    def set_position(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos

    def move_down(self,pixels):
        self.y += pixels

    def move_up(self,pixels):
        self.y -= pixels

    def move_left(self, pixels):
        self.x -= pixels

    def move_right(self, pixels):
        self.x += pixels

    def draw_text(self, text, font, fill):
        pass