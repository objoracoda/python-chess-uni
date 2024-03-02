# Импорт библиотеки для отрисовки букв на поле
import string

# Импорт класса всех фигур
import Piece, Pawn, Rook, Knight, Bishop, Queen, King


class Chessboard:
    def __init__(self):
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        self.initialize_board()
        self.current_player = 'white' 


    def initialize_board(self):
        # Расставляем черные фигуры
        
        self.board[0] = [Rook.Rook('black'), Knight.Knight('black'), Bishop.Bishop('black'), Queen.Queen('black'),
                         King.King('black'), Bishop.Bishop('black'), Knight.Knight('black'), Rook.Rook('black')]
        self.board[1] = [Pawn.Pawn('black') for _ in range(8)]

        # Расставляем белые фигуры
        self.board[7] = [Rook.Rook('white'), Knight.Knight('white'), Bishop.Bishop('white'), Queen.Queen('white'),
                         King.King('white'), Bishop.Bishop('white'), Knight.Knight('white'), Rook.Rook('white')]
        self.board[6] = [Pawn.Pawn('white') for _ in range(8)]


    def print_board(self):
        letters =  string.ascii_uppercase[:8]
        print('   ',*letters,'    ')
        for i, s in enumerate(self.board):
            print(f'{i+1}  ',*s,f'  {i+1}')
        print('   ',*letters,'    ')


    def is_valid_move(self, start_row, start_col, end_row, end_col):
        piece = self.board[start_row][start_col]

        if not isinstance(piece, Piece.Piece):
            return False

        # Проверка наличия фигуры на стартовой позиции
        if piece == '.':
            return False

        # Проверка, принадлежит ли фигура текущему игроку
        if piece.color != self.current_player:
            return False

        # Получение возможных ходов для фигуры
        possible_moves = piece.get_possible_moves(self.board, start_row, start_col)

        # Проверка, является ли конечная позиция одним из возможных ходов
        if (end_row, end_col) not in possible_moves:
            return False


        return True


    def move_piece(self, start_row, start_col, end_row, end_col):
        piece = self.board[start_row][start_col]
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = '.'

        #  Проверка на преварщение в королеву пешки
        if isinstance(piece,Pawn.Pawn):
            if end_row == 0:
                queen_exists = any(isinstance(piece, Queen.Queen) and piece.color == 'white' for row in self.board for piece in row)
                if not queen_exists:
                    self.board[end_row][end_col] = Queen.Queen('white')

            if end_row == 7:
                queen_exists = any(isinstance(piece, Queen.Queen) and piece.color == 'black' for row in self.board for piece in row)
                if not queen_exists:
                    self.board[end_row][end_col] = Queen.Queen('black')

        self.current_player = 'black' if self.current_player == 'white' else 'white'


    def check_win(self):
        # Проверяем наличие короля нужного цвета на доске
        w,b = False,False
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if isinstance(piece, King.King) and piece.color == 'white':
                    w = True
                if isinstance(piece, King.King) and piece.color == 'black':
                    b = True
        if not w:
            print('Черные выиграли!')
            return False
        if not b:
            print('Белые выиграли!')
            return False
        return True



class GameLoop:
    def __init__(self):
        self.board = Chessboard()
        
    def get_move(self):
        while True:
            move = input("Введите ваш ход (например -> 'a2-a4'): ").strip().lower()
            if len(move) == 5 and move[0] in 'abcdefgh' and move[1] in '12345678' and move[2] == '-' and move[3] in 'abcdefgh' and move[4] in '12345678':
                return move
            else:
                print("Не корректный ход. Введите в формате 'a2-a4'.")


    def main(self):
        #board = Chessboard()
        self.board.print_board()

        #current_turn = True

        while True:
            move = self.get_move()
            start_pos, end_pos = move.split('-')
            start_col, start_row = ord(start_pos[0]) - ord('a'), int(start_pos[1]) - 1
            end_col, end_row = ord(end_pos[0]) - ord('a'), int(end_pos[1]) - 1

            piece = self.board.board[start_row][start_col]

            if piece == '.':
                print("На этой позиции нет фигуры!")
                continue


            if piece.color != self.board.current_player:
                print("Сейчас не ваш ход.")
                continue


            if not self.board.is_valid_move(start_row, start_col, end_row, end_col):
                print("Не корректный ход.")
                continue


            self.board.move_piece(start_row, start_col, end_row, end_col)
            self.board.print_board()

            if self.board.check_win() == False:
                break


if __name__ == "__main__":
    game = GameLoop()
    game.main()
