from kivy.app import App
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
# The Widget class is the base class required for creating Widgets
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.uix.image import Image
import games.PianoTiles.piano_tiles as pt
from games.Hangman import HM
from random import choice
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.factory import Factory
from kivy.uix.button import Button
import Two_Players
from single_player_game import SinglePlayerGameWindow
from kivy.clock import Clock
from pathlib import Path
import json

class Dashboard(Screen):
    pass


class PianoTilesWindow(Screen):
    with open(Path("games/PianoTiles/save_data/piano_tiles.json"),"r") as data:
        marks = json.load(data)
    score = str(pt.score)
    pre_name = marks[-1]['name']
    pre_score = marks[-1]['score']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.piano = SoundLoader.load('audio.mp3')
        self.highest_marks()
    def play_piano(self):
        if self.piano:
            self.piano.play()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.piano = SoundLoader.load('audio.mp3')

    def stop_piano(self):
        self.piano.stop()

    def start_game(self):
        global pre_name,pre_score
        self.piano.play()
        with open(Path("games/PianoTiles/save_data/piano_tiles.json"),"r") as data:
            marks = json.load(data)
        pre_name = marks[-1]['name']
        pre_score = marks[-1]['score']
        self.ids._preName.text = pre_name
        self.ids._preScore.text = str(pre_score)
        self.highest_marks()
        pt.start()
        self.score = pt.score
        self.save()
        self.piano.stop()
        self.manager.current = 'GameOverWindow'

    def on_text_validate(self,widget):
        self.text_input_str = widget.text
        print(self.text_input_str)

    def save(self):
        new_score = {'name':self.text_input_str,'score':self.score}
        with open(Path("games/PianoTiles/save_data/piano_tiles.json"),"r") as data:
            marks = json.load(data)
        with open(Path("games/PianoTiles/save_data/piano_tiles.json"),"w") as f:
            marks.append(new_score)
            json.dump(marks,f)

    def highest_marks(self):
        with open(Path("games/PianoTiles/save_data/piano_tiles.json"),"r") as data:
            marks = json.load(data)
        L = []
        for i in marks:
            L.append(int(i["score"]))
        highestScore = max(L)
        self.ids._highestMarks.text = str(highestScore )


class TicTacToeWindow(Screen):
    label_color = ListProperty([0, 0, 1, 1])  # Initial label color

    def on_enter(self):
        Clock.schedule_interval(self.change_label_color, 1)

    def on_leave(self):
        Clock.unschedule(self.change_label_color)

    def change_label_color(self, dt):
        if self.label_color == [0, 0, 1, 1]:  # Blue to green
            self.label_color = [0, 1, 0, 1]
        elif self.label_color == [0, 1, 0, 1]:  # Green to red
            self.label_color = [1, 0, 0, 1]
        else:  # Red to blue
            self.label_color = [0, 0, 1, 1]

        label = self.ids.my_label
        animation = Animation(color=self.label_color, duration=0.2)
        animation.start(label)


class HangmanLiteWindow(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    button_sqT=StringProperty("Start")
    difficulty=3
    hm = HM.HangMan(difficulty)
    loop_state=0#1-continue,0-finished


    def Diff_set(self,value):
        self.ids.diff_id.text=value
        if value== "easy":
            self.difficulty = 1
        if value == "medium":
            self.difficulty = 2

        if value == "hard":
            self.difficulty = 3
    def Start_clicked(self):
        if(self.button_sqT=="Start" and self.loop_state==0):
            self.create_Box()
            self.loop_state=1
            self.button_sqT="Quit"
            self.ids.button_sq.text="Quit"
        else:
            self.loop_state = 0
            self.button_sqT = "Start"
            self.ids.button_sq.text = "Start"

    def create_Box(self):
        for i in range(0,len(self.hm.m_word)):
            imagea=Image(source='images/square3.png',allow_stretch=True,keep_ratio=False,size_hint=(0.15,0.2),pos_hint={'x':((1-(len(self.hm.m_word)*0.15))/2)+0.15*i,'y':0.4})
            self.add_widget(imagea)
            
class TwoPlayersGameWindow(Screen):
  def run_two_players(self):
        import Two_Players
        Two_Players.play_game()

class GameOverWindow(Screen):
    pass

class WindowManager(ScreenManager):
    single_player_game = ObjectProperty(None)  # Add this line


class GameArcadeApp(App):
    pass


# run the App
if __name__ == '__main__':
    GameArcadeApp().run()
    
