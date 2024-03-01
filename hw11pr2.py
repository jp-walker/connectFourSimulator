# Filename: hw11pr2.py
# Name: JP Walker

import random
print("you're now opening hw11pr2.py")
class Board:
    """A data type representing a Connect-4 board
       with an arbitrary number of rows and columns.
    """

    def __init__(self, width, height):
        """Construct objects of type Board, with the given width and height."""
        self.width = width
        self.height = height
        self.data = [[' ']*width for row in range(height)]

        # We do not need to return anything from a constructor!

    def __repr__(self):
        """This method returns a string representation
           for an object of type Board.
        """
        s = '' 
        n = ''
        string = ''
                                 # The string to return
        for row in range(0, self.height):
            s += '|'
            for col in range(0, self.width):
                s += self.data[row][col] + '|'
            s += '\n'

        s += (2*self.width + 1) * '-'   # Bottom of the board

        for n in range(self.width):
            n = " " + str(n)
            string += n

        return s + "\n" + string      # The board is complete; return it

    def addMove(self, col, ox):
        """takes two arguments: col, represents the index of the column to which the checker will be added. 
        ox is a 1-character string representing the checker to add to the board. 
        ox should either be 'X' or 'O' (capital O, not zero)"""
        H = self.height

        for row in range(0,H):
            if self.data[row][col] != ' ':
                self.data[row-1][col] = ox
                return

        self.data[H-1][col] = ox

    def clear(self):
        """clears all 'X's or 'O's from the board self"""
        H = self.height
        
        for row in range(0,H):
            for col in range(self.width):
                if self.data[row][col] != ' ':
                    self.data[row][col] = " "
        return

    def setBoard(self, moveString):
        """Accepts a string of columns and places
           alternating checkers in those columns,
           starting with 'X'.

           For example, call b.setBoard('012345')
           to see 'X's and 'O's alternate on the
           bottom row, or b.setBoard('000000') to
           see them alternate in the left column.

           moveString must be a string of one-digit integers.
        """
        nextChecker = 'X'   # start by playing 'X'
        for colChar in moveString:
            col = int(colChar)
            if 0 <= col <= self.width:
                self.addMove(col, nextChecker)
            if nextChecker == 'X':
                nextChecker = 'O'
            else:
                nextChecker = 'X'

    def allowsMove(self, c):
        """checks if c is within the range from 0 to the last column and if
        there is still room left in the column.
        return True if the calling object (of type Board) does allow a move into column c. 
        returns False if column c is not a legal column number for the calling object. 
        also returns False if column c is full."""
        if c >= self.width or c < 0:
            return False
        elif c <= self.width and self.data[0][c] == " ":
            return True
        else:
            return False

    def isFull(self):
        """returns True if the calling object (of type Board) is completely full of checkers. 
        returns False otherwise"""
        result = True

        for col in range(self.width):
            if self.allowsMove(col):
                return False
        return result
    
    def delMove(self, c):
        """"removes the top checker from the column c. 
        If the column is empty, delMove does nothing"""
        H = self.height

        for row in range(0,H):
            if self.data[row][c] != ' ':
                self.data[row][c] = " "
                return


    def winsFor(self, ox):
        """argument ox is a 1-character checker: either 'X' or 'O'. 
        returns True if there are four checkers of type ox in a row on the board. 
        returns False otherwise. checks horizontally, vertically, and diagonally"""
        H = self.height
        W = self.width
        D = self.data

        for row in range(H):
            for col in range(W):
                if inarow_Neast(ox, row, col, D, 4):
                    return True
                elif inarow_Nsouth(ox, row, col, D, 4):
                    return True
                elif inarow_Nsoutheast(ox, row, col, D, 4):
                    return True
                elif inarow_Nnortheast(ox, row, col, D, 4):
                    return True
        return False 

    def hostGame(self): 
        """hosts a game of Connect Four, using the methods listed above. 
        alternates turns between 'X' (who will always go first) and 'O' (who will always go second). 
        asks the user (with the input function) to select a column number for each move."""
        print("Welcome to the world championships of connect 4!")
        print(self)
        playerX = input("who is playing the X's? ")
        print("and O's are played by the all-knowing COMPUTER CHAMP!!")
        playerO = "The Computer Champ"

        while True:
            XC = int(input("X's choice: "))
            while not self.allowsMove(XC):
                XC = int(input("try again. X's choice: "))
            self.addMove(XC, "X")
            if self.winsFor("X"):
                print("congratulations to our world champion,", playerX)
                print(self)
                break
            elif self.isFull():
                print("the board's full and no one has won... it's a tie")
                print(self)
                break
            print(self)
            OC = self.aiMove("O")
            print("the COMPUTER CHAMP's choice is : ", OC)
            self.addMove(OC, "O")
            if self.winsFor("O"):
                print("congratulations to our world champion,", playerO)
                print(self)
                break
            elif self.isFull():
                print("the board's full and no one has won... it's a tie")
                print(self)
                break
            print(self)




            """if self.winsFor("X"):
                print("congratulations to our worldchampion, ", playerX)
            elif self.winsFor("O"):
                print("congratulations to our worldchampion, ", playerO)
            else:
                print("it's a tie!")
                 while not self.allowsMove(OC):
                OC = int(input("try again. O's choice: "))
            self.addMove(OC, "O")"""
    


    # start of new functions 


    def colsToWin(self, ox):
        """takes one argument of a string that is either X or O.
        returns a list of columns that the argument can move in the
        next turn to win and finish the game. columns appear in numeric order 
        if multiple. does not look ahead farther than one turn."""
        L = []
        for col in range(self.width):
            if self.allowsMove(col):
                self.addMove(col, ox)
                if self.winsFor(ox):
                    L += [col]
                self.delMove(col)
        return L

    def aiMove(self, ox):
        """takes one argument, ox, which is either "X" or "O". returns single
        integer indicating which column it will choose to addMove() to, which will
        be approved by allowsMove(). 
        if ox can win in the next turn, it will make that move.
        if the opponant can win in the next turn, it will block it.
        if neither of these are true, it will"""

        no_op = 0 

        if ox == "X":
            other = "O"
        else:
            other = "X"

        for col in [3,4,2,5,1,6,0]:
            if not self.allowsMove(col):
                no_op
            else: 
                if len(self.colsToWin(ox)) >= 1:
                    print(232)
                    return random.choice(self.colsToWin(ox))
                elif len(self.colsToWin(other)) >= 1:
                    print(236)
                    return random.choice(self.colsToWin(other))
                else:
                    print(240)
                    return col








