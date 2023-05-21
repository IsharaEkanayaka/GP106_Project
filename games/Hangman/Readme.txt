

by default the leds are connected to digital pin 2,3,4 and ldr to A0

what each file does>>>>>>>>>>>

mainSource=this contains the gameloop
HM=this contains the hangman game class which has all the methods for controlling the game instance
dependencies=has all the common modules used in the project
STuple_toT=converts string(in the form of a tuple) in the wordTuple.txt file into an actual tuple and get imported in the HM.py file
wordCtot=this class recives an string(wordCollection.txt) and creates a tuple containing all the ini=dividual words in the wordCollection.txt 
buildfiles=this updates the wordTuple.txt file(if you add or remove words form the wordCollection.txt file,before lunching the mainSource.py ,lunch 
            this file .)
Configuratoion.py=initiallize the connection between arduino and python , and sets the pins
LDR_input=returns the letter given  by the morse code


wordCollection=contains all the words that belongs to the program(add more words to expand the game)
wordTuple=contains all the words in the wordCollection.txt as  tuple 


main_run.bat-this lunches first Buildfiles then mainSource


1.Open  the Configuration.py file and set the pins accordingly to your arduino setup
2.install dependencies mentioned in the dependencies.py file(also install pyfirmata)
3.fix the distance between ldr and flashlight about 2cm of less
4.run the main_run.bat
