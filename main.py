import string

import Piece, Pawn, Rook, Knight, Bishop, Queen, King
# Классы всех фигур, наследующие от Piece параметры цвета и символа

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
        #print(possible_moves)
        # Проверка, является ли конечная позиция одним из возможных ходов

        if (end_row, end_col) not in possible_moves:
            return False


        return True


    def move_piece(self, start_row, start_col, end_row, end_col):
        piece = self.board[start_row][start_col]
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = '.'
        self.current_player = 'black' if self.current_player == 'white' else 'white'

# Добавить методы для проверки наличия шаха и мате, а также для других правил


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

        if piece == '.':
            print("На этой позиции нет фигуры!")
            continue

        if not isinstance(piece, Piece.Piece):
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
