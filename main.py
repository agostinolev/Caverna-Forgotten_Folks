from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.uix.checkbox import CheckBox
import random
import os.path
from kivy.core.window import Window
Window.softinput_mode = 'below_target'

fields = []
for i in range(7):
	fields.append('Player '+str(i+1))


Builder.load_file('main.kv')
d={}
players = []

def choose_class(*args):
    species = ['Bladolicy','Elfy','Górskie krasnoludy','Jaskiniowe gobliny','Kryształowe golemy','Ludzie','Mroczne elfy','Trolle']
    random.shuffle(species)

    for player in players:
        if(player in d):
            if(d[player][1] == 'blocked'):
                species.remove(d[player][0]) # remove from species the one that are blocked

    for player in players:
        if(player in d):
            if(d[player][1] == 'unblock'):
                specie0 = d[player][0] # the initial specie

                while True:
                    specie = species.pop()
                    if(specie == specie0):
                        species.append(specie)
                        random.shuffle(species)
                    else:
                        break
            else:
                specie = d[player][0]
        else:
            specie = species.pop()
        d[player] = [specie,'unblock']

class ScreenTwo(Screen):

    check_ref = {}
    def on_pre_enter(self,*args):
        choose_class()
        self.create_button()
        self.print_players()

    def print_players(self,*args):
        self.check_ref = {}
        self.pos_hintNames = [-0.3, 0.4]
        self.pos_hintSpeciess = [0.1, 0.4]
        self.pos_hintboxs = [0.65, 0.85]
        for i in d:
            self.add_widget(Label(text="{0}:".format(i), pos_hint={'x': self.pos_hintNames[0], 'y': self.pos_hintNames[1]},color=(1,1,1,1)))
            self.add_widget(Label(text="{0}".format(d[i][0]), pos_hint={'x': self.pos_hintSpeciess[0], 'y': self.pos_hintSpeciess[1]},color=(1,1,1,1)))
            c = CheckBox(pos_hint={'x': self.pos_hintboxs[0], 'y': self.pos_hintboxs[1]},active=False, size_hint=(.5,.1))
            self.check_ref[i] = c
            self.add_widget(c)
            self.pos_hintNames[1] -= 0.1; self.pos_hintSpeciess[1] -= 0.1; self.pos_hintboxs[1] -= 0.1


    def create_button(self):
        btn = Button(text="Choose new Players",size_hint_y=None,size_hint_x=0.5,height='48dp',width='10dp',pos_hint={'x':0.0, 'y':0.0})
        btn.bind(on_release=self.new_players)
        self.add_widget(btn)
        btn = Button(text="Re-roll",size_hint_y=None,size_hint_x=0.5,height='48dp',width='10dp',pos_hint={'x':0.5, 'y':0.0})
        btn.bind(on_release=self.new_reroll)
        self.add_widget(btn)

    def new_players(self,*args):
        self.clear_widgets()
        switching_function()

    def new_reroll(self,*args):
        for child in self.children[:]:
            if isinstance(child,Label):
                for i in d:
                    if(child.text == d[i][0]):
                        self.remove_widget(child)
        for idx, wgt in self.check_ref.items():
            if(wgt.active): 
                d[idx][1] = 'blocked'
            else:
                d[idx][1] = 'unblock'
            self.remove_widget(wgt)
        self.on_pre_enter()


class MainScreen(Screen):
    container = ObjectProperty(None)

    def save_data(self):
        
        global d
        d = {}
        global players
        players = []
        for child in reversed(self.container.children):
            if isinstance(child, TextInput):
                if(child.text != ''):
                    players.append(child.text)


def switching_function(*args):
        MainApp.sm.current = 'screen_1'

class MainApp(App):
    sm = ScreenManager()

    def build(self):
        MainApp.sm.add_widget(MainScreen(name='screen_1'))
        MainApp.sm.add_widget(ScreenTwo(name='screen_2'))
        return MainApp.sm

 

if __name__ == "__main__":
    MainApp().run()
