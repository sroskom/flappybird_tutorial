from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
import random


        
class Sprite(Image):
    def __init__(self, **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self.size = self.texture_size

class Background(Sprite):
    def __init__(self, source):
        super(Background, self).__init__()
        self.image = Sprite(source=source)
        self.add_widget(self.image)
        self.size = self.image.size
        self.image_dupe = Sprite(source=source, x=self.width)
        self.add_widget(self.image_dupe)
        
    def update(self):
        self.image.x -= 2
        self.image_dupe.x -= 2

        if self.image.right <= 0:
            self.image.x = 0
            self.image_dupe.x = self.width

class Bird(Sprite):
    def __init__(self, pos):
        super(Bird,self).__init__(source='atlas://images/bird_anim/wing-up',pos=pos)
        self.velocity_y = 0
        self.gravity = -.1

    def update(self):
        self.velocity_y += self.gravity
        self.veloctiy_y = max(self.velocity_y, -5)
        self.y += self.velocity_y
        if self.velocity_y < -5:
            self.source = 'atlas://images/bird_anim/wing-up'
        elif self.velocity_y < 0:
            self.source = 'atlas://images/bird_anim/wing-mid'
    def on_touch_down(self, *ignore):
        self.velocity_y = 3
        self.source = 'atlas://images/bird_anim/wing-down'

class Ground(Sprite):
    def update(self):
        self.x -= 2
        if self.x < -24:
            self.x += 24

class Pipe(Widget):
    def __init__(self, pos):
        super(Pipe, self).__init__(pos=pos)
        self.top_image = Sprite(source='images/pipe_top.png')
        self.top_image.pos = (self.x,self.y +3.5*24)
        self.add_widget(self.top_image)
        self.bottom_image = Sprite(source='images/pipe_bottom.png')
        self.bottom_image.pos = (self.x,self.y -self.bottom_image.height)
        self.add_widget(self.bottom_image)
        self.width = self.top_image.width
        self.scored = False

    def update(self):
        self.x -= 2
        self.top_image.x = self.bottom_image.x = self.x
        if self.right <0:
            self.parent.remove_widget(self)

class Pipes(Widget):
    add_pipe = 0
    def update(self, dt):
        for child in list(self.children):
            child.update()
        self.add_pipe -= dt
        if self.add_pipe <0:
            y = random.randint(self.y +50,self.height - 50 -3.5*24)
            self.add_widget(Pipe(pos=(self.width,y)))
            self.add_pipe = 1.5
            
class Game(Widget):
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        if True:
            self.background = Background(source='images/background.png')
            self.size = self.background.size
            self.add_widget(self.background)
            self.ground = Ground(source='images/ground.png')
            self.pipes = Pipes(pos=(0,self.ground.height),size=self.size)
            self.add_widget(self.pipes)
            self.add_widget(self.ground)
            self.score_label = Label(center_x=self.center_x,
                                     top=self.top - 30,text='0')
            self.add_widget(self.score_label)
            self.bird =Bird(pos=(20,self.height/2))
            self.add_widget(self.bird)
            Clock.schedule_interval(self.update, 1.0/60.0)
            self.game_over = False
            self.score = 0

    def update(self, dt):
        self.background.update()
        self.bird.update()
        self.ground.update()
        self.pipes.update(dt)

        if self.bird.collide_widget(self.ground):
            self.game_over = True
        for pipe in self.pipes.children:
            if pipe.top_image.collide_widget(self.bird):
                self.game_over = True
            elif pipe.bottom_image.collide_widget(self.bird):
                self.game_over = True
            elif not pipe.scored and pipe.right < self.bird.x:
                pipe.scored = True
                self.score +=1
                self.score_label.text = str(self.score)
            
        if self.game_over:
            pass
        
class GameApp(App):
    def build(self, *args):
        game = Game()
        Window.size = game.size
        return game

if __name__ == '__main__':
    GameApp().run()
