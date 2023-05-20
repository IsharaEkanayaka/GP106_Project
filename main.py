from kivy.app import App
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
# The Widget class is the base class required for creating Widgets
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
import games.piano_tiles as pt
from kivy.clock import Clock
from pathlib import Path
import json

class Dashboard(Screen):
    pass


class PianoTilesWindow(Screen):
    with open(Path("games/save_data/piano_tiles.json"),"r") as data:
        marks = json.load(data)
    
    
    pre_name = marks[-1]['name']
    pre_score = marks[-1]['score']
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.piano = SoundLoader.load('audio.mp3')

    def stop_piano(self):
        self.piano.stop()

    def start_game(self):
        global pre_name,pre_score
        self.piano.play()
        with open(Path("games/save_data/piano_tiles.json"),"r") as data:
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

    def on_text_validate(self,widget):
        self.text_input_str = widget.text
        print(self.text_input_str)

    def save(self):
        new_score = {'name':self.text_input_str,'score':self.score}
        with open(Path("games/save_data/piano_tiles.json"),"r") as data:
            marks = json.load(data)
        with open(Path("games/save_data/piano_tiles.json"),"w") as f:
            marks.append(new_score)
            json.dump(marks,f)

    def highest_marks(self):
        with open(Path("games/save_data/piano_tiles.json"),"r") as data:
            marks = json.load(data)
        L = []
        for i in marks:
            L.append(int(i["score"]))
        highestScore = max(L)
        self.ids._highestMarks.text = str(highestScore )

    

class TicTacToeWindow(Screen):
    pass

class HangmanLiteWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class GameArcadeApp(App):
    pass
        
# run the App
if __name__ == '__main__':
    GameArcadeApp().run()
    
