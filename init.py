import pygame, pygame_gui
from CONST import *

# инициализация pygame и создание окна
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Дорога чемпиона")

# Загрузка шрифтов.
font = pygame.font.Font("Fonts\TrainOne-Regular.ttf", 30)
font2 = pygame.font.SysFont("gabriola", 30)
font3 = pygame.font.SysFont("gabriola", 40)

# Словарь с данными для csv
dict_info = {'Id': '',
             'Nickname': '',
             'Level': '',
             'Time': '',
             'Score': ''}
lev = 'Easy'
nick = ''
timee = ''
identification = 0
score = 0

# Загрузка звуков.
gameOverSound = pygame.mixer.Sound('dataObjects/gameover.wav')
gameOverSound2 = pygame.mixer.Sound('dataObjects/gameOver2.mp3')
play_sound = pygame.mixer.Sound('dataObjects/play sound2.mp3')
start_sound = pygame.mixer.Sound('dataObjects/start sound.mp3')
loose_sound = pygame.mixer.Sound('dataObjects/lose sound.mp3')
go_play_sound = pygame.mixer.Sound('dataObjects/go play sound2.mp3')
pygame.mixer.music.load('dataObjects/background.mid')

# Загрузка изображений фона игры
backgroundImage1 = pygame.image.load('dataObjects/road2.jpg')
backgroundImage1 = pygame.transform.scale(backgroundImage1, (WINDOWWIDTH, WINDOWHEIGHT))
backgroundImage2 = pygame.image.load('dataObjects/road3.jpg')
backgroundImage2 = pygame.transform.scale(backgroundImage2, (WINDOWWIDTH, WINDOWHEIGHT))

windowSurface.blit(backgroundImage2, (0, 0))

# Инициализация pygame_gui: линия ввода, надписи, выпдающий выбор
manager = pygame_gui.UIManager((WINDOWWIDTH, WINDOWHEIGHT))

difficulty = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
    options_list=['Easy', 'Medium', 'Hard'], starting_option='Easy',
    relative_rect=pygame.Rect((350, 396), (205, 40)),
    manager=manager)

entry = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((120, 396), (205, 40)), manager=manager)

switch_rules = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((120, 310), (435, 30)),
                                            text='Правила', manager=manager)

switch_play = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((120, 500), (435, 30)),
                                           text='Начать игру', manager=manager)
