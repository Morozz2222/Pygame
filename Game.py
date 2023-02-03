import csv
import random
import sys
import time
from random import randint

import pygame
from pygame.locals import *

from CONST import *
from init import *
from spritess import Player, Obstacles, Addition, load_image, EndPhoto


# Функции draw для написания текста
def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR1)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def drawText_2(text, font, surface, x, y):
    textobj = font.render(text, 2, TEXTCOLOR2)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def accounting_for_lives():
    # создадим спрайты для ведения учета жизней
    global sprite1, sprite2, sprite3
    sprite1 = pygame.sprite.Sprite()
    sprite1.image = pygame.transform.scale(load_image("car96.png"), (40, 40))
    sprite1.rect = sprite1.image.get_rect()
    sprite1.rect.x, sprite1.rect.y = 650, 20
    sprite2 = pygame.sprite.Sprite()
    sprite2.image = pygame.transform.scale(load_image("car96.png"), (40, 40))
    sprite2.rect = sprite2.image.get_rect()
    sprite2.rect.x, sprite2.rect.y = 600, 20
    sprite3 = pygame.sprite.Sprite()
    sprite3.image = pygame.transform.scale(load_image("car96.png"), (40, 40))
    sprite3.rect = sprite3.image.get_rect()

    sprite3.rect.x, sprite3.rect.y = 550, 20


def rules_text():
    # Правила
    pygame_gui.windows.UIMessageWindow(rect=pygame.Rect((150, 150), (450, 450)),
                                       manager=manager,
                                       window_title='Правила',
                                       html_message='Приветствуем тебя в нашей игре!'
                                                    'Укрывайся от камней, знаков и людей, которые проходят мимо, когда будешь ехать на машине'
                                                    'но собирай бензин - он даст тебе дополнительные очки.'
                                                    'Мы подготовили для тебя специальную кнопку, чтобы тебе легче было пройти игру'
                                                    'Нажми на клавишу [X] и твоя машинка станет меньше!'
                                                    'Помни, воспользоваться таким подарком можно только один раз,'
                                                    'но главное не врезайся в препятствия, ведь у тебя только три жизни.'
                                                    'Чтобы выйти из игры нажми на клавишу [Esc], удачи')


def end_of_play():
    pygame.display.set_caption('Gameover')
    clock = pygame.time.Clock()

    # В последнем окне появляется фото, где написано, что игра окончена
    all_sprites2 = pygame.sprite.Group()
    loose_sound.set_volume(5)
    loose_sound.play()
    _ = EndPhoto(all_sprites2, (WINDOWWIDTH, WINDOWHEIGHT))
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Выход из приложения
                pygame.quit()
                running = False
            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    running = False
                if event.key == pygame.K_SPACE:
                    windowSurface.blit(backgroundImage2, (0, 0))
                    pygame.mouse.set_visible(True)
                    start_window()
                # При нажатии на данные кнопки вы возвращаетесь в главное меню
        windowSurface.blit(backgroundImage1, (0, 0))
        drawText('Нажмите [SPACE] для выхода'
                 'в'
                 'главное меню', font, windowSurface, 130, 400)
        drawText(f"Ваш результат:{dict_info['Score']}", font, windowSurface, 150, 500)

        all_sprites2.draw(windowSurface)
        all_sprites2.update()
        pygame.display.flip()
        clock.tick(200)


def exit_go():
    # Окно, с подтверждением выхода из приложения
    pygame_gui.windows.UIConfirmationDialog(
        rect=pygame.Rect((200, 250), (250, 200)),
        manager=manager,
        window_title='Подтверждение выхода',
        action_long_desc='Вы действительно хотите закончить?',
        action_short_name='OK',
        blocking=True)


