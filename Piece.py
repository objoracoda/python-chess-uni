class Piece:
    def __init__(self, color):
        self.color = color
        self.symbol = '.'

    # Метод __repr__ в Python выдает текстовое или строковое представление сущности или объекта. Для отрисовки
    def __repr__(self):
        return self.symbol
