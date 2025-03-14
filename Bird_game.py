import pygame
import sys
import random
import json

totalmyscores = 73737

screen_x = 1550
screen_y = 800

pygame.init()

screen = pygame.display.set_mode((screen_x, screen_y))
backgraund = pygame.transform.scale(pygame.image.load("fon3.png"), (screen_x, screen_y))

clock = pygame.time.Clock()

class Parent_class(pygame.sprite.Sprite):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(pikt).convert_alpha(), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.mask = pygame.mask.from_surface(self.image)

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Bird(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, speed):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE]:
            i = 15
            if self.rect.y < 25:
                self.rect.y = 25
            while i > 0:
                self.rect.y -= 10
                i -= 7
        self.rect.y += 3

bird1 = Bird("bird1.1.png", 20, 20, 710, 400, 6)

class Obstacle(Parent_class):
    def __init__(self, pict, size_x, size_y, pos_x, pos_y, speed):
        super().__init__(pict, size_x, size_y, pos_x, pos_y)
        self.speed_obstacle = speed

    def update(self):
        self.rect.x -= self.speed_obstacle

        if self.rect.x == -200:
            self.rect.x = 1750

     
    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Botton():
    def __init__(self, pict, size_x, size_y, pos_x, pos_y, color_text, font_type):
        self.pict_botton = pict
        self.image = pygame.transform.scale(pygame.image.load(pict), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.size_x = size_x
        self.size_y = size_y
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.color = color_text
        self.type = font_type

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

    def click(self):
        global play
        for evt in pygame.event.get():
            if evt.type == pygame.MOUSEBUTTONDOWN:
                x, y = evt.pos
                if self.collidepoint(x, y):
                    bird1.rect.x = 710
                    bird1.rect.y = 400
                    print("ыыыы рестарт")
                    obstacle1.rect.x = 1800
                    obstacle1.rect.y = 700
                    

                    player_scores["Gamers"]["Grisha"].append(scores)
                    with open("scores.json", "w", encoding="utf-8") as file:
                        json.dump(player_scores, file)
                    play = True



botton1 = Botton("restart.png", 120, 60, 717, 395, 200, "Calibri")


scores = 0
f1 = pygame.font.SysFont('Caladea', 36)
text1 = f1.render("Grisha's Scores:" + str(scores), True, (0, 200, 0))

f2 = pygame.font.SysFont('Caladea', 36)
text2 = f2.render("restart", True, (0, 0, 0))

f3 = pygame.font.SysFont('Caladea', 36)
text3 = f3.render("Press space to restart", True, (20, 55, 5))

obstacles = pygame.sprite.Group()
obstacles2 = pygame.sprite.Group()
obstacles3 = pygame.sprite.Group()
my_images = ["obstacle.png", "obstacle2.png", "obstacle3.png", "obstacle4.png"]
obstacle1 = Obstacle("obstacle1.png", 100, random.randint(100, 400), 1800, 700, 5) # низ
obstacle2 = Obstacle("obstacle2.png", 100, random.randint(100, 300), 2200, 700, 5) #низ
obstacle3 = Obstacle("obstacle3.png", 100, random.randint(200, 500), 1800, 0, 5)
obstacle4 = Obstacle("obstacle4.png", 100, random.randint(400, 450), 2200, 0, 5)
obstacle5 = Obstacle("obstacle5.png", 100, random.randint(400, 450), 2000, 0, 5)
obstacle6 = Obstacle("obstacle6.png", 100, random.randint(300, 350), 2000, 600, 5)
obstacles.add(obstacle1)
obstacles.add(obstacle2)
obstacles.add(obstacle6)
obstacles2.add(obstacle3)
obstacles2.add(obstacle4)
obstacles2.add(obstacle5)
obstacles3.add(obstacle1)
obstacles3.add(obstacle2)
obstacles3.add(obstacle3)
obstacles3.add(obstacle4)
obstacles3.add(obstacle5)
obstacles3.add(obstacle6)

play = True

'''pygame.mixer.init()
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.1)'''


with open("scores.json", encoding='UTF-8') as file:
    player_scores = json.load(file)

user = 0

game = True

while game:
    
    if play:
        scores_player = scores

        screen.blit(backgraund, (0, 0))

        obstacle1.reset()
        obstacle1.update()
        
        obstacle2.reset()
        obstacle2.update()
       
        obstacle3.reset()
        obstacle3.update()
        
        obstacle4.reset()
        obstacle4.update()
       
        obstacle5.reset()
        obstacle5.update()

        obstacle6.reset()
        obstacle6.update()

        bird1.reset()
        bird1.update()


        screen.blit(text1, (50, 50))

        if bird1.rect.y >= 750:
            play = False
            player_scores["Gamers"]["Grisha"].append(scores)
            with open("scores.json", "w", encoding="utf-8") as file:
                json.dump(player_scores, file)
            

        if pygame.sprite.spritecollide(bird1, obstacles3, False, pygame.sprite.collide_mask):
            play = False
            player_scores["Gamers"]["Grisha"].append(scores)
            with open("scores.json", "w", encoding="utf-8") as file:
                json.dump(player_scores, file)

        if bird1.rect.bottomleft[0] == obstacle1.rect.topright[0] or bird1.rect.bottomleft[0] == obstacle2.rect.topright[0] or bird1.rect.bottomleft[0] == obstacle6.rect.topright[0]:
            scores += 1
            text1 = f1.render("Grishas's Scores:" + str(scores), True, (0, 200, 0))
        screen.blit(text1, (50, 50))

    if play == False:
        botton1.reset()
        botton1.click()
        screen.blit(text2, (725, 400))
        screen.blit(text3, (605, 450))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(60) 