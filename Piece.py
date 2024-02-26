
class Piece():

    def __init__(self,color):
        self.color = color
        self.name = ""


    def is_white(self):
        return self.color


    
class Pawn(Piece):

    def __init__(self,color):
        super().__init__(color)
        self.name = "P"
        if self.color:
            self.name = "♟"
        else:
            self.name = "♙"

    def set_color(self):
        if self.color:
            self.name = "♟"
        else:
            self.name = "♙"

    def __str__(self):
        return self.name