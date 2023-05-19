from kivy.app import App
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
# The Widget class is the base class required for creating Widgets
from kivy.uix.widget import Widget
import games.piano_tiles as pt

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
    pass

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