"""
If there is a way for ox to win, then aiMove MUST return that move (that column number). It must win when it can. There may be more than one way to win: in this case, any one of those winning column moves may be returned.
If there is NO way for ox to win, but there IS a way for ox to block the opponent's four-in-a-row, then aiMove MUST return a move that blocks its opponent's four-in-a-row. Again, it should not look more than one move ahead for its opponent. If there are no wins, but multiple ways to block the opponent, then aiMove should return any one of those ways to block the opponent. (Even though the opponent might win in a different way.)
If there is NO way for ox to win NOR a way for ox to block the opponent from winning, then aiMove should return a move of your (the programmer's) choice—but it must be a legal move. We won't call aiMove when the board is full.
"""




b = Board(7,6)




def inarow_Neast(ch, r_start, c_start, A, N):
    """starts from r_start and c_start and checks for N-in-a-row eastward of element ch, 
    returning True or False, as appropriate."""
    result = False
    if c_start + N - 1 >= len(A[0]):
        return False
    for n in range(N):
        if A[r_start][c_start+n] == ch:
            result = True
        else:
            return False
    return result


def inarow_Nsouth(ch, r_start, c_start, A, N):
    """starts from r_start and c_start and checks for N-in-a-row southward of element ch, 
    returning True or False, as appropriate."""
    result = False
    if r_start + N - 1 >= len(A):
        return False
    for n in range(N):
        if A[r_start+n][c_start] == ch:
            result = True
        else:
            return False
    return result

def inarow_Nsoutheast(ch, r_start, c_start, A, N):
    """starts from r_start and c_start and checks for N-in-a-row southeastward of element ch, 
    returning True or False, as appropriate."""
    result = False
    if r_start + N - 1 >= len(A) or c_start + N -1 >= len(A[0]):
        return False
    for n in range(N):
        if A[r_start+n][c_start+n] == ch:
            result = True
        else:
            return False
    return result

def inarow_Nnortheast(ch, r_start, c_start, A, N):
    """starts from r_start and c_start and checks for N-in-a-row northeastward of element ch, 
    returning True or False, as appropriate."""
    result = False
    if r_start - N + 1 <= 0 or c_start + N > (len(A[0]) + 1):
        return False
    for n in range(N):
        if A[r_start-n][c_start+n] == ch:
            result = True
        else:
            return False
    return result