## Nolan Hollingsworth
## Project 1
## CPS 499 - Game Dev
## University of Dayton

import cocos
from cocos.director import director
from cocos.actions import *
import cocos.collision_model as cm
import cocos.euclid as eu
import pyglet
from pyglet.window import key
from pyglet.window import mouse
import random

# UPDATE IF BACKGROUND CHANGES OR SCREEN RES CHANGES
WIDTH = 1280
HEIGHT = 720
BGWIDTH = 5000
BGHEIGHT = 5000

window = None

class Mover(cocos.actions.Move):
    def __init__(self, worldRect):
        super(Mover, self).__init__()
        self.worldRect = worldRect

    is_event_handler = True
    MOVE_SPEED = 750

    def step(self, dt):
        global keyboard, scroller
        if dt > 0.1:
            return

        vx = (keyboard[key.D] - keyboard[key.A]) * self.MOVE_SPEED
        vy = (keyboard[key.W] - keyboard[key.S]) * self.MOVE_SPEED

        runner_x, runner_y = self.target.position
        if (runner_x) > 1940:
            self.target.velocity = (-keyboard[key.A] * self.MOVE_SPEED, vy)
        elif(runner_x) < 50:
            self.target.velocity = (keyboard[key.D] * self.MOVE_SPEED, vy)
        elif(runner_y) > 1950:
            self.target.velocity = (vx, -keyboard[key.S] * self.MOVE_SPEED)
        elif(runner_y) < 50:
            self.target.velocity = (vx, keyboard[key.W] * self.MOVE_SPEED)
        else:
            self.target.velocity = (vx, vy)

        vx, vy = self.target.velocity

        dx = vx * dt
        dy = vy * dt

        last = self.target.get_rect()

        new = last.copy()
        new.x += dx
        new.y += dy

        self.target.position = new.center
        scroller.set_focus(*new.center)

        self.target.cshape.center = eu.Vector2(*self.target.position)


class runner(cocos.sprite.Sprite):
    def __init__(self, image):
        super(runner, self).__init__(image)
        self.position = 200, 200
        move_speed = random.randint(1, 8)
        move_1 = MoveTo((1800, 1800), move_speed) + MoveTo((200, 200), move_speed) + \
            MoveTo((1800, 200), move_speed) + MoveTo((200, 1800), move_speed)
        repeat = Repeat(move_1)
        self.cshape = cm.AARectShape(eu.Vector2(*self.position), 50, 50)
        self.do(repeat)

    def update_(self):
        self.cshape.center = eu.Vector2(*self.position)


class player(cocos.sprite.Sprite):
    def __init__(self, image, worldRect):
        super(player, self).__init__(image)
        self.position = (100, 100)
        self.anchor = 50, 50
        self.cshape = cm.AARectShape(eu.Vector2(*self.position), 50, 50)


class Rect(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class BackgroundLayer(cocos.layer.ScrollableLayer):
    def __init__(self):
        super().__init__()
        background = cocos.sprite.Sprite("Grass.png")
        background.position = 1000, 1000

        base1 = cocos.sprite.Sprite("base.png")
        base2 = cocos.sprite.Sprite("base.png")
        base3 = cocos.sprite.Sprite("base.png")
        base4 = cocos.sprite.Sprite("base.png")
        base1.position = 200, 200
        base2.position = 1800, 1800
        base3.position = 200, 1800
        base4.position = 1800, 200
        self.add(background)
        self.add(base1)
        self.add(base2)
        self.add(base3)
        self.add(base4)

        self.worldRect = Rect(0, 0, 2000, 2000)

        self.runner1 = runner(pyglet.resource.image("Runner.png"))
        self.player = player(pyglet.resource.image(
            "Thrower.png"), self.worldRect)
        mover = Mover(self.worldRect)
        self.player.do(mover)
        self.add(self.runner1)
        self.rando = 10
        i = 1
        while i < self.rando:
            self.newRunner = runner(pyglet.resource.image("Runner.png"))
            self.add(self.newRunner)
            i += 1
        self.add(self.player)

        self.coll_manager = cm.CollisionManager()

        self.instructions = cocos.text.Label("Use WASD to move around and tag the runners!",
                                             font_name='Verdana',
                                             font_size=32,
                                             anchor_x='center', anchor_y='center')
        self.instructions.position = 700, -50
        self.add(self.instructions)

    def update(self, dt):
        self.runner1.update_()
        if self.player.cshape.overlaps(self.runner1.cshape):
            self.you_win()

    def you_win(self):
        self.win = cocos.text.Label("YOU WIN!!!!!!!!!!!",
                                    font_name='Verdana',
                                    font_size=60,
                                    anchor_x='center', anchor_y='center',
                                    color=(0, 0, 0, 10))
        self.win.position = self.player.position[0], self.player.position[1] + 100
        self.add(self.win)
        self.player.pause()
        self.runner1.pause()


if __name__ == "__main__":
    global keyboard, scroller, CollisionManager
    window = cocos.director.director.init(
        width=WIDTH, height=HEIGHT, caption="Tag", resizable=True, autoscale=True)
    director.set_show_FPS(True)
    director.window.pop_handlers()

    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    bg_layer = BackgroundLayer()

    scroller = cocos.layer.ScrollingManager()
    scroller.add(bg_layer)

    gameScene = cocos.scene.Scene()

    gameScene.schedule_interval(bg_layer.update, 1/60)

    gameScene.add(scroller)

    director.run(gameScene)
