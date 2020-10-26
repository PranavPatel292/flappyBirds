import pygame
import numpy as np
import math
pygame.init()
pygame.display.set_caption("Flappy Birds")
run = True
win = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
counter = 0
val = 3.0
bg = pygame.image.load('./src/images/bg.jpg')
TOTAL = 1
birds = []
savedBirds = []

hit = False
sprite = [pygame.image.load('./src/images/flappy_birds_03.png'), pygame.image.load('./src/images/flappy_birds_02.png'), pygame.image.load('./src/images/flappy_birds_01.png')] # Credit:- https://github.com/sourabhv/FlapPyBird/tree/master/assets/sprites


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


class bird:
    def __init__(self, wih, who):

        self.x = 20
        self.y = int(np.random.uniform(0, 400))
        self.gravity = 0.01
        self.val = 0
        self.fitness = 0.0
        self.score = 0.0
        self.wih = wih
        self.who = who
        self.birdCount = 0


    def draw_bird(self):
        sprite[self.birdCount] = pygame.transform.scale(sprite[self.birdCount], (20,20))
        win.blit(sprite[self.birdCount], (self.x, self.y))
        self.birdCount +=1
        if self.birdCount == 3:
            self.birdCount = 0

        # pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), 10)

    def update(self):
        self.val += self.gravity * 6.9
        self.y += int(math.ceil(self.val))
        self.val = 7

    def up(self):
        # self.val += int(math.ceil(self.gravity) * 0.5)
        self.y -= int(math.ceil(37*0.4))

    def bird_nural_network(self, input_nodes, p1):
        m1 = []
        m1.append(self.y / 400.0)
        m1.append(p1.xloc / 400.0)
        m1.append(p1.ysize / 400.0)
        m1.append((p1.yloc + p1.space + p1.ysize + 50) / 400.0)
        m1.append(self.val / 10.0)
        m1 = np.reshape(m1, (input_nodes, 1))
        hidden_01 = sigmoid(np.dot(self.wih, m1))
        output = sigmoid(np.dot(self.who, hidden_01))

        return output

    def mutate(self, wih, who, MR):
        self.wih *= MR
        self.who *= MR


class pipe:
    def __init__(self):
        self.xloc = 200
        self.yloc = 0
        self.xsize = 50
        self.ysize = int(np.random.uniform(0, 250))
        self.space = 100

    def obst(self):
        pygame.draw.rect(win, (0, 34, 255), (self.xloc, self.yloc, self.xsize, self.ysize))
        pygame.draw.rect(win, (255, 0, 0), (self.xloc, self.yloc+self.space+self.ysize+50, self.xsize, (400 - self.ysize) * 0.8))


for i_ in range(0 ,TOTAL):
    wih = [[ 0.8966073,   0.72380709, -0.54097643, -0.83709224,  0.18913336],
 [ 0.69612567,  0.6957421,  -0.99054107,  0.84730983, -0.10480697],
 [-0.1616458,  -0.50842527, -0.87352018, -0.54744702, -0.40013167],
 [ 0.08365708,  0.75491527,  0.75943065, -0.07970506, -0.0539899 ],
 [ 0.16585281, -0.02287557, -0.13984885,  0.1226917,   0.83178329],
 [-0.1741504,   0.75049286, -0.25146313, -0.12191447, -0.21820628],
 [-0.10000038,  0.6150552,  -0.68120268,  0.85945039, -0.93373793],
 [ 0.40914554, -0.56463164, -0.01469176, -0.11827222, -0.90701965],
 [-0.48877335,  0.22649128, -0.60419919, -0.62454319, -0.85067383],
 [-0.22780587,  0.54047259, -0.74986416, -0.680767,    0.11483972],
 [-0.8494589,  -0.39171963, -0.02970757, -0.91527806,  0.32403367],
 [ 0.30536281,  0.3683013,  -0.69566597, -0.26735361, -0.74759807],
 [ 0.41065579,  0.40604243,  0.60030062, -0.9810002,   0.64687367],
 [-0.35502107 , 0.11987233, -0.73937632, -0.80377817, -0.64624687],
 [-0.82768676,  0.04942528, -0.68878522, -0.50667821, -0.99140717],
 [ 0.91497972, -0.85720216, -0.71674094,  0.92566441,  0.92432259]]

    who=  [[-0.05822779,  0.14473684, -0.78183554,  0.17789052,  0.4523775,   0.99984206,
  -0.6902925,  -0.24827687, -0.23596389,  0.81886912,  0.7487535,  -0.94541102,
  -0.98839935, -0.5979785,  -0.06018369,  0.30562823]]
    birds.append(bird(wih, who))

p1 = pipe()

while run:
    pygame.time.delay(0)
    win.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    p1.xloc -= 5
    p1.obst()

    for i_ in range(len(birds)):
        birds[i_].draw_bird()
        birds[i_].update()
        output = birds[i_].bird_nural_network(5, p1)
        birds[i_].score += 1

        if birds[i_].score % 1000 == 0:
            print(birds[i_].score)

        if output[0][0] <= 0.5:
            birds[i_].up()

        if birds[i_].y >= 390:
            birds[i_].y = 390
            birds[i_].val = 0

        if birds[i_].y < 0:
            birds[i_].y = 10

        # if keys[pygame.K_SPACE]:
        #     birds[i_].up()
    for b_ in range(len(birds)):
        if birds[b_].x <= p1.xloc and birds[b_].x >= p1.xloc:
            if birds[b_].y <= p1.ysize or birds[b_].y >= p1.yloc + p1.space + p1.ysize + 50:
                print("hit")
                run = False
    if p1.xloc <= 0:
        p1.xloc = 400
        p1.ysize = int(np.random.uniform(0, 250))


    pygame.display.update()
    clock.tick(60)

pygame.quit()