def play():
    global ADDNEW, COUNT3, topScore, COUNT2, TF
    pygame.time.set_timer(pygame.USEREVENT, 3000)
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    start_sound.stop()
    obstacleAdd = 0
    CARS = ('dataObjects/canm.png', 'dataObjects/bandg.png', 'dataObjects/znak.png')
    CARS_SURF = []
    # Создаем список с объектами препятствий
    for event in range(len(CARS)):
        CARS_SURF.append(
            pygame.image.load(CARS[event]).convert_alpha())

    # Все группы спрайтов
    obstacle_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    addition_group = pygame.sprite.Group()
    Obstacles(CARS_SURF[randint(0, 2)], obstacle_group)
    score = 0
    play_sound.play(-1)
    # Запускаем тематическую музыку
    player = Player(player_group)
    run = True
    tick = pygame.time.get_ticks()

    lives_group = pygame.sprite.Group()
    accounting_for_lives()
    i = 0
    sprites = [sprite1, sprite2, sprite3]
    lives_group.add(sprite1, sprite2, sprite3)

    while run:
        clock.tick(FPS)
        # Счетчик будущего результата, в итоге результат будет - score // 4
        score += 1
        # if score > topScore:
        #     topScore = score

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # Счетчик появления препятствий
        obstacleAdd += 1

        # В зависимости от того, какой уровень выбрал пользователь препятствия начинают появляться быстрее
        if lev == 'Easy':
            ADDNEW = 45
            if score // 4 > 250:
                ADDNEW = 37
        if lev == 'Medium':
            ADDNEW = 35
            if score // 4 > 250:
                ADDNEW = 27
        if lev == 'Hard':
            ADDNEW = 25
            if score // 4 > 250:
                ADDNEW = 20

        if obstacleAdd == ADDNEW:
            obstacleAdd = 0
            Obstacles(CARS_SURF[randint(0, 2)], obstacle_group)

        if score // 4 > 100:
            if score // 4 == random.randint(100, score):
                # Добавление бонусов в игру, определяется случайное число от 100 до данного результата
                # Если число совпадет с текущим езультатом то выпадает бонус, дающий 100 доп. очков
                Addition(addition_group)

        for enemy in obstacle_group:
            # Проверка на столкновение с препятствиями, убирается одна жизнь при столкновении
            gets_hit = pygame.sprite.spritecollide(player, obstacle_group, True)
            if gets_hit:
                gameOverSound2.play()
                obstacle_group.remove(enemy)
                COUNT3 += 1
                sprites[i].kill()
                i += 1

        gets_hitt = pygame.sprite.spritecollide(player, addition_group, True)
        if gets_hitt:
            # Проверка на столкновение с бонусом
            score += 400

        if COUNT3 == 3:
            # Если жизни кончились(всего их три), то в csv файл заносим данные:
            # идентификатор, ник, результат, выбранный уровень, время игры
            play_sound.stop()
            time.sleep(0.5)
            dict_info['Score'] = score // 4
            tick = tick / 1000.0
            dict_info['Time'] = tick
            dk = dict_info.keys()
            with open('Statistics2.csv', mode="w", newline='', encoding="utf8") as f:
                writer = csv.DictWriter(
                    f, fieldnames=dk,
                    delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
                writer.writeheader()
                writer.writerow(dict_info)
            end_of_play()
            # Переходим в последнее окно
            run = False

        windowSurface.blit(backgroundImage1, (0, 0))

        drawText('Score: %s' % (score // 4), font, windowSurface, 10, 0)
        obstacle_group.clear(windowSurface, backgroundImage1)
        addition_group.clear(windowSurface, backgroundImage1)

        # update
        obstacle_group.update()
        addition_group.update()
        player_group.update()

        # draw
        lives_group.draw(windowSurface)
        obstacle_group.draw(windowSurface)
        addition_group.draw(windowSurface)
        player_group.draw(windowSurface)

        # flip
        pygame.display.flip()


def start_window():
    # Начальное окно
    run = True
    global identification, lev, nick
    start_sound.play(-1)
    start_sound.set_volume(0.5)
    # Запускаем мелодию, выводим текст
    drawText_2('Введите свой ник:', font2, windowSurface, 120, 360)
    drawText_2('Выберите уровень:', font2, windowSurface, 350, 360)
    drawText_2("Дорога чемпиона", font, windowSurface, 150, 80)

    while run:
        time_delta = mainClock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    go_play_sound.play()
                    exit_go()
            elif event.type == QUIT:
                gameOverSound2.play()
                # run = False
                exit_go()
            # Используем pygame_gui
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                lev = event.text
                # В переменную записываем выбраный уровень

            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                nick = event.text
                # В переменную записываем ник

            if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                # Окно с подтверждением выхода
                run = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == switch_rules:
                    # Окно с правилами
                    rules_text()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == switch_play:
                    identification += 1
                    # В ранее подготовленный словарь заносим необходимые данные
                    dict_info['Id'] = str(identification)
                    dict_info['Level'] = lev
                    dict_info['Nickname'] = nick
                    # Переходим в игру
                    play()

        manager.update(time_delta)
        manager.draw_ui(windowSurface)
        pygame.display.update()


start_window()
