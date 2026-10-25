from src.exceptions.exceptions import OutOfBoundsException, ColumnFilledException


class Board:
    def __init__(self):
        self.rows=6
        self.cols=7
        self.grid=[[0 for _ in range(self.cols)] for _ in range(self.rows)]

    '''@property
    def cols(self):
        return self.cols

    @property
    def rows(self):
        return self.rows

    @property
    def grid(self):
        return self.grid'''

    def drop_piece(self,col,player):
        """
        a function which drops a piece into the board in
        a specified column for a specific player
        :param col: int: number of the column
        :param player: int: number of the player
        raises OutOfBoundsException when col is out of bounds
        raises ColumnFilledException when col is filled

        :return: int: row that the piece was dropped
        """
        if col < 0 or col >= self.cols:
            raise OutOfBoundsException()

        if self.grid[0][col] !=0:
            raise ColumnFilledException()

        for row in range(self.rows - 1, -1,-1):
            if self.grid[row][col] ==0:
                self.grid[row][col]=player
                return row


    def is_column_full(self,col):
        """
        function which checks if a column is full
        :param col: int: number of the column
        :return: boolean: true if column is full, False otherwise
        """
        return self.grid[0][col]!=0

    def check_winner(self):
        """
        function which checks if there is a winner by checking
        all the directions: horizontal, vertical, diagonal(2 directions)
        if it finds 4 continuous numbers for the same player(1 or 2) then it is a win

        :return:int : number of the player who won(1,2) or 0 in case no one won
        """
        # Horizontal
        for row in range(self.rows):
            for col in range(self.cols-3):
                if self.grid[row][col]!=0 and\
                    self.grid[row][col]==self.grid[row][col+1] == \
                    self.grid[row][col+2]==self.grid[row][col+3]:
                    return self.grid[row][col]

        #Vertical
        for row in range(self.rows-3):
            for col in range(self.cols):
                if self.grid[row][col]!=0 and\
                    self.grid[row][col]== self.grid[row+1][col] ==\
                        self.grid[row+2][col] == self.grid[row+3][col]:
                    return self.grid[row][col]

        # Diagonal(down-right)
        for row in range(self.rows-3):
            for col in range(self.cols-3):
                if self.grid[row][col] != 0 and \
                        self.grid[row][col] == self.grid[row + 1][col+1] == \
                        self.grid[row + 2][col+2] == self.grid[row + 3][col+3]:
                    return self.grid[row][col]

        # Diagonal (down-left)
        for row in range(self.rows-3):
            for col in range(self.cols):
                if self.grid[row][col] != 0 and \
                        self.grid[row][col] == self.grid[row + 1][col-1] == \
                        self.grid[row + 2][col-2] == self.grid[row + 3][col-3]:
                    return self.grid[row][col]

        return 0

    def is_full(self):
        """
        checks if the board is completely full and no other moves can be made
        :return: boolean
        """
        return all(self.grid[0][col]!=0 for col in range(self.cols))

    def __str__(self):
        symbols={0:'.',1:'X',2:'O'}
        lines=[]
        for row in self.grid:
            lines.append(' '.join(symbols[cell] for cell in row))
        lines.append(' '.join(str(i+1) for i in range (self.cols)))
        return '\n'.join(lines)








