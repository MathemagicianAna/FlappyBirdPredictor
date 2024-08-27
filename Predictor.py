import tkinter as tk
from random import *
import math


class Bird:
    # def __init__(self):
    #     #     self.x = 50
    #     #     self.y = 300
    #     #     self.speed = 0
    #     #     self.image = tk.PhotoImage(file='images/bird.png')
    #     #     self.image_id = canvas.create_image(self.x, self.y, image=self.image)
    #     #     self.genome = [uniform(-1, 1), uniform(-1, 1), uniform(-1, 1)]
    #     #     self.jump_reload = True
    #     #     self.live = True
    #     #     self.score = 0

    def __init__(self, genome=[]):
        self.x = 50
        self.y = 300
        self.speed = 0
        self.image = tk.PhotoImage(file='images/bird.png')
        self.image_id = canvas.create_image(self.x, self.y, image=self.image)

        if genome:
            self.genome = genome
        else:
            self.genome = [uniform(-1, 1), uniform(-1, 1), uniform(-1, 1)]

        self.jump_reload = True
        self.live = True
        self.score = 0

    def move(self, pipe):
        self.score += 1
        canvas.coords(self.image_id, self.x, self.y)
        self.speed += 0.2
        self.y += self.speed

        if self.x+self.image.width()/2 > pipe.x-pipe.image_pipetop.width()/2:
            if self.x-self.image.width()/2 < pipe.x+pipe.image_pipetop.width()/2:
                if self.y-self.image.height()/2 < pipe.window_start_y or self.y+self.image.height()/2 > pipe.window_start_y+pipe.window_gap:
                    self.live = False

    def jump(self):
        if self.jump_reload == False: return
        self.jump_reload = False
        window.after(200, self.jump_update)

        self.speed = -5

    def jump_update(self):
        self.jump_reload = True

    def think(self, pipe):
        n1 = self.y
        n2 = pipe.window_start_y
        n3 = pipe.window_start_y + pipe.window_gap

        out = n1 * self.genome[0] + n2 * self.genome[1] + n3 * self.genome[2]

        if out > 0:
            self.jump()


class Pipe:
    def __init__(self):
        self.x = 250
        self.window_start_y = 200
        self.window_gap = 120
        self.speed = 2
        self.image_pipetop = tk.PhotoImage(file='images/pipeTop.png')
        self.image_pipebottom = tk.PhotoImage(file='images/pipeBottom.png')
        self.image_top_start = self.window_start_y-self.image_pipetop.height()/2
        self.image_bottom_start = self.window_start_y+self.image_pipetop.height()/2+self.window_gap
        self.image_pipetop_id = canvas.create_image(self.x, self.image_top_start, image=self.image_pipetop)
        self.image_pipebottom_id = canvas.create_image(self.x, self.image_bottom_start, image=self.image_pipebottom)

    def move(self):
        self.x -= self.speed
        canvas.coords(self.image_pipetop_id, self.x, self.image_top_start)
        canvas.coords(self.image_pipebottom_id, self.x, self.image_bottom_start)

        if self.x < -self.image_pipetop.width()/2:
            self.reload()

    def reload(self):
        self.x = 300+self.image_pipetop.width()/2
        self.window_start_y = randint(20, 350)
        self.image_top_start = self.window_start_y-self.image_pipetop.height()/2
        self.image_bottom_start = self.window_start_y+self.image_pipetop.height()/2+self.window_gap

window = tk.Tk()
window.geometry("300x500")
window.title("flappy bird")

canvas = tk.Canvas(window, width=300, height=500, bg='#70c5ce')
canvas.pack()

birds = []
for i in range(30):
    birds.append(Bird())

pipe = Pipe()

bestbird = {
    'genome': [],
    'score': 0,
}

for i in range(len(birds)):
    if birds[i].score > bestbird['score']:
        bestbird['genome'] = birds[i].genome
        bestbird['score'] = birds[i].score

#window.bind('<Button-1>', bird.jump)

def main():

    global birds

    for i in range(len(birds)):
        birds[i].move(pipe)
        birds[i].think(pipe)

    birds = [bird for bird in birds if bird.live == True]

    for i in range(len(birds)):
        if birds[i].score > bestbird['score']:
            bestbird['genome'] = birds[i].genome
            bestbird['score'] = birds[i].score

    if len(birds) == 0:
        bestgenome = bestbird['genome']
        birds.append(Bird(bestgenome))
        for i in range(30):
            mutation_genome = [bestgenome[0], bestgenome[1], bestgenome[2]]
            mutation_genome[randint(0, 2)] += uniform(-1/2, 1/2)
            birds.append(Bird(mutation_genome))
        pipe.reload()

    pipe.move()
    window.after(10, main)

main()

window.mainloop()


