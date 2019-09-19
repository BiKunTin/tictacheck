#! /usr/bin/env python

class ChessBoard():
    def Checknum(self):
        #check if 'whoseturn' have full piece or not
        if self.whoseturn == "black":
            myColor = 'b'
            enemyColor = 'w'
        else:
            myColor = 'w'
            enemyColor = 'b'
        k=0
        for row in range(4):
            for col in range(4):
                piece = self.squares[row][col]
                if ('R' in piece or 'P' in piece or 'K' in piece or 'B' in piece) and myColor in piece:
                     k = k+1
        return k;

    def PawnStatus(self):
        #check if 'whosepawn' can turn backwards then turn it
        for col in range(4):
            piece = self.squares[0][col]
            if ('P' in piece) and self.bPdir==-1 and 'b' in piece:
                    self.bPdir==1
            if ('P' in piece) and self.wPdir==-1 and 'w' in piece:
                    self.wPdir==1
        for col in range(4):
            piece = self.squares[3][col]
            if ('P' in piece) and self.bPdir==1 and 'b' in piece:
                    self.bPdir==-1
            if ('P' in piece) and self.wPdir==1 and 'w' in piece:
                    self.wPdir==-1

    def IsInCheck(self):
        #check if 'whoseturn' can win or not
        if self.whoseturn == "black":
            myColor = 'b'
            enemyColor = 'w'
        else:
            myColor = 'w'
            enemyColor = 'b'
        k = self.Checknum();
        currow = -1
        curcol = -1
        avg = -1
        check = 0
        if k == 4:
            for row in range(4):
                for col in range(4):
                    piece = self.squares[row][col]
                    if ('R' in piece or 'P' in piece or 'K' in piece or 'B' in piece) and myColor in piece:
                        if currow == -1:
                            currow = row
                            curcol = col
                        else:
                            if avg == -1: 
                                avg = (abs(currow-row)+1)/(abs(curcol-col)+1)
                            else:
                                if avg != (abs(currow-row)+1)/(abs(curcol-col)+1):
                                    return -1;
                                else:
                                    check = 0
            return 1;
        else:
            return -1;           

    def CheckPut(self):
        if self.whoseturn == "black":
            myColor = 'b'
            enemyColor = 'w'
        else:
            myColor = 'w'
            enemyColor = 'b'
        if myColor == 'b':
            if self.bK == 1 or self.bR==1 or self.bB ==1 or self.bP ==1:
                return 1;
            else:
                return 0;
        else:
            if self.wK == 1 or self.wR==1 or self.wB ==1 or self.wP ==1:
                return 1;
            else:
                return 0;

    def SwitchWhoseTurn(self):
        if self.whoseturn == "black":
            self.whoseturn = "white"
        else:
            self.whoseturn = "black"

    def GetPlayerInput_SquareFrom(self):
        ch = "?"
        cmd_r = 0
        cmd_c = 0
        while (ch not in self.squares[cmd_r][cmd_c] or self.GetListOfValidMoves((cmd_r,cmd_c))==[]):
            print ("Player", self.whoseturn)
            cmd_r = int(input("  From row: "))
            cmd_c = int(input("  From col: "))
            if self.whoseturn == "black":
                ch = "b"
            else:
                ch = "w"
    
            if (self.squares[cmd_r][cmd_c] == 'e'):
                print ("  Nothing there!")
            elif (ch not in self.squares[cmd_r][cmd_c]):
                print ("  That's not your piece!")
            elif self.GetListOfValidMoves((cmd_r,cmd_c)) == []:
                print ("  No valid moves for that piece!")
                
        return (cmd_r,cmd_c)

    def IsClearPath(self,fromTuple,toTuple):
        #Return true if there is nothing in a straight line between fromTuple and toTuple, non-inclusive
        #Direction could be +/- vertical, +/- horizontal, +/- diagonal
        fromSquare_r = fromTuple[0]
        fromSquare_c = fromTuple[1]
        toSquare_r = toTuple[0]
        toSquare_c = toTuple[1]
        fromPiece = self.squares[fromSquare_r][fromSquare_c]

        if abs(fromSquare_r - toSquare_r) <= 1 and abs(fromSquare_c - toSquare_c) <= 1:
            #The base case: just one square apart
            return True
        else:
            if toSquare_r > fromSquare_r and toSquare_c == fromSquare_c:
                #vertical +
                newTuple = (fromSquare_r+1,fromSquare_c)
            
            elif toSquare_r < fromSquare_r and toSquare_c == fromSquare_c:
                #vertical -
                newTuple = (fromSquare_r-1,fromSquare_c)
            
            elif toSquare_r == fromSquare_r and toSquare_c > fromSquare_c:
                #horizontal +
                newTuple = (fromSquare_r,fromSquare_c+1)

            elif toSquare_r == fromSquare_r and toSquare_c < fromSquare_c:
                #horizontal -
                newTuple = (fromSquare_r,fromSquare_c-1)

            elif toSquare_r > fromSquare_r and toSquare_c > fromSquare_c:
                #diagonal "SE"
                newTuple = (fromSquare_r+1,fromSquare_c+1)

            elif toSquare_r > fromSquare_r and toSquare_c < fromSquare_c:
                #diagonal "SW"
                newTuple = (fromSquare_r+1,fromSquare_c-1)

            elif toSquare_r < fromSquare_r and toSquare_c > fromSquare_c:
                #diagonal "NE"
                newTuple = (fromSquare_r-1,fromSquare_c+1)

            elif toSquare_r < fromSquare_r and toSquare_c < fromSquare_c:
                #diagonal "NW"
                newTuple = (fromSquare_r-1,fromSquare_c-1)

                
            if self.squares[newTuple[0]][newTuple[1]] != 'e':
                return False
            else:
                return self.IsClearPath(newTuple,toTuple)
    

    def GetListOfValidMoves(self,fromTuple):
        legalDestinationSpaces = []
        for row in range(4):
            for col in range(4):
                d = (row,col)
                if self.IsLegalMove(fromTuple,d):
                        legalDestinationSpaces.append(d)
        return legalDestinationSpaces

    def IsLegalMove(self,fromTuple,toTuple):
        fromSquare_r = fromTuple[0]
        fromSquare_c = fromTuple[1]
        toSquare_r = toTuple[0]
        toSquare_c = toTuple[1]
        fromPiece = self.squares[fromSquare_r][fromSquare_c]
        toPiece = self.squares[toSquare_r][toSquare_c]

        if self.whoseturn == "black":
            enemyColor = 'w'
        if self.whoseturn == "white":
            enemyColor = 'b'

        if fromTuple == toTuple:
            return False
        
        if "P" in fromPiece:
            #Pawn
            if self.whoseturn == "black":
                if toSquare_r == fromSquare_r+1 and toSquare_c == fromSquare_c and toPiece == 'e':
                    #moving forward one space
                    return True
                if self.bPdir ==1 and toSquare_r == fromSquare_r+1 and (toSquare_c == fromSquare_c+1 or toSquare_c == fromSquare_c-1) and enemyColor in toPiece:
                    #attacking forward
                    return True
                if self.bPdir ==-1 and toSquare_r == fromSquare_r-1 and (toSquare_c == fromSquare_c+1 or toSquare_c == fromSquare_c-1) and enemyColor in toPiece:
                    #attacking backward
                    return True

            elif self.whoseturn == "white":
                if toSquare_r == fromSquare_r-1 and toSquare_c == fromSquare_c and toPiece == 'e':
                    #moving forward one space
                    return True
                if self.wPdir ==1 and toSquare_r == fromSquare_r+1 and (toSquare_c == fromSquare_c+1 or toSquare_c == fromSquare_c-1) and enemyColor in toPiece:
                    #attacking forward
                    return True
                if self.wPdir ==-1 and toSquare_r == fromSquare_r-1 and (toSquare_c == fromSquare_c+1 or toSquare_c == fromSquare_c-1) and enemyColor in toPiece:
                    #attacking backward
                    return True
                
        elif "R" in fromPiece:
            #Rook
            if (toSquare_r == fromSquare_r or toSquare_c == fromSquare_c) and (toPiece == 'e' or enemyColor in toPiece):
                if self.IsClearPath(fromTuple,toTuple):
                    return True

        elif "K" in fromPiece:
            #Knight
            col_diff = toSquare_c - fromSquare_c
            row_diff = toSquare_r - fromSquare_r
            if toPiece == 'e' or enemyColor in toPiece:
                if col_diff == 1 and row_diff == -2:
                    return True
                if col_diff == 2 and row_diff == -1:
                    return True
                if col_diff == 2 and row_diff == 1:
                    return True
                if col_diff == 1 and row_diff == 2:
                    return True
                if col_diff == -1 and row_diff == 2:
                    return True
                if col_diff == -2 and row_diff == 1:
                    return True
                if col_diff == -2 and row_diff == -1:
                    return True
                if col_diff == -1 and row_diff == -2:
                    return True

        elif "B" in fromPiece:
            #Bishop
            if ( abs(toSquare_r - fromSquare_r) == abs(toSquare_c - fromSquare_c) ) and (toPiece == 'e' or enemyColor in toPiece):
                if self.IsClearPath(fromTuple,toTuple):
                    return True
        return False #if none of the other "True"s are hit above

    def GetPlayerInput_SquareTo(self,fromTuple):
        toTuple = ('x','x')

        validMoveList = self.GetListOfValidMoves(fromTuple)
        
        print ("List of valid moves for piece at",fromTuple,": ", validMoveList)
        
        while (not toTuple in validMoveList):
            cmd_r = int(input("  To row: "))
            cmd_c = int(input("  To col: "))
            toTuple = (cmd_r,cmd_c)
            if not toTuple in validMoveList:
                print ("  Invalid move!")
                
        return toTuple

    def GetPlayerInput(self):
        toTuple = (999,999)
        while toTuple == (999,999):
            fromTuple = self.GetPlayerInput_SquareFrom()
            toTuple = self.GetPlayerInput_SquareTo(fromTuple)

        return (fromTuple,toTuple)

    def MakeMove(self,moveTuple):
        fromSquare_r = moveTuple[0][0]
        fromSquare_c = moveTuple[0][1]
        toSquare_r = moveTuple[1][0]
        toSquare_c = moveTuple[1][1]

        fromPiece = self.squares[fromSquare_r][fromSquare_c]
        toPiece = self.squares[toSquare_r][toSquare_c]


        print (fromPiece, "moves from square ("+str(fromSquare_r)+","+str(fromSquare_c)+") to square ("+str(toSquare_r)+","+str(toSquare_c)+")")
        if toPiece != 'e':
            print (fromPiece,"captures",toPiece+"!")
            if toPiece == 'bB':
                self.bB=1;
            if toPiece == 'bK':
                self.bK=1;
            if toPiece == 'bR':
                self.bR=1;
            if toPiece == 'bP':
                self.bP=1;
            if toPiece == 'wB':
                self.wB=1;
            if toPiece == 'wK':
                self.wK=1;
            if toPiece == 'wR':
                self.wR=1;
            if toPiece == 'wP':
                self.wP=1;
            
        self.squares[toSquare_r][toSquare_c] = fromPiece
        self.squares[fromSquare_r][fromSquare_c] = 'e'
    
    def PutPiece(self):
        print ("Player", self.whoseturn)
        if self.whoseturn == "black":
            ch = "b"
        else:
            ch = "w"
        check = 0
        check1 = 0
        while (check1 == 0):
            while (check == 0):
                cmd_p = str(input("  Add piece (B = Bishop, K = Knight, P = Pawn, R = Rook) to the table "))
                if cmd_p == 'B' or cmd_p == 'b':
                    cmd_p='B'
                    if ch == "b":
                        if self.bB==1:
                            self.bB=0
                            check = 1
                        else:
                            print ("There is no Bishop")
                    else:
                        if self.wB==1:
                            self.wB=0
                            check = 1
                        else:
                            print ("There is no Bishop")
                elif cmd_p == 'R' or cmd_p == 'r':
                    cmd_p='R'
                    if ch == "b":
                        if self.bR==1:
                            self.bR=0
                            check = 1
                        else:
                            print ("There is no Rook")
                    else:
                        if self.wR==1:
                            self.wR=0
                            check = 1
                        else:
                            print ("There is no Rook")
                elif cmd_p == 'P' or cmd_p == 'p':
                    cmd_p='P'
                    if ch == "b":
                        if self.bP==1:
                            self.bP=0
                            check = 1
                        else:
                            print ("There is no Pawn")
                    else:
                        if self.wP==1:
                            self.wP=0
                            check = 1
                        else:
                            print ("There is no Pawn")
                elif cmd_p == 'K' or cmd_p == 'k':
                    cmd_p='K'
                    if ch == "b":
                        if self.bK==1:
                            self.bK=0
                            check = 1
                        else:
                            print ("There is no Knight")
                    else:
                        if self.wK==1:
                            self.wK=0
                            check = 1
                        else:
                            print ("There is no Knight")
                else:
                    print ("Invalid Input")

            cmd_r = int(input("  To row: "))
            cmd_c = int(input("  To col: "))
            if (self.squares[cmd_r][cmd_c] == 'e'):
                self.squares[cmd_r][cmd_c]=str(ch+cmd_p)
                check1=1
            else:
                print ("Cannot move piece here")

    def SetUpBoard(self,opt):
        if opt == 0:
            self.squares[0] = ['e','e','e','e']
            self.squares[1] = ['e','e','e','e']
            self.squares[2] = ['e','e','e','e']
            self.squares[3] = ['e','e','e','e']
      
    def Draw(self):
        print ("    c0   c1   c2   c3    ")
        print ("  -----------------------  ")
        for r in range(4):
            print ("r"+str(r)+"|",end=' ')
            for c in range(4):
                if self.squares[r][c] != 'e':
                    print  (str(self.squares[r][c]), "|",end=' ')
                else:
                    print ("   |",end=' ')
                if c == 3:
                    print #to get a new line
            print (" \n -----------------------  ")

    def MainLoop(self):
        print ("Starting Chess...")
        self.whoseturn = "black"
        
        self.SetUpBoard(0)#make sure arg is 0 for standard set-up
        
        while self.IsInCheck() != 1:
            self.Draw()
            if self.CheckPut()== 1:
                if self.move >= 6:
                    keypres = int(input(" Press 1 to put piece, Press 2 to move piece: "))
                    if keypres == 2:
                        move1 = self.GetPlayerInput()
                        self.MakeMove(move1)
                    else:
                        self.PutPiece()
                else:
                    self.PutPiece()
            else:
                move1 = self.GetPlayerInput()
                self.MakeMove(move1)
            self.move = self.move +1
            self.PawnStatus()
            self.SwitchWhoseTurn()

        self.Draw() #draw board a final time to show the end game setup
        print ("Player ",self.whoseturn," has lost the match!")
        
    def __init__(self):
        self.squares = [['e','e','e','e'],['e','e','e','e'],['e','e','e','e'],['e','e','e','e']]
        self.bK=1
        self.bR=1
        self.bP=1
        self.bB=1
        self.wR=1
        self.wK=1
        self.wP=1
        self.wB=1
        self.move=0
        self.bPdir=1
        self.wPdir=-1


if __name__ == "__main__":
    b = ChessBoard()
    b.MainLoop()
