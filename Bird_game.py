import pygame
import sys
import random
import json
import os

# Инициализация игры
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

# Звуки
jamp_sound = pygame.mixer.Sound("jampsound.wav")
lose_sound = pygame.mixer.Sound("losesound.wav")
lose_sound.set_volume(0.5)

class Bird(Parent_class):
    def __init__(self, pikt, size_x, size_y, pos_x, pos_y, speed):
        super().__init__(pikt, size_x, size_y, pos_x, pos_y)
        self.speed = speed
        self.original_y = pos_y
        self.jumping = False
        self.jump_count = 0

    def update(self):
        keys_pressed = pygame.key.get_pressed()
        
        if keys_pressed[pygame.K_SPACE] and not self.jumping:
            self.jumping = True
            self.jump_count = 15
            jamp_sound.set_volume(0.1)
            jamp_sound.play()
        
        if self.jumping:
            if self.jump_count > 0:
                self.rect.y -= 15
                self.jump_count -= 1
            else:
                self.jumping = False
        
        self.rect.y += 3
        
        if self.rect.y < 25:
            self.rect.y = 25

    def reset_position(self):
        self.rect.y = self.original_y
        self.jumping = False
        self.jump_count = 0

bird1 = Bird("bird1.1.png", 20, 20, 710, 400, 6)

class Obstacle(Parent_class):
    def __init__(self, pict, size_x, size_y, pos_x, pos_y, speed):
        super().__init__(pict, size_x, size_y, pos_x, pos_y)
        self.speed_obstacle = speed
        self.original_x = pos_x
        self.original_y = pos_y

    def update(self):
        self.rect.x -= self.speed_obstacle
        if self.rect.x < -200:
            self.rect.x = 1750
            if "obstacle1.png" in self.image:
                self.rect.height = random.randint(100, 400)
            elif "obstacle2.png" in self.image:
                self.rect.height = random.randint(100, 300)
            elif "obstacle3.png" in self.image:
                self.rect.height = random.randint(200, 500)
            elif "obstacle4.png" in self.image:
                self.rect.height = random.randint(400, 450)
            elif "obstacle5.png" in self.image:
                self.rect.height = random.randint(400, 450)
            elif "obstacle6.png" in self.image:
                self.rect.height = random.randint(300, 350)
            self.image = pygame.transform.scale(pygame.image.load(self.image), (100, self.rect.height))

    def reset_position(self):
        self.rect.x = self.original_x
        self.rect.y = self.original_y

# Создание препятствий
obstacle1 = Obstacle("obstacle1.png", 100, random.randint(100, 400), 1800, 700, 5)
obstacle2 = Obstacle("obstacle2.png", 100, random.randint(100, 300), 2200, 700, 5)
obstacle3 = Obstacle("obstacle3.png", 100, random.randint(200, 500), 1800, 0, 5)
obstacle4 = Obstacle("obstacle4.png", 100, random.randint(400, 450), 2200, 0, 5)
obstacle5 = Obstacle("obstacle5.png", 100, random.randint(400, 450), 2000, 0, 5)
obstacle6 = Obstacle("obstacle6.png", 100, random.randint(300, 350), 2000, 600, 5)

obstacles3 = pygame.sprite.Group(obstacle1, obstacle2, obstacle3, obstacle4, obstacle5, obstacle6)

