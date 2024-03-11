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

        if isinstance(piece,King.King) or isinstance(piece, Rook.Rook):
            piece.has_moved = True
            print(piece.has_moved)

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

        if king_row is not None:
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

    def check_mat_for_rakirivcka(self,king_row,king_col,color):
        king = self.board[king_row][king_col]

        # Проверяем, находится ли король под ударом
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != '.' and piece.color != color:
                    if (king_row, king_col) in piece.get_possible_moves(self.board, row, col):
                        return False

        return True

    def check_rakirovka(self,type_rakirovka,color):
        if color == 'white' and self.current_player == 'white':
            if type_rakirovka == 'shortR':
                if isinstance(self.board[7][4], King.King) and isinstance(self.board[7][7],Rook.Rook) and (self.board[7][5] == '.') and (self.board[7][6] == '.') and (self.check_mat_for_rakirivcka(7,6,'white')):
                    if self.board[7][4].has_moved == False and self.board[7][7].has_moved == False:
                        if self.check_shah('white')!=True:
                            return True
            if type_rakirovka == 'longR':
                if isinstance(self.board[7][4], King.King) and isinstance(self.board[7][0],Rook.Rook) and (self.board[7][3] == '.') and (self.board[7][3] == '.') and (self.board[7][1] == '.') (self.check_mat_for_rakirivcka(7,2,'white')):
                    if self.board[7][4].has_moved == False and self.board[7][0].has_moved == False:
                        if self.check_shah('white')!=True:
                            return True

        if color == 'black' and self.current_player == 'black':
            if type_rakirovka == 'shortR':
                if isinstance(self.board[0][4], King.King) and isinstance(self.board[0][7],Rook.Rook) and (self.board[0][5] == '.') and (self.board[0][6] == '.') and (self.check_mat_for_rakirivcka(0,4,'black')):
                    if self.board[0][4].has_moved == False and self.board[0][7].has_moved == False:
                        if self.check_shah('black')!=True:
                            return True
            if type_rakirovka == 'longR':
                if isinstance(self.board[0][4], King.King) and isinstance(self.board[0][0],Rook.Rook) and (self.board[0][3] == '.') and (self.board[0][3] == '.') and (self.board[0][1] == '.') and (self.check_mat_for_rakirivcka(0,2,'black')):
                    if self.board[0][4].has_moved == False and self.board[0][0].has_moved == False:
                        if self.check_shah('black')!=True:
                            return True
                    

    def rakirovka(self,type_rakirovka,color):
        if color == 'white':
            if type_rakirovka == 'shortR':
                self.board[7][4] = '.'
                self.board[7][6] = King.King('white')
                self.board[7][7] = '.'
                self.board[7][5] = Rook.Rook('white')
                self.current_player = 'black' if self.current_player == 'white' else 'white' # смена цвета игрока после ракировки 
            if type_rakirovka == 'longR':
                self.board[7][4] = '.'
                self.board[7][2] = King.King('white')
                self.board[7][0] = '.'
                self.board[7][3] = Rook.Rook('white')
                self.current_player = 'black' if self.current_player == 'white' else 'white' # смена цвета игрока после ракировки 

        if color == 'black':
            if type_rakirovka == 'shortR':
                self.board[0][4] = '.'
                self.board[0][6] = King.King('blask')
                self.board[0][7] = '.'
                self.board[0][5] = Rook.Rook('black')
                self.current_player = 'black' if self.current_player == 'white' else 'white' # смена цвета игрока после ракировки 
            if type_rakirovka == 'longR':
                self.board[0][4] = '.'
                self.board[0][2] = King.King('black')
                self.board[0][0] = '.'
                self.board[0][3] = Rook.Rook('black')
                self.current_player = 'black' if self.current_player == 'white' else 'white' # смена цвета игрока после ракировки 
                



# Класс с игровым циклом
class GameLoop:
    def __init__(self):
        self.board = Chessboard()

    # Получение координат (хода) откуда и куда 
    def get_move(self):
        while True:
            move = input("Введите ваш ход (например -> 'a2-a4'): ").strip()
            if move == 'shortR':
                return 'shortR'
            if move == 'longR':
                return 'longR'
            if len(move) == 5 and move[0] in 'abcdefgh' and move[1] in '12345678' and move[2] == '-' and move[3] in 'abcdefgh' and move[4] in '12345678':
                return move
            else:
                print("Не корректный ход. Введите в формате 'a2-a4'.")


    def main(self):
        self.board.print_board()

        while True:
            move = self.get_move()

            if move != 'shortR' and move != 'longR':
                azbuka = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}

                start_pos, end_pos = move.split('-')
                
                #start_col = ord(start_pos[0]) - ord('a')
                start_col = azbuka[start_pos[0]]
                start_row = int(start_pos[1]) - 1

                #end_col = ord(end_pos[0]) - ord('a') 
                end_col = azbuka[end_pos[0]]
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
            else:
                if move == 'shortR':
                    if self.board.check_rakirovka(move, self.board.current_player):
                        self.board.rakirovka('shortR',self.board.current_player)
                    else:
                        print('Короткая Ракировка невозможна!')
                if move == 'longR':
                    if self.board.check_rakirovka(move, self.board.current_player):
                        self.board.rakirovka('longR',self.board.current_player)
                    else:
                        print('Длинная Ракировка невозможна!')


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