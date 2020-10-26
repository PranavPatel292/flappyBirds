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
TOTAL = 350
birds = []
savedBirds = []
hit = False


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

    def draw_bird(self):
        pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), 10)

    def update(self):
        self.val += self.gravity * 6.9
        self.y += int(math.ceil(self.val))
        self.val = 7

    def up(self):
        # self.val += int(math.ceil(self.gravity) * 0.5)
        self.y -= int(math.ceil(37*0.4))

    def bird_nural_network(self, input_nodes, p1):
        LR = 0.01
        m1 = []
        m1.append(self.y / 400.0)
        m1.append(p1.xloc / 400.0)
        m1.append(p1.ysize / 400.0)
        m1.append((p1.yloc + p1.space + p1.ysize + 50) / 400.0)
        m1.append(self.val / 10.0)
        # print m1[04]
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
        pygame.draw.rect(win, (255, 0, 0), (self.xloc, self.yloc+self.space+self.ysize+1, self.xsize, 400 - self.ysize))


def calcateFitness(savedBirds):
    sum_ = 0.0
    f = []
    for bi_ in range(len(savedBirds)):
        sum_ += savedBirds[bi_].score

    for bi_ in range(len(savedBirds)):
        # print saved_birds[bi_].score / sum_
        savedBirds[bi_].fitness = savedBirds[bi_].score / sum_
        savedBirds[bi_].score = 0

    for j_ in range(len(savedBirds)):
        r = (savedBirds[int(np.random.uniform(0, len(savedBirds)))])
        birds.append(bird(r.wih, r.who))
        birds[j_].mutate(birds[j_].wih, birds[j_].who, 0.01)


for i_ in range(0 , TOTAL):
    wih = np.random.uniform(-1, 1, size=(16, 5))
    who = np.random.uniform(-1, 1, size=(1, 16))
    birds.append(bird(wih, who))

p1 = pipe()
while run:
    pygame.time.delay(2)
    win.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    if len(birds) == 0:
        run = False
    #     print "Next Genration", counter + 1
    #     counter += 1
    #     calcateFitness(savedBirds)
    #     # run = False
    #     savedBirds = []

    keys = pygame.key.get_pressed()
    p1.xloc -= 5
    p1.obst()



    for i_ in range(len(birds)):
        birds[i_].draw_bird()
        birds[i_].update()
        output = birds[i_].bird_nural_network(5, p1)
        birds[i_].score += 1
       # if len(birds) == 1:
           #  print birds[i_].who
            # print birds[i_].wih

        if birds[i_].score > 1000:
            print("Good Bird")
            print(birds[i_].score)
            g = len(birds[i_].who)
            k = len(birds[i_].wih)

            print("WHO", birds[i_].who)
            print(birds[i_].wih)

            # for m_ in range(0, g):
            #     print("WHO", who[m_])

            # for n_ in range(0, k):
            #     print(wih[n_])
            run = False

        if output[0][0] <= 0.5:
            birds[i_].up()

        if birds[i_].y >= 390:
            birds[i_].y = 390
            birds[i_].val = 0

        if birds[i_].y < 0:
            birds[i_].y = 10

        # if keys[pygame.K_SPACE]:
        #     birds[i_].up()

    index_ = []

    for b_ in range(len(birds)):
        if birds[b_].x <= p1.xloc and birds[b_].x >= p1.xloc:
            if birds[b_].y <= p1.ysize or birds[b_].y >= p1.yloc + p1.space + p1.ysize + 1:
                index_.append(birds.index(birds[b_]))
    if len(index_) > 0:
        for i_ in reversed(range(len(index_))):
            savedBirds.append(birds[index_[i_]])
            # print "save", len(savedBirds)
            del birds[index_[i_]]



    if p1.xloc <= 0:
        p1.xloc = 400
        p1.ysize = int(np.random.uniform(0, 250))


    pygame.display.update()
    clock.tick(60)

pygame.quit()