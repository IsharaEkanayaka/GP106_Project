#!/usr/bin/python
# Filename : piano_tiles.py
# Author : Ishara Ekanayaka
# Reg No : E/20/094
from pyfirmata import Arduino,OUTPUT,util,INPUT
import time
import random
score = 0
#setup configurations
board=Arduino("COM8")
button1 = board.digital[8]
button2 = board.digital[9]
button3 = board.digital[10]
button1.mode = INPUT
button2.mode = INPUT
button3.mode = INPUT
PIEZO =board.get_pin('d:11:p')

#set led pins as output pins
board.digital[2].mode = OUTPUT
board.digital[3].mode = OUTPUT
board.digital[4].mode = OUTPUT
board.digital[5].mode = OUTPUT
board.digital[6].mode = OUTPUT
board.digital[7].mode = OUTPUT

#start utilization process
it = util.Iterator(board)
it.start()

R1,R2,R3 = 20,20,20
def row1():
    turn(R1)
def row2():
    turn(R2+3)
def row3():
    turn(R3+6)

#decide randomly which led is turn on in row 1
def decide():
    global R1
    X = [0,1,2]
    p = random.choices(X)[0]
    R1 = p
def turn_off():
    board.digital[2].write(0)
    board.digital[3].write(0)
    board.digital[4].write(0)
    board.digital[5].write(1)
    board.digital[6].write(1)
    board.digital[7].write(1)
def buzzer(a):
    if a == 0:
        PIEZO.write(0.1)
        board.pass_time(0.1)
        PIEZO.write(0)
    if a == 1:
        PIEZO.write(1)
        board.pass_time(0.1)
        PIEZO.write(0)

def turn(a):
    if a==0:
        board.digital[2].write(1)
        board.digital[3].write(0)
        board.digital[4].write(0)
        board.digital[5].write(0)
        board.digital[6].write(1)
        board.digital[7].write(1)

    elif a==1:
        board.digital[2].write(1)
        board.digital[3].write(0)
        board.digital[4].write(0)
        board.digital[5].write(1)
        board.digital[6].write(0)
        board.digital[7].write(1)

    elif a==2:
        board.digital[2].write(1)
        board.digital[3].write(0)
        board.digital[4].write(0)
        board.digital[5].write(1)
        board.digital[6].write(1)
        board.digital[7].write(0)
    elif a==3:
        board.digital[2].write(0)
        board.digital[3].write(1)
        board.digital[4].write(0)
        board.digital[5].write(0)
        board.digital[6].write(1)
        board.digital[7].write(1)
    elif a==4:
        board.digital[2].write(0)
        board.digital[3].write(1)
        board.digital[4].write(0)
        board.digital[5].write(1)
        board.digital[6].write(0)
        board.digital[7].write(1)
    elif a==5:
        board.digital[2].write(0)
        board.digital[3].write(1)
        board.digital[4].write(0)
        board.digital[5].write(1)
        board.digital[6].write(1)
        board.digital[7].write(0)
    elif a==6:
        board.digital[2].write(0)
        board.digital[3].write(0)
        board.digital[4].write(1)
        board.digital[5].write(0)
        board.digital[6].write(1)
        board.digital[7].write(1)
    elif a==7:
        board.digital[2].write(0)
        board.digital[3].write(0)
        board.digital[4].write(1)
        board.digital[5].write(1)
        board.digital[6].write(0)
        board.digital[7].write(1)
    elif a==8:
        board.digital[2].write(0)
        board.digital[3].write(0)
        board.digital[4].write(1)
        board.digital[5].write(1)
        board.digital[6].write(1)
        board.digital[7].write(0)
def start():
    global score
    global R1,R2,R3
    while True:
        i = 0
        if score < 5:
            c = 0
            b1,b2,b3 = 0,0,0
            X = [0,1,2]
            r = random.choices(X)[0]
            turn(r)
            time.sleep(1)
            turn_off()
            turn(r+3)
            time.sleep(1)
            turn(r+6)

            timer1 = time.time()
            timer2 = 5
            while (timer2 - timer1) <= 1:
                button1_state = button1.read()
                button2_state = button2.read()
                button3_state = button3.read()

                if r+6 ==6:
                    if button1_state == 1:
                        buzzer(1)
                        i = 1
                        b1 = 1
                    if button2_state == 1 or button3_state == 1:
                        c = 1
                        buzzer(0)
                        break
                if r+6 ==7:
                    if button2_state == 1:
                        buzzer(1)
                        i = 1
                        b2 = 1
                    if button3_state == 1 or button1_state == 1:
                        c = 1
                        buzzer(0)
                        break
                if r+6 ==8:
                    if button3_state == 1:
                        buzzer(1)
                        i = 1
                        b3 = 1
                    if button1_state == 1 or button2_state == 1:
                        c = 1
                        buzzer(0)
                        break
                timer2 = time.time()
            turn_off()
            score = score + i
            if c == 1:
                print("Game over")
                print("score",score)
                break
            if b1 == 0 and b2 == 0 and b3 == 0:
                print("Game over")
                print("score",score)
                print("didn't pressed")
                buzzer(0)
                break
        
        if score >= 5:
            c = 0
            b1,b2,b3 = 0,0,0
            R3 = R2
            R2 = R1
            decide()

            timer1 = time.time()
            timer2 = 5
            while (timer2 - timer1) <= 1:
                button1_state = button1.read()
                button2_state = button2.read()
                button3_state = button3.read()
                turn(R1)
                time.sleep(0.01)
                turn_off()
                turn(R2+3)
                time.sleep(0.01)
                turn_off()
                turn(R3+6)
                time.sleep(0.01)
                if R3 == 0:
                    if button1_state == 1:
                        buzzer(1)
                        i = 1
                        b1 = 1
                    if button2_state == 1 or button3_state == 1:
                        c = 1
                        buzzer(0)
                        break
                if R3 == 1:
                    if button2_state == 1:
                        buzzer(1)
                        i = 1
                        b2 = 1
                    if button3_state == 1 or button1_state == 1:
                        c = 1
                        buzzer(0)
                        break
                if R3 == 2:
                    if button3_state == 1:
                        buzzer(1)
                        i = 1
                        b3 = 1
                    if button2_state == 1 or button1_state == 1:
                        c = 1
                        buzzer(0)
                        break
                turn_off()
                timer2 = time.time()
            score = score + i
            if c == 1:
                print("Game over")
                print("score",score)
                break
            if R3 == 20 or R2 == 20:
                pass
            else:
                if b1 == 0 and b2 == 0 and b3 == 0:
                    print("Game over")
                    print("score",score)
                    print("didn't pressed")
                    buzzer(0)
                    break






