class BoardException(Exception):
    def __init__(self, message):
        self._message = message

    def __str__(self):
        return self._message


class OutOfBoundsException(BoardException):
    def __init__(self):
        super().__init__("This position is out of bounds")


class ColumnFilledException(BoardException):
    def __init__(self):
        super().__init__("This column is filled")
