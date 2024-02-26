import string

# Классы всех фигур, наследующие от Piece параметры цвета и символа
class Piece:
    def __init__(self, color):
        self.color = color
        self.symbol = '.'

    def __repr__(self):
        return self.symbol


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♟' if color == 'black' else '♙'


    def get_possible_moves(self, board, row, col):
        possible_moves = []
        direction = -1 if self.color == 'white' else 1
        # Проверка для двойного хода из начальной позиции
        if (row == 6 and self.color == 'white') or (row == 0 and self.color == 'black'):
            print('good')
            print(board[row + (2 * direction)][col])
            if board[row + (2 * direction)][col] is '.':
                possible_moves.append((row + 2 * direction, col))
        # Проверка для обычного хода
        if board[row + direction][col] is '.':
            possible_moves.append((row + direction, col))
        # Проверка для атаки по диагонали
        if 0 <= col - 1 < 8 and board[row + direction][col - 1] is not '.':
            possible_moves.append((row + direction, col - 1))
        if 0 <= col + 1 < 8 and board[row + direction][col + 1] is not '.':
            possible_moves.append((row + direction, col + 1))
        #print(possible_moves)
        return possible_moves

    def can_move_only_available_moves(self, board, row, col):
        direction = -1 if self.color == 'white' else 1
        return (row + direction, col) not in self.get_possible_moves(board, row, col)


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♜' if color == 'black' else '♖'


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♞' if color == 'black' else '♘'


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♝' if color == 'black' else '♗'


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♛' if color == 'black' else '♕'


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♚' if color == 'black' else '♔'



class Chessboard:
    def __init__(self):
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        self.initialize_board()
        self.current_player = 'white' 


    def initialize_board(self):
        # Расставляем черные фигуры
        
        self.board[0] = [Rook('black'), Knight('black'), Bishop('black'), Queen('black'),
                         King('black'), Bishop('black'), Knight('black'), Rook('black')]
        self.board[1] = [Pawn('black') for _ in range(8)]
        # Расставляем белые фигуры
        self.board[7] = [Rook('white'), Knight('white'), Bishop('white'), Queen('white'),
                         King('white'), Bishop('white'), Knight('white'), Rook('white')]
        self.board[6] = [Pawn('white') for _ in range(8)]


    def print_board(self):
        letters =  string.ascii_uppercase[:8]
        print('   ',*letters,'    ')
        for i, s in enumerate(self.board):
            print(f'{i+1}  ',*s,f'  {i+1}')
        print('   ',*letters,'    ')


    def is_valid_move(self, start_row, start_col, end_row, end_col):
        piece = self.board[start_row][start_col]

        if not isinstance(piece, Piece):
            return False

        # Проверка наличия фигуры на стартовой позиции
        if piece is None:
            return False

        # Проверка, принадлежит ли фигура текущему игроку
        if piece.color != self.current_player:
            return False

        # Получение возможных ходов для фигуры
        possible_moves = piece.get_possible_moves(self.board, start_row, start_col)
        #print(possible_moves)
        # Проверка, является ли конечная позиция одним из возможных ходов

        if (end_row, end_col) not in possible_moves:
            '''
            print((end_row,end_col))
            print(possible_moves)
            print('!')
            '''
            return False

        # Проверка, может ли фигура передвигаться только на доступные ходы
        if (start_row, start_col) != (end_row, end_col):
            if piece.can_move_only_available_moves(self.board, start_row, start_col):
                print('!')
                return False

        return True


    def move_piece(self, start_row, start_col, end_row, end_col):
        piece = self.board[start_row][start_col]
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = '.'
        self.current_player = 'black' if self.current_player == 'white' else 'white'

# Добавить методы для хода фигуры, проверки наличия шаха и мате, а также для других правил


def get_move():
    while True:
        move = input("Введите ваш ход (например -> 'a2-a4'): ").strip().lower()
        if len(move) == 5 and move[0] in 'abcdefgh' and move[1] in '12345678' and \
           move[2] == '-' and move[3] in 'abcdefgh' and move[4] in '12345678':
           return move
        else:
            print("Не корректный ход. Введите в формате 'a2-a4'.")


def main():
    board = Chessboard()
    board.print_board()

    current_turn = True

    while True:
        move = get_move()
        start_pos, end_pos = move.split('-')
        start_col, start_row = ord(start_pos[0]) - ord('a'), int(start_pos[1]) - 1
        end_col, end_row = ord(end_pos[0]) - ord('a'), int(end_pos[1]) - 1

        piece = board.board[start_row][start_col]

        if piece is None:
            print("На этой позиции нет фигуры!")
            continue

        if not isinstance(piece, Piece):
            print("Не верная фигура.")
            continue

        if piece.color != board.current_player:
            print("Сейчас не ваш ход.")
            continue


        if not board.is_valid_move(start_row, start_col, end_row, end_col):
            print("Не корректный ход.")
            continue

        board.move_piece(start_row, start_col, end_row, end_col)
        board.print_board()


if __name__ == "__main__":
    main()
