from kivy.app import App
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
# The Widget class is the base class required for creating Widgets
from kivy.uix.widget import Widget
# to change the kivy default settings we use this module config
from kivy.config import Config
Config.set('graphics', 'resizable', True)
class MyApp(App):
    def build(self):
        music = SoundLoader.load("audio.mp3")
        if music:
            music.play()
        self.img = Image(source ='R.png')
        self.img.allow_stretch = True
        self.img.keep_ratio = False
        self.img.size_hint_x = 1
        self.img.size_hint_y = 1
        self.img.pos = (350, 400)
        self.img.opacity = 1
        s = Widget()
        s.add_widget(self.img)
        return s
# run the App
if __name__ == '__main__':
    MyApp().run()
