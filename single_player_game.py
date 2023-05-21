from kivy.app import App
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.app import App
from random import choice
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.factory import Factory



class SinglePlayerGameWindow(Screen):
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

        label2 = self.ids.my_label2
        animation = Animation(color=self.label_color, duration=0.2)
        animation.start(label2)

    def restart_game(self):
        self.clear_buttons()

    def clear_buttons(self):
        grid_layout = self.ids.grid_layout
        for button in grid_layout.children:
            button.text = ""

    def on_button_click(self, button):
        # Handle button click logic here
        pass

    def on_button_click(self, button):
        if button.text == '':
            button.text = 'X'  # Update button text for player's move
            if self.check_game_over():
                return
            self.make_computer_move()

    def make_computer_move(self):
        empty_buttons = [button for button in self.ids.grid_layout.children if isinstance(button, Button) and button.text == '']
        if empty_buttons:
            # Check for winning move for computer
            for button in empty_buttons:
                button.text = 'O'
                if self.check_game_over():
                    return
                button.text = ''

            # Check for blocking player's winning move
            for button in empty_buttons:
                button.text = ''
                if self.check_game_over():
                    button.text = 'O'
                    return
                button.text = ''

            # Choose a random move if no winning/blocking move found
            computer_button = choice(empty_buttons)
            computer_button.text = 'O'

    def check_game_over(self):
        winning_combinations = [
            [1, 2, 3], [4, 5, 6], [7, 8, 9],  # Rows
            [1, 4, 7], [2, 5, 8], [3, 6, 9],  # Columns
            [1, 5, 9], [3, 5, 7]  # Diagonals
        ]


        # Check for winning combinations
        for combination in winning_combinations:
            buttons = [self.ids.grid_layout.children[index-1] for index in combination]
            print([button.text for button in buttons])  # Debug print statement
            if all(button.text == 'X' for button in buttons):
                # Player wins
                self.show_game_result("Player wins!")
                return True
            elif all(button.text == 'O' for button in buttons):
                # Computer wins
                self.show_game_result("Computer wins!")
                return True

        # Check for tie
        empty_buttons = [button for button in self.ids.grid_layout.children if
                         isinstance(button, Button) and button.text == '']
        if not empty_buttons:
            self.show_game_result("It's a tie!")
            return True

        return False

    def show_game_result(self, result):
        # Implement your logic to display the game result (e.g., show a popup)
        # The "result" parameter contains the game result message (e.g., "Player wins!", "Computer wins!", "It's a tie!")
        popup = Popup(title="Game Result", content=Label(text=result), size_hint=(None, None), size=(400, 200))
        popup.open()

