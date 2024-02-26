import string
import Piece as piece

class Desk:
    def __init__(self):
        self.desk_view = [['.' for _ in range(8)] for _ in range(8)]
        
        #Белые
        for i in range(8):
            self.desk_view[6][i] = piece.Pawn(True)


        #Черные
        for i in range(8):
            self.desk_view[1][i] = piece.Pawn(False)


    def view_desk(self):
        letters =  string.ascii_uppercase[:8]
        print('   ',*letters,'    ')
        for i, s in enumerate(self.desk_view):
            print(f'{i+1}  ',*s,f'  {i+1}')
        print('   ',*letters,'    ')


