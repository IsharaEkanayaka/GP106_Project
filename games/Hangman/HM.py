import time
import random
import numpy as np

from games import Config
from games.Hangman import wordCollection
import sys



led_pins = (2, 3, 4)  # change according to your setup
LDR_pin = 0  # change according to your setup

for i in range(0, len(led_pins)):
    Config.board.digital[led_pins[i]].write(0)

#////////////////////////////LDRInput////////////////////////////////////////////


morsedata = {
    '01': 'A',
    '1000': 'B',
    '1010': 'C',
    '100': 'D',
    '0': 'E',
    '0010': 'F',
    '110': 'G',
    '0000': 'H',
    '00': 'I',
    '0111': 'J',
    '101': 'K',
    '0100': 'L',
    '11': 'M',
    '10': 'N',
    '111': 'O',
    '0110': 'P',
    '1101': 'Q',
    '010': 'R',
    '000': 'S',
    '1': 'T',
    '001': 'U',
    '0001': 'V',
    '011': 'W',
    '1001': 'X',
    '1011': 'Y',
    '1100': 'Z'

}
def analogread():
    return Config.board.analog[LDR_pin].read()

def readletter():
    current_level = 0.0
    cutoff = 0.30
    timelist = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    arrayfilled = 0
    morse = []
    above_level = False
    below_level = True
    wordfound = False

    time.sleep(0.001)
    # while(analogread()==None):
    #   pass

    start_time = time.time()
    # print('.........')
    while True:
        while analogread() == None:
            pass
        current_level = analogread()

        while (below_level == True) and (wordfound == False) and (current_level < cutoff):
            current_level = analogread()
            time.sleep(0.001)

        if (below_level == True) and (current_level > cutoff):
            if arrayfilled == 7:
                break
            timelist[arrayfilled] = (time.time() - start_time)
            # print('u')
            arrayfilled = arrayfilled + 1
            below_level = False
            above_level = True
            wordfound = True

        if (above_level == True) and (current_level < cutoff):
            timelist[arrayfilled] = (time.time() - start_time)
            # print('d')
            arrayfilled = arrayfilled + 1
            below_level = True
            above_level = False

        duration = (time.time() - start_time) - (timelist[timelist != 0][-1])
        time.sleep(0.001)
        if (below_level == True) and (duration > 1.0):  # returns in seconds
            break

        # check for len(timelist) is even/it shold be even if correct
    for i in range(1, len(timelist[timelist != 0]), 2):
        # the maximum time in s for the dots
        timegap = (timelist[i] - timelist[i - 1]).item()
        if timegap < 0.4:
            morse.append(0)
        else:
            morse.append(1)

    return morsedata.get(''.join(str(l) for l in morse))

#///////////////////////////////////////////////GAMECLASS//////////////////////////////////////////////////////////////////////////////


class HangMan:

    def __init__(self, difficulty):
        # initializing class variables
        self.gessedCorrrect=False
        self.m_gamestate = 'continue'
        self.m_playerwon = False
        self.m_attempts = 1
        self.m_difficulty = difficulty
        self.marks=0

        self.m_word = []  # contains the word
        self.m_rightc = []  # contain the correctly gessed letters in order
        self.m_wrongc = []  # contains the incorrectly gessed letters
        self.m_freec = []  # contains the letters (word-right)-remaining letters in the word needs to be gessed
        # assign a word to self.m_word below to check the code and comment getwordlist and get word funxtions

        self.m_word = self.getword()

        for i in range(0, len(self.m_word)):
            self.m_rightc.append('_ ')
            self.m_freec = self.m_word.copy()

    def getword(self):
        randIndex = random.randint(0, (len(wordCollection.wordset[str(self.m_difficulty)]) - 1))
        return list(wordCollection.wordset[str(self.m_difficulty)][randIndex])

        # returns a list with the charactor count and there indecies in the word

    def repeats_inword(self, word, charactor):
        ccount = 0
        rlist = []

        for i in range(0, len(word)):
            if word[i] == charactor:
                rlist.append(i)
                ccount = ccount + 1
        rlist.insert(0, ccount)
        return rlist

    # decoded arduino input is recived by this
    def askinput(self):
        letter = readletter()
        return letter

    # the given letter is checked against the word
    def checkinput(self):
        print('enter the letter :', end='',flush=True)  # flush the buffer to ensure this statement gets printed in the console
        letter = self.askinput()  # get the input
        print(letter)
        if self.m_freec.count(letter) > 0:
            print('-correct')
            lrepeats_inword = self.repeats_inword(self.m_word, letter)
            lrepeats_inright = self.repeats_inword(self.m_rightc, letter)

            self.m_rightc[lrepeats_inword[lrepeats_inright[0] + 1]] = letter  # updates m_rightc
            self.m_freec.remove(letter)
            self.gessedCorrrect=True

        else:
            print('-incorrect')
            self.m_wrongc.append(letter)
            self.m_attempts = self.m_attempts + 1
            self.gessedCorrrect=False

        # each loop this is called and the current state of the game is updated

    def checkstatus(self):
        if self.m_attempts >= 4:
            self.m_gamestate = 'finished'

        if self.m_word == self.m_rightc:
            self.m_gamestate = 'finished'
            self.m_playerwon = True
        # function to print a list as a string

    def printlist(self, thelist):
        for item in thelist:
            print(item, end='')

    # def list_tostring(thelist):''.join(str(l) for l in self.m_word)

    # def savegame(): future improvements

    # this renders graphics in the terminal
    def render(self):
        # clear window
        if self.m_gamestate == 'continue':
            self.printlist(self.m_rightc)
            print('')

        if self.m_gamestate == 'finished' and self.m_playerwon == False:
            print('!!!you lost!!!')
            print('The correct word is :', ''.join(str(l) for l in self.m_word))
            print('you gessesed :', ''.join(str(l) for l in self.m_rightc))
            # print marks

        if self.m_gamestate == 'finished' and self.m_playerwon == True:
            print('!!!you won!!!')
            print('The word is :', ''.join(str(l) for l in self.m_word))

        # run loop of the entire game

    def run(self):
        while True:
            self.checkstatus()
            self.render()
            if self.m_gamestate == 'finished':
                break
            else:
                self.checkinput()
                self.update_marks()
                self.light_update()

        # the tree led bulbs are lit accordingly

    def light_update(self):
        for i in range(0, (self.m_attempts - 1)):
            Config.board.digital[led_pins[i]].write(1)

        # when this game instance is deleted the data will be saved to a text file

    def update_marks(self):
        if self.gessedCorrrect:
            self.marks=self.marks+(int(self.m_difficulty)*10)


#print("*****HANG MAN*****")
#difficulty = '1'
## gameloop
#while True:
#    hm = HangMan(difficulty)
#    hm.run()
#    del hm
#
#    choice = str(input("Do you want to play again (Y/N)? "))
#    for i in range(0, len(led_pins)):
#        Config.board.digital[led_pins[i]].write(0)
#
#    if choice == 'Y':
#        print('Y')
#
#    if choice == 'N':
#        print('N')
#        break
