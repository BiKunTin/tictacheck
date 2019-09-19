import os
import random
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
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

    def GetPlayerInput(self,frow,fcol,trow,tcol):
        ch = "?"
        cmd_r = 0
        cmd_c = 0
        cmd_rt =0
        cmd_ct =0
        check =0
        check1 =0
        check2 =0
        while( check ==0):
            check1=1
            check2=1
            #print " From row + col to row + col",
            #cmd_k =str(raw_input())
            cmd_r,cmd_c,cmd_rt,cmd_ct = frow,fcol,trow,tcol
            if self.whoseturn == "black":
                ch = "b"
            else:
                ch = "w"
            fromTuple = (cmd_r,cmd_c)
            if (self.squares[cmd_r][cmd_c] == 'e'):
                print "  Nothing there!"
                check1=0
            elif (ch not in self.squares[cmd_r][cmd_c]):
                print "  That's not your piece!"
                check1=0
            elif self.GetListOfValidMoves((cmd_r,cmd_c)) == []:
                print "  No valid moves for that piece!"
                check1=0
            validMoveList = self.GetListOfValidMoves(fromTuple)
            toTuple = (cmd_rt,cmd_ct)
            if not toTuple in validMoveList:
                print "  Invalid move!"
                check2=0
            if(check1==1 and check2==1):
                check=1
        return (fromTuple,toTuple)

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


    def MakeMove(self,moveTuple):
        fromSquare_r = moveTuple[0][0]
        fromSquare_c = moveTuple[0][1]
        toSquare_r = moveTuple[1][0]
        toSquare_c = moveTuple[1][1]

        fromPiece = self.squares[fromSquare_r][fromSquare_c]
        toPiece = self.squares[toSquare_r][toSquare_c]


        print fromPiece, "moves from square ("+str(fromSquare_r)+","+str(fromSquare_c)+") to square ("+str(toSquare_r)+","+str(toSquare_c)+")"
        if toPiece != 'e':
            print fromPiece,"captures",toPiece+"!"
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
    
    def PutPiece(self,piece,trow,tcol):
        if self.whoseturn == "black":
            ch = "b"
        else:
            ch = "w"
        check1 = 0
        while (check1 == 0):
            check = 0
            #print ("  Add piece (B = Bishop, K = Knight, P = Pawn, R = Rook) to the row + col:"),
            cmd_p,cmd_r,cmd_c = piece,trow,tcol
            if cmd_p == 'B' or cmd_p == 'b':
                cmd_p='B'
                if ch == "b":
                    if self.bB==1:
                        #self.bB=0
                        check = 1
                    else:
                        print "There is no Bishop"
                else:
                    if self.wB==1:
                        #self.wB=0
                        check = 1
                    else:
                        print "There is no Bishop"
            elif cmd_p == 'R' or cmd_p == 'r':
                cmd_p='R'
                if ch == "b":
                    if self.bR==1:
                        #self.bR=0
                        check = 1
                    else:
                        print "There is no Rook"
                else:
                    if self.wR==1:
                        #self.wR=0
                        check = 1
                    else:
                        print "There is no Rook"
            elif cmd_p == 'P' or cmd_p == 'p':
                cmd_p='P'
                if ch == "b":
                    if self.bP==1:
                        #self.bP=0
                        check = 1
                    else:
                        print "There is no Pawn"
                else:
                    if self.wP==1:
                        #self.wP=0
                        check = 1
                    else:
                        print "There is no Pawn"
            elif cmd_p == 'K' or cmd_p == 'k':
                cmd_p='K'
                if ch == "b":
                    if self.bK==1:
                        #self.bK=0
                        check = 1
                    else:
                        print "There is no Knight"
                else:
                    if self.wK==1:
                        #self.wK=0
                        check = 1
                    else:
                        print "There is no Knight"
            else:
                print "Invalid Input"
            if (self.squares[cmd_r][cmd_c] == 'e'):
                if check==1:
                    self.squares[cmd_r][cmd_c]=str(ch+cmd_p)
                    check1=1
                    if cmd_p == 'B':
                        if ch == "b":
                            self.bB=0
                        else:
                            self.wB=0
                    elif cmd_p == 'R':
                        if ch == "b":
                            self.bR=0
                        else:
                            self.wR=0
                    elif cmd_p == 'P':
                        if ch == "b":
                            self.bP=0
                        else:
                            self.wP=0
                    elif cmd_p == 'K':
                        if ch == "b":
                            self.bK=0
                        else:
                            self.wK=0
            else:
                print "Cannot move piece here"
    def AllMove(self):
        if self.whoseturn == "black":
            myColor = 'b'
            enemyColor = 'w'
        else:
            myColor = 'w'
            enemyColor = 'b'
        count = 0
        if myColor == 'b':
            if self.bB==1 or self.bK==1 or self.bR==1 or self.bP==1:
                print 'Can add',
                if self.bB==1:
                    print 'Bishop,',
                if self.bK==1:
                    print 'Knight,',
                if self.bP==1:
                    print 'Pawn,',
                if self.bR==1:
                    print 'Rook,',
                print
                print ' List of valid square to put piece:',
                for row in range(4):
                        for col in range(4):
                            d = (row,col)
                            if self.squares[row][col] == 'e':
                                count=0
                                print d,
                print
        else:
            if self.wB==1 or self.wK==1 or self.wR==1 or self.wP==1:
                print 'Can add',
                if self.wB==1:
                    print 'Bishop,',
                if self.wK==1:
                    print 'Knight,',
                if self.wP==1:
                    print 'Pawn,',
                if self.wR==1:
                    print 'Rook',
                print
                print 'List of valid square to put piece:',
                for row in range(4):
                        for col in range(4):
                            d=(row,col)
                            if self.squares[row][col] == 'e':
                                count=0
                                print d,
                print
        for row in range(4):
            for col in range(4):
                d = (row,col)
                if self.squares[row][col] != 'e' and myColor in self.squares[row][col]:
                    validMoveList = self.GetListOfValidMoves(d)
                    count = count +len(validMoveList)
                    print "List of valid moves for piece at",d,": ", validMoveList
        return count

    def SetUpBoard(self,opt):
        if opt == 0:
            self.squares[0] = ['e','e','e','e']
            self.squares[1] = ['e','e','e','e']
            self.squares[2] = ['e','e','e','e']
            self.squares[3] = ['e','e','e','e']
      
    def Draw(self):
        os.system('clear')
        countb = 0
        countw = 0
        if self.bP==1:
            countb = countb +1
        if self.bB==1:
            countb = countb +1
        if self.bK==1:
            countb = countb +1
        if self.bR==1:
            countb = countb +1
        if self.wP==1:
            countw = countw +1
        if self.wB==1:
            countw = countw +1
        if self.wK==1:
            countw = countw +1
        if self.wR==1:
            countw = countw +1
        print "             ",
        print '-' +'-' * 4 * countb
        print "Black pieces: |",
        if self.bP==1:
            print  bcolors.OKBLUE+'P'+bcolors.ENDC,"|",
        if self.bB==1:
            print  bcolors.OKBLUE+'B'+bcolors.ENDC,"|",
        if self.bK==1:
            print  bcolors.OKBLUE+'K'+bcolors.ENDC,"|",
        if self.bR==1:
            print  bcolors.OKBLUE+'R'+bcolors.ENDC,"|",
        print
        print "             ",
        print '-' +'-' * 4 * countb
        print
        print
        print "    ",
        print "    c0  c1  c2  c3    "
        print "    ",
        print "  ------------------  "
        for r in range(4):
            print "    ",
            print "r"+str(r)+"|",
            for c in range(4):
                if self.squares[r][c] != 'e':
                    if 'b' in self.squares[r][c]: 
                        if 'P' in self.squares[r][c]:
                            print  bcolors.OKBLUE+'P'+ bcolors.ENDC,"|",
                        if 'B' in self.squares[r][c]:
                            print  bcolors.OKBLUE+'B'+ bcolors.ENDC,"|",
                        if 'K' in self.squares[r][c]:
                            print  bcolors.OKBLUE+'K'+ bcolors.ENDC,"|",
                        if 'R' in self.squares[r][c]:
                            print  bcolors.OKBLUE+'R'+ bcolors.ENDC,"|", 
                    else:
                        if 'P' in self.squares[r][c]:
                            print  bcolors.FAIL+'P'+ bcolors.ENDC,"|",
                        if 'B' in self.squares[r][c]:
                            print  bcolors.FAIL+'B'+ bcolors.ENDC,"|",
                        if 'K' in self.squares[r][c]:
                            print  bcolors.FAIL+'K'+ bcolors.ENDC,"|",
                        if 'R' in self.squares[r][c]:
                            print  bcolors.FAIL+'R'+ bcolors.ENDC,"|",
                else:
                    print "  |",
                if c == 3:
                    print #to get a new line
            print "    ",
            print "  ------------------  "
        print
        print "             ",
        print '-' +'-' * 4 * countw
        print "White pieces: |",
        if self.wP==1:
            print  bcolors.FAIL+'P'+bcolors.ENDC,"|",
        if self.wB==1:
            print  bcolors.FAIL+'B'+bcolors.ENDC,"|",
        if self.wK==1:
            print  bcolors.FAIL+'K'+bcolors.ENDC,"|",
        if self.wR==1:
            print  bcolors.FAIL+'R'+bcolors.ENDC,"|",
        print
        print "             ",
        print '-' +'-' * 4 * countw

    def MainLoop(self):
        print "Starting Chess..."
        self.whoseturn = "black"
        self.SetUpBoard(0)#make sure arg is 0 for standard set-up
        cmd_k='start'
        while self.IsInCheck() != 1:
            self.Draw()
            print "Player", self.whoseturn
            self.AllMove()
            #cmd_k =str(raw_input())
            cmd_k= f.readline()
            if cmd_k == '':
                break
            print cmd_k[0]
            cmd_deci = cmd_k[0]
            if cmd_deci == 'm':
                cmd_r,cmd_c,cmd_rt,cmd_ct = int(cmd_k[2]),int(cmd_k[4]),int(cmd_k[6]),int(cmd_k[8])
                move1 = self.GetPlayerInput(cmd_r,cmd_c,cmd_rt,cmd_ct)
                self.MakeMove(move1)
            else:
                cmd_p,cmd_r,cmd_c = cmd_k[2],int(cmd_k[4]),int(cmd_k[6])
                if self.CheckPut()== 1:
                    self.PutPiece(cmd_p,cmd_r,cmd_c)
            movek = self.AllMove()
            self.move = self.move +1
            self.PawnStatus()
            self.SwitchWhoseTurn()

        self.Draw() #draw board a final time to show the end game setup
        print "Player ",self.whoseturn," has lost the match!"
        
    def __init__(self):
        self.squares = [['e','e','e','e'],['e','e','e','e'],['e','e','e','e'],['e','e','e','e']]
        self.color ='none'
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