class Button():
    def __init__(self, pict, size_x, size_y, pos_x, pos_y, color_text, font_type):
        self.image = pygame.transform.scale(pygame.image.load(pict), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.color = color_text
        self.font = pygame.font.SysFont(font_type, 36)
        self.text = self.font.render("Restart", True, color_text)
        
    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(self.text, (self.rect.x + 20, self.rect.y + 15))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

button1 = Button("restart.png", 120, 60, 717, 395, (0, 0, 0), "Calibri")

# Инициализация системы результатов
def init_scores():
    scores_file = "scores.json"
    default_scores = {"players": {}}
    
    if not os.path.exists(scores_file):
        with open(scores_file, "w", encoding="utf-8") as file:
            json.dump(default_scores, file)
        return default_scores
    
    try:
        with open(scores_file, encoding='UTF-8') as file:
            data = json.load(file)
            # Проверяем структуру файла
            if "players" not in data:
                data = default_scores
                with open(scores_file, "w", encoding="utf-8") as file:
                    json.dump(data, file)
            return data
    except (json.JSONDecodeError, IOError):
        return default_scores

player_scores = init_scores()

# Игровые переменные
play = True
scores = 0
current_player = ""
f1 = pygame.font.SysFont('Caladea', 36)
text1 = f1.render(f"Score: {scores}", True, (0, 200, 0))

# Поле ввода
font = pygame.font.Font(None, 36)
input_text = ""
active = False
input_rect = pygame.Rect(600, 300, 200, 40)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive

# Музыка
'''pygame.mixer.music.load('music1.wav')
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)'''

def show_high_scores():
    # Получаем топ-5 результатов
    high_scores = []
    for player, scores_list in player_scores["players"].items():
        if scores_list:  # Проверяем, есть ли результаты у игрока
            high_scores.append((player, max(scores_list)))
    
    high_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Отображаем таблицу
    title = f1.render("High Scores:", True, (255, 255, 255))
    screen.blit(title, (screen_x - 250, 50))
    
    for i, (player, score) in enumerate(high_scores[:5]):
        score_text = f1.render(f"{i+1}. {player}: {score}", True, (255, 255, 255))
        screen.blit(score_text, (screen_x - 250, 90 + i * 40))

game = True

while game:
    if play:
        screen.blit(backgraund, (0, 0))
        
        for obstacle in obstacles3:
            obstacle.update()
            obstacle.reset()
            
            if bird1.rect.bottomleft[0] == obstacle.rect.topright[0]:
                scores += 1
                text1 = f1.render(f"Score: {scores}", True, (0, 200, 0))
        
        bird1.update()
        bird1.reset()
        
        screen.blit(text1, (50, 50))
        show_high_scores()
        
        if bird1.rect.y >= 750 or pygame.sprite.spritecollide(bird1, obstacles3, False, pygame.sprite.collide_mask):
            play = False
            lose_sound.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if not play:
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = input_rect.collidepoint(event.pos)
                color = color_active if active else color_inactive
                
                if button1.is_clicked(event.pos) and input_text:
                    current_player = input_text
                    # Добавляем результат
                    if current_player not in player_scores["players"]:
                        player_scores["players"][current_player] = []
                    player_scores["players"][current_player].append(scores)
                    
                    # Сохраняем в файл
                    with open("scores.json", "w", encoding="utf-8") as file:
                        json.dump(player_scores, file)
                    
                    # Рестарт игры
                    play = True
                    scores = 0
                    text1 = f1.render(f"Score: {scores}", True, (0, 200, 0))
                    bird1.reset_position()
                    for obstacle in obstacles3:
                        obstacle.reset_position()
                    input_text = ""
                    #pygame.mixer.music.play(-1)
            
            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    current_player = input_text
                    active = False
                    color = color_inactive
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
    
    if not play:
        screen.blit(backgraund, (0, 0))
        button1.reset()
        
        label = f1.render("Enter your name:", True, (255, 255, 255))
        screen.blit(label, (input_rect.x, input_rect.y - 40))
        pygame.draw.rect(screen, color, input_rect, 2)
        text_surface = font.render(input_text, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        input_rect.w = max(200, text_surface.get_width() + 10)
        
        instruction = f1.render("Press SPACE to jump, enter name and click RESTART", True, (20, 55, 5))
        screen.blit(instruction, (500, 450))
        
        current_score = f1.render(f"Your score: {scores}", True, (255, 255, 0))
        screen.blit(current_score, (650, 200))
        
        show_high_scores()

    pygame.display.update()
    clock.tick(60)