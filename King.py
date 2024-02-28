import Piece

class King(Piece.Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♚' if color == 'black' else '♔'


    def get_possible_moves(self, board, row, col):
        possible_moves = []

        # Все возможные соседние клетки короля
        neighbor_cells = [
            (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
            (row, col - 1),                         (row, col + 1),
            (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)
        ]

        # Проверяем каждую соседнюю клетку
        for r, c in neighbor_cells:
            # Проверяем, находится ли клетка в пределах доски и свободна ли она
            if 0 <= r < 8 and 0 <= c < 8 and (board[r][c] == '.' or board[r][c].color != self.color):
                possible_moves.append((r, c))

        return possible_moves