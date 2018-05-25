import random
import pygame

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PIPE = (57, 255, 20)
SKY = (78, 192, 202)
GROUND = (224, 215, 146)
DARK_GROUND = (124, 115, 46)
BIRD = (253, 95, 0)

size = (500, 760)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Flappy Bird")

done = False

clock = pygame.time.Clock()

introfont = pygame.font.Font("fonts/Flappy.ttf", 75)
mainfont = pygame.font.SysFont('arial', 30, False, False)
scorefont = pygame.font.Font("fonts/04B_19__.ttf", 40)


music_pipe = pygame.mixer.Sound("sounds/pipe.wav")
music_die = pygame.mixer.Sound("sounds/die.ogg")
music_flap = pygame.mixer.Sound("sounds/flap.wav")

gameState = 1

pipes = []

score = 0
highScore = 0



class Bird():
    def __init__(self):
        self.x = 250
        self.y = 250
        self.yV = 0

    def flap(self):
        self.yV = -10
        music_flap.play(0)

    def update(self):
        self.yV += 0.5
        self.y += self.yV
        if self.y >= 608:
            self.y = 608
            self.yV = 0
        if self.yV > 20:
            self.yV = 20

    def draw(self):
        pygame.draw.rect(screen, BIRD, (self.x, self.y, 40, 40))

    def reset(self):
        self.x = 250
        self.y = 250
        self.yV = 0


bird = Bird()


class Pipe():
    def __init__(self):
        self.centerY = random.randrange(130, 520)
        self.x = 800
        self.size = 100

    def update(self):
        global pipes
        global bird
        global gameState
        global score
        self.x -= 4
        if self.x == 300:
            pipes.append(Pipe())
        if self.x <= -100:
            del pipes[0]
        if self.x >= 170 and self.x <= 290 and bird.y <= (
            self.centerY - self.size) or self.x >= 170 and self.x <= 290 and (bird.y + 40) >= (
            self.centerY + self.size):
            music_die.play(0)
            gameState = 3
        if self.x == 168 and bird.y > (self.centerY - 100) and bird.y < (self.centerY + 100):
            music_pipe.play(0)
            score += 1
        if bird.y >= 608:
            music_die.play(0)
            gameState = 3

    def draw(self):
        pygame.draw.rect(screen, PIPE, (self.x, 0, 80, (self.centerY - self.size)))
        pygame.draw.rect(screen, PIPE, (self.x, (self.centerY + self.size), 80, (548 - self.centerY)))


pipes.append(Pipe())


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if gameState == 1:
                    gameState = 2
                elif gameState == 3:
                    bird.reset()
                    pipes = []
                    pipes.append(Pipe())
                    gameState = 2
                    score = 0
                else:
                    bird.flap()


    intro_back = pygame.image.load("Backgrounds/start.png").convert()
    intro_back = pygame.transform.scale(intro_back, (500, 760))
    intro_rect = intro_back.get_rect()

    pygame.draw.rect(screen, PIPE, (0, 650, 800, 50))
    pygame.draw.line(screen, DARK_GROUND, (0, 650), (800, 650), 5)
    pygame.draw.line(screen, DARK_GROUND, (0, 650), (800, 650), 5)



    if gameState == 1:
        screen.fill(PIPE)
        screen.blit(intro_back, intro_rect)
        text = introfont.render("Press space to play", True, PIPE)
        textX = text.get_rect().width
        textY = text.get_rect().height
        screen.blit(text, ((250 - (textX / 2)), (350 - (textY / 2))))

    if gameState == 2:
        screen.fill(PIPE)
        screen.blit(intro_back, intro_rect)
        bird.update()
        bird.draw()

        for pipe in pipes:
            pipe.update()
            pipe.draw()

        if score > highScore:
            highScore = score

        text = scorefont.render(str(score), True, WHITE)
        textX = text.get_rect().width
        textY = text.get_rect().height
        screen.blit(text, ((250 - (textX / 2)), (50 - (textY / 2))))

    if gameState == 3:
        screen.blit(intro_back, intro_rect)
        for pipe in pipes:
            pipe.draw()
        bird.draw()
        text = mainfont.render(("Score: " + str(score)), True, BLACK)
        textX = text.get_rect().width
        textY = text.get_rect().height
        screen.blit(text, ((250 - (textX / 2)), (300 - (textY / 2))))
        text = mainfont.render(("High Score: " + str(highScore)), True, BLACK)
        textX = text.get_rect().width
        textY = text.get_rect().height
        screen.blit(text, ((250 - (textX / 2)), (350 - (textY / 2))))
        text = mainfont.render("Press space to play again", True, BLACK)
        textX = text.get_rect().width
        textY = text.get_rect().height
        screen.blit(text, ((250 - (textX / 2)), (400 - (textY / 2))))
        text = scorefont.render(str(score), True, WHITE)
        textX = text.get_rect().width
        textY = text.get_rect().height
        screen.blit(text, ((250 - (textX / 2)), (50 - (textY / 2))))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