class ComputerRand(ChessBoard):
    def __init__(self):
        self.Comp =ChessBoard()
    def Compmakemove(self):
        move = self.AllMove()
        move1 = move.random()
        print move1

class Human(ChessBoard):
    def __init__(self):
        self.Hum =ChessBoard()

def MainLoop(player1,player2):
    print "Starting Game..."
    players=player1
    players.whoseturn = "black"
    players.SetUpBoard(0)#make sure arg is 0 for standard set-up
    cmd_k='start'
    #while players.IsInCheck() != 1:
    players.Draw()
    print "Player", players.whoseturn
    players.AllMove()
    #cmd_k =str(raw_input())
    if(players==player1):
        cmd_k= f.readline()
    #if cmd_k == '':
    #        break
    print cmd_k
    cmd_deci = cmd_k[0]
    if cmd_deci == 'm':
        cmd_r,cmd_c,cmd_rt,cmd_ct = int(cmd_k[2]),int(cmd_k[4]),int(cmd_k[6]),int(cmd_k[8])
        move1 = players.GetPlayerInput(cmd_r,cmd_c,cmd_rt,cmd_ct)
        players.MakeMove(move1)
    else:
        cmd_p,cmd_r,cmd_c = cmd_k[2],int(cmd_k[4]),int(cmd_k[6])
        if players.CheckPut()== 1:
            players.PutPiece(cmd_p,cmd_r,cmd_c)
    movek = players.AllMove()
    players.move = players.move +1
    players.PawnStatus()
    players.SwitchWhoseTurn()
    '''
    if(players==player1):
        players=player2
    else:
        players=player1
    '''
    players.Draw() #draw board a final time to show the end game setup
    print "Player ",players.whoseturn," has lost the match!"

if __name__ == "__main__":
    f = open('test.txt', 'r')
    b = ChessBoard()
    c=ComputerRand()
    #b.MainLoop()
    MainLoop(b,c)
