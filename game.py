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

    # Двигаем фигуру
    def move_piece(self, start_row, start_col, end_row, end_col):
        piece = self.board[start_row][start_col]
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = '.'

        #  Проверка на преварщение в королеву пешки
        if isinstance(piece,Pawn.Pawn):
            if end_row == 0:
                # Ищем белую королеву на доске
                queen_exists = any(isinstance(piece, Queen.Queen) and piece.color == 'white' for row in self.board for piece in row)
                # Если нет белой королевы
                if queen_exists == False:
                    self.board[end_row][end_col] = Queen.Queen('white')

            if end_row == 7:
                # Ищем черную королеву на доске
                queen_exists = any(isinstance(piece, Queen.Queen) and piece.color == 'black' for row in self.board for piece in row)
                # Если нет черной королевы
                if queen_exists == False:
                    self.board[end_row][end_col] = Queen.Queen('black')

        self.current_player = 'black' if self.current_player == 'white' else 'white' # смена цвета игрока


    def check_win(self,color):
        # Ищем короля нужного цвета на доске
        
        king_row, king_col = None, None
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if isinstance(piece, King.King) and piece.color == color:
                    king_row, king_col = row, col
                    break

        king = self.board[king_row][king_col]
        # Получаем все возможные ходы короля
        king_moves = king.get_possible_moves(self.board,king_row,king_col)
        other_moves = []

        # Проверяем, находится ли король под ударом
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != '.' and piece.color != color:
                    if (king_row, king_col) in piece.get_possible_moves(self.board, row, col):
                        for moves in piece.get_possible_moves(self.board, row, col):
                            other_moves.append(moves)

        if set(king_moves).issubset(other_moves) and len(other_moves) != 0:
            return False

        # Если все хорошо, мата нет!
        return True

    def check_shah(self,color):
        # Проверяем наличие короля нужного цвета на доске
        
        king_row, king_col = None, None
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if isinstance(piece, King.King) and piece.color == color:
                    king_row, king_col = row, col
                    break

        king = self.board[king_row][king_col]
        # Получаем все возможные ходы короля
        king_moves = king.get_possible_moves(self.board,king_row,king_col)
        other_moves = []

        # Проверяем, находится ли король под ударом
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != '.' and piece.color != color:
                    if (king_row, king_col) in piece.get_possible_moves(self.board, row, col):
                        return True

        return False

# Класс с игровым циклом
class GameLoop:
    def __init__(self):
        self.board = Chessboard()

    # Получение координат (хода) откуда и куда 
    def get_move(self):
        while True:
            move = input("Введите ваш ход (например -> 'a2-a4'): ").strip().lower()
            if len(move) == 5 and move[0] in 'abcdefgh' and move[1] in '12345678' and move[2] == '-' and move[3] in 'abcdefgh' and move[4] in '12345678':
                return move
            else:
                print("Не корректный ход. Введите в формате 'a2-a4'.")


    def main(self):
        # Рисуем доску вначале игры
        self.board.print_board()

        # Основной цикл игры
        while True:
            move = self.get_move()
            start_pos, end_pos = move.split('-')
            start_col = ord(start_pos[0]) - ord('a')
            start_row = int(start_pos[1]) - 1

            end_col = ord(end_pos[0]) - ord('a') 
            end_row = int(end_pos[1]) - 1

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


            if self.board.check_win('black') == False:
                print('Мат! Black lose')
                break

            if self.board.check_win('white') == False:
                print('Мат! White lose')
                break

            if self.board.check_shah('black') == True:
                print('Шах для черных!')

            if self.board.check_shah('white') == True:
                print('Шах для белых!')


game = GameLoop()
game.main()