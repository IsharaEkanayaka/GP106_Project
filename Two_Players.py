def play_game():
    from pyfirmata import Arduino,OUTPUT,INPUT,util
    import time
    import sys
    board = Arduino ("COM8")

    # Defining  Arduino Pins
    Row0=5
    Row1=6
    Row2=7
    Col0=8
    Col1=9
    Col2=10
    Btn0=0
    Btn1=1
    Btn2=2

    # Defining Arduino Pins as INPUT or OUTPUT

    board.digital[Row0].mode = OUTPUT
    board.digital[Row1].mode = OUTPUT
    board.digital[Row2].mode = OUTPUT
    board.digital[Col0].mode = OUTPUT
    board.digital[Col1].mode = OUTPUT
    board.digital[Col2].mode = OUTPUT
    board.analog[Btn0].mode = INPUT
    board.analog[Btn1].mode = INPUT
    board.analog[Btn2].mode = INPUT
    it = util.Iterator(board)
    it.start()
    board.analog[Btn0].enable_reporting()
    board.analog[Btn1].enable_reporting()
    board.analog[Btn2].enable_reporting()


    status ="START"
    # Getting the names of the players
    player1=""
    player2=""
    # The player who is playing the game
    turn="1"
    # Coordinates of each point marked by each player in 3x3 grid
    player1points=[]
    player2points=[]
    currentRow = 0
    currentCol = 0

    # Setting a single LED on the grid to turn ON
    def lightLed(point):
        global board
        if 1 == point[0]:
            board.digital[Row0].write(1)
            board.digital[Row1].write(0)
            board.digital[Row2].write(0)
        elif 2 == point[0]:
            board.digital[Row0].write(0)
            board.digital[Row1].write(1)
            board.digital[Row2].write(0)
        elif 3 == point[0]:
            board.digital[Row0].write(0)
            board.digital[Row1].write(0)
            board.digital[Row2].write(1)
        if 1 == point[1]:
            board.digital[Col0].write(0)
            board.digital[Col1].write(1)
            board.digital[Col2].write(1)
        elif 2 == point[1]:
            board.digital[Col0].write(1)
            board.digital[Col1].write(0)
            board.digital[Col2].write(1)
        elif 3 == point[1]:
            board.digital[Col0].write(1)
            board.digital[Col1].write(1)
            board.digital[Col2].write(0)

    # Setting all LEDs on the grid to turn OFF
    def offLed():
        board.digital[Row0].write(0)
        board.digital[Row1].write(0)
        board.digital[Row2].write(0)
        board.digital[Col0].write(1)
        board.digital[Col1].write(1)
        board.digital[Col2].write(1)

    # Selecting a single point on the 3x3 matrix

    def selectPoint():
        global board
        global currentRow
        global currentCol
        global Btn0
        global Btn1
        global Btn2
        count = 0
        print("Select a Row")
        while True:
            for point in player1points:
                lightLed(point)
                offLed()
            if count % 40 == 0:
                for point in player2points:
                    lightLed(point)
                    offLed()
            count += 1
            if board.analog[Btn0].read() == 1.0 :
                currentRow = 1
                break
            if board.analog[Btn1].read() == 1.0 :
                currentRow = 2
                break
            if board.analog[Btn2].read() == 1.0 :
                currentRow = 3
                break
        print("Row", currentRow, "selected")
        time.sleep(1)
        print("Select a Column")
        while True:
            lightLed([currentRow,1])
            offLed()
            lightLed([currentRow,2])
            offLed()
            lightLed([currentRow,3])
            offLed()
            if board.analog[Btn0].read() == 1.0 :
                currentCol = 1
                break
            if board.analog[Btn1].read() == 1.0 :
                currentCol = 2
                break
            if board.analog[Btn2].read() == 1.0 :
                currentCol = 3
                break
        print("Col", currentCol, "selected")
        time.sleep(1)
        if ([currentRow,currentCol] in player1points or [currentRow,currentCol] in player2points ):
            print("Point already taken")
            selectPoint()
            return
        else:
            return

    # Checking whether one of the players have won and then exit the game
    def checkWin():
        global player1
        global player2
        global player1points
        global player2points
        if(checkWinSinglePlayer(player1points) == True):
            print("TIC-TAC-TOE")
            print("------------------------------------")
            print("")
            print(player1,"WON")
            print("")
            ("------------------------------------")
            time.sleep(3)
            sys.exit()
        if(checkWinSinglePlayer(player2points) == True):
            print("TIC-TAC-TOE")
            print("------------------------------------")
            print("")
            print(player1,"WON")
            print("")
            ("------------------------------------")
            time.sleep(3)
            sys.exit()

    # Checking no of points which were marked by each player in each row and column and diagonal respectively to decide whether he has won

    def checkWinSinglePlayer(player1points):

        row1 = 0
        row2 = 0
        row3 = 0
        col1 = 0
        col2 = 0
        col3 = 0
        dig1 = 0
        dig2 = 0
        for point in player1points:
            if point[0] == 1: row1 += 1
            if point[0] == 2: row2 += 1
            if point[0] == 3: row3 += 1
            if point[1] == 1: col1 += 1
            if point[1] == 2: col2 += 1
            if point[1] == 3: col3 += 1
            if point[0] == point[1]: dig1 += 1
            if point == [1,2]: dig2 += 1
            if point == [2,2]: dig2 += 1
            if point == [3,1]: dig2 += 1
        if(row1 == 3 or row2 == 3 or row3 == 3 or col1 == 3 or col2 == 3 or col3 == 3 or dig1 ==3 or dig2 == 3):
            return True
        else :
            return False

    while True:
        # Start game and taking each player's name as input
        if status == "START":
            print("WELCOME TO TIC-TAC-TOE")
            print("------------------------------------")
            player1 = input("Enter name of player 1 -: ")
            player2 = input("Enter name of player 2 -: ")
            status = "PLAY"
        # play game
        if status == "PLAY":
            print("TIC-TAC-TOE")
            print("------------------------------------")
            if turn == "1":
                print(player1,"'s Turn")
            else:
                print(player2,"'s Turn")
            print("------------------------------------")
            # Allowing players to mark a point by selecting a row and a column accordingly
            selectPoint()
            # Saving the selected point under each player
            if turn == "1":
                player1points.append([currentRow,currentCol])
                currentRow=0
                currentCol=0
                turn ="2"
            else:
                player2points.append([currentRow,currentCol])
                currentRow=0
                currentCol=0
                turn ="1"
        # Checking weather anyone has won the game after last point selection
        checkWin()
