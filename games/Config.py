from pyfirmata import Arduino, OUTPUT
from pyfirmata import Arduino, util, INPUT

board=Arduino("COM3")
button1 = board.digital[8]
button2 = board.digital[9]
button3 = board.digital[10]
button1.mode = INPUT
button2.mode = INPUT
button3.mode = INPUT
PIEZO =board.get_pin('d:11:p')

board.analog[0].mode = INPUT

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
board.analog[0].enable_reporting()