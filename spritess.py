from random import randint
import sys, os

# from pygame.locals import *
from init import *
from CONST import *
import random


# Обработка изображений
def load_image(name, colorkey=None):
    fullname = os.path.join('dataObjects', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# Отображение оставшихся жизней в игре
class PlayerLives(pygame.sprite.Sprite):
    def __init__(self, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(load_image("car48.png"), (30, 30))
        self.rect = self.image.get_rect(center=(300, 350))


# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(load_image("car96.png"), (80, 80))
        # self.image.set_colorkey()
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOWWIDTH // 2
        self.rect.bottom = WINDOWHEIGHT - 650
        self.add(group)

    def update(self):
        # По умолчанию делаем игрока статичным на экране.
        # Затем выполняется проверка, выполняется ли обработка событий для нажатых клавиш со стрелками
        global COUNT2
        self.player_pos_x = 0
        self.player_pos_y = 0

        # Получаем список клавиш, которые были нажаты
        keystone = pygame.key.get_pressed()
        # Контролируем передвижение
        if keystone[pygame.K_LEFT]:
            self.player_pos_x = -PLAYERMOVERATE
        elif keystone[pygame.K_RIGHT]:
            self.player_pos_x = PLAYERMOVERATE
        if keystone[pygame.K_UP]:
            self.player_pos_y = -PLAYERMOVERATE
        elif keystone[pygame.K_DOWN]:
            self.player_pos_y = PLAYERMOVERATE

        # При нажатии специальной кнопки машинка становится в два раза меньше
        if keystone[pygame.K_x]:
            if COUNT2 == 0:
                self.image = load_image("car48.png")
                COUNT2 += 1
        else:
            self.image = pygame.transform.scale(load_image("car96.png"), (80, 80))

        # Проверка границ слева и справа
        if self.rect.x > WINDOWWIDTH:
            self.rect.x = 0
        if self.rect.x < 0:
            self.rect.x = WINDOWWIDTH
        if self.rect.y > WINDOWHEIGHT:
            self.rect.y = 0
        if self.rect.y < 0:
            self.rect.y = WINDOWHEIGHT

        self.rect.x += self.player_pos_x
        self.rect.y += self.player_pos_y


# Класс с препятствиями
class Obstacles(pygame.sprite.Sprite):
    def __init__(self, surf, group):
        pygame.sprite.Sprite.__init__(self)
        global BADDIEMINSIZE, BADDIEMAXSIZE, BADDIEMINSPEED, BADDIEMAXSPEED
        # В зависимости от уровня устанавливаеим диапазон скорости и размера
        if lev == 'Medium':
            BADDIEMINSIZE = 40
            BADDIEMAXSIZE = 60
        if lev == 'Hard':
            BADDIEMINSIZE = 50
            BADDIEMAXSIZE = 60
            BADDIEMINSPEED = 5
            BADDIEMAXSPEED = 7
        self.image = pygame.transform.scale(surf, (random.randint(BADDIEMINSIZE, BADDIEMAXSIZE),
                                                   random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)))
        self.rect = self.image.get_rect()
        self.rect.x = randint(1, WINDOWWIDTH)
        self.rect.y = 700

        # добавляем в группу
        # у машин будет разная скорость
        self.speed = random.randint(BADDIEMINSPEED, BADDIEMAXSPEED)
        self.add(group)

    def update(self):
        # Скорость
        if self.rect.y > 0:
            self.rect.y -= self.speed
        else:
            # теперь не перебрасываем вверх,
            # а удаляем из всех групп
            self.kill()


# Класс с бонусом
class Addition(pygame.sprite.Sprite):
    def __init__(self, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('dataObjects/benz.png').convert_alpha()
        self.rect = self.image.get_rect()
        # Устанавливаем случайную позицию вылета и скорость
        self.rect.x = randint(1, WINDOWWIDTH)
        self.rect.y = 700
        self.speed = random.randint(4, 6)
        self.add(group)

    def update(self):
        if self.rect.y > 0:
            self.rect.y -= self.speed
        else:
            self.kill()


# Фото в завершающем окне
class EndPhoto(pygame.sprite.Sprite):
    image_right = None
    image_left = None

    def __init__(self, group, size):
        super().__init__(group)
        EndPhoto.image_right = load_image("gameover22.png")
        EndPhoto.image_left = pygame.transform.flip(EndPhoto.image_right, True, False)
        self.width, self.height = size
        self.image = EndPhoto.image_right
        self.rect = self.image.get_rect()
        self.rect.left = -600

    def update(self):
        # Постепенно "выплывает" с опред. скоростью
        if self.rect.left < 0:
            self.rect.left += 1.5
