from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
# The Widget class is the base class required for creating Widgets
from kivy.uix.widget import Widget
import games.piano_tiles as pt
from games.Hangman import HM


class Dashboard(Screen):
    pass


class PianoTilesWindow(Screen):
    score = str(pt.score)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.piano = SoundLoader.load('audio.mp3')

    def play_piano(self):
        if self.piano:
            self.piano.play()

    def stop_piano(self):
        self.piano.stop()

    def start_game(self):
        self.piano.play()
        pt.start()
        self.piano.stop()


class TicTacToeWindow(Screen):
    pass


class HangmanLiteWindow(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    button_sqT=StringProperty("Start")
    difficulty=1
    loop_state=0#1-continue,0-finished

    def Diff_set(self,value):
        self.ids.diff_id.text=value
        if value== "easy":
            self.difficulty = 1
        if value == "medium":
            self.difficulty = 2

        if value == "hard":
            self.difficulty = 3
    def game_init(self):
        if(self.button_sqT=="Start" and self.loop_state==0):
            hm=HM.HangMan(self.difficulty)
            self.loop_state=1
            self.button_sqT="Quit"
            print("object created :",self.difficulty)
            print(hm.m_word)


class WindowManager(ScreenManager):
    pass


class GameArcadeApp(App):
    # def build(self):
    #     music = SoundLoader.load("audio.mp3")
    #     if music:
    #         music.play()
    pass


# run the App
if __name__ == '__main__':
    GameArcadeApp().run()
