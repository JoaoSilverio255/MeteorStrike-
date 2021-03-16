import pygame , sys , random


#Game init
pygame.init()
pygame.display.set_caption("Meteor Strike!")

#Globals

LIVES = 3
FONT1 = pygame.font.Font(None,40)
FPS = 60
WIDTH = 1280
HEIGHT = 720
SCORE = 0
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255,255,255)
PNG_LIST = ("Meteor Dodger Assets/Meteor1.png","Meteor Dodger Assets/Meteor2.png","Meteor Dodger Assets/Meteor3.png")
BACKGROUND = pygame.image.load("Meteor Dodger Assets/parallax-space-backgound1.png")


#Functions
def draw_surface(path,x,y):
    surface = pygame.image.load(path)
    SCREEN.blit(surface,(x,y))

def background():
    draw_surface("Meteor Dodger Assets/parallax-space-backgound1.png", 0, 0)
    draw_surface("Meteor Dodger Assets/parallax-space-stars.png", 120, 300)
    draw_surface("Meteor Dodger Assets/parallax-space-stars.png", 1000, 200)
    draw_surface("Meteor Dodger Assets/parallax-space-big-planet.png", 1000, 600)
    draw_surface("Meteor Dodger Assets/parallax-space-far-planets.png", 300, 100)
    draw_surface("Meteor Dodger Assets/parallax-space-ring-planet.png", 100, 400)

def draw_text(TEXT,FONT2,COLOR,SURFACE,X,Y):
    TEXT_SRFC = FONT2.render(TEXT,True,COLOR)
    TEXT_RECT = TEXT_SRFC.get_rect()
    TEXT_RECT.topleft = (X , Y)
    SURFACE.blit(TEXT_SRFC,TEXT_RECT)

#Classes
class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, PATH, X, Y):
        super().__init__()
        self.image = pygame.image.load(PATH)
        self.rect = self.image.get_rect(center=(X, Y))
        self.health = 3

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.screen_hitbox()
        self.show_health()

    def screen_hitbox(self):
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

    def show_health(self):
        draw_text(f"Lives : {self.health}",FONT1,WHITE,SCREEN,20,20)

    def damage_taken(self,DAMAGE):
        self.health -= DAMAGE



class Meteor(pygame.sprite.Sprite):
    def __init__(self , PATH , X , Y ,x_speed,y_speed):
        super().__init__()
        self.image = pygame.image.load(PATH)
        self.rect = self.image.get_rect(center = (X,Y))
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed

        if self.rect.centery >= 800:
            self.kill()

class Laser(pygame.sprite.Sprite):
    def __init__(self, PATH, pos, SPEED):
        super().__init__()
        self.image = pygame.image.load(PATH)
        self.rect = self.image.get_rect(center=(pos))
        self.speed = SPEED

    def update(self):
        self.rect.centery -= self.speed

        if self.rect.centery <= 0:
            self.kill()


#Sprites Group
SPACESHIP = SpaceShip("Meteor Dodger Assets/spaceship.png",640,500)
SPACESHIP_GROUP = pygame.sprite.GroupSingle()
SPACESHIP_GROUP.add(SPACESHIP)

METEOR_GROUP = pygame.sprite.Group()

LASER_GROUP = pygame.sprite.Group()

#Timer

METEOR_EVENT = pygame.USEREVENT
pygame.time.set_timer(METEOR_EVENT , 250)

#Game MECHANICS
def game_mec():
    LASER_GROUP.draw(SCREEN)
    LASER_GROUP.update()

    SPACESHIP_GROUP.draw(SCREEN)
    SPACESHIP_GROUP.update()

    METEOR_GROUP.draw(SCREEN)
    METEOR_GROUP.update()

    if pygame.sprite.spritecollide(SPACESHIP_GROUP.sprite, METEOR_GROUP, True):
        SPACESHIP_GROUP.sprite.damage_taken(1)

    for laser in LASER_GROUP:
        pygame.sprite.spritecollide(laser, METEOR_GROUP, True)

    return 1


#Game Logic
def game():
    global SCORE
    RUNNING = True
    while RUNNING:
        pygame.mouse.set_visible(False)
        for event in pygame.event.get(): #Player Input
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == METEOR_EVENT:
                METEOR_PATH = random.choice(PNG_LIST)
                X_POS = random.randrange(0,1000)
                Y_POS = random.randrange(-500,-50)
                X_SPEED = random.randrange(4,10)
                Y_SPEED = random.randrange(20,60)
                METEOR = Meteor(METEOR_PATH,X_POS,Y_POS,X_SPEED,Y_SPEED)
                METEOR_GROUP.add(METEOR)
            if event.type == pygame.MOUSEBUTTONDOWN and SPACESHIP_GROUP.sprite.health <= 0:
                SPACESHIP_GROUP.sprite.health = 3
                METEOR_GROUP.empty()
                SCORE = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if len(LASER_GROUP) < 3:
                    LASER = Laser("Meteor Dodger Assets/Laser.png",event.pos,50)
                    LASER_GROUP.add(LASER) # ##


        background()
        if SPACESHIP_GROUP.sprite.health > 0:
            SCORE += game_mec()
        else:
            game_over()
        pygame.display.update()
        CLOCK.tick(FPS)

#Game over Screen
def game_over():
        SCREEN.blit(BACKGROUND, (0, 0))
        pygame.mouse.set_visible(True)
        draw_text("Game over , you lost.",FONT1,WHITE,SCREEN,400,300)
        draw_text("Start Again? Press any mouse key!", FONT1, (255, 0, 0), SCREEN,400 , 400)
        draw_text(f"You lasted : {SCORE} seconds", FONT1, (255, 0, 0), SCREEN, 400, 350)

        if SCORE <= 30:
            draw_text(f"Just: {SCORE} seconds? You can do better than that.", FONT1, (255, 0, 0), SCREEN, 400, 600)

        elif SCORE >= 60:
            draw_text(f" Great job! You are better than most!", FONT1, (255, 0, 0), SCREEN, 400, 600)



game()

