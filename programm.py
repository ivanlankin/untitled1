import pygame
import requests
import sys
import os
cords = input("кординаты 1 х 2 у").split(',')
mashtab = input('маштаб').split(',')
response = None
def map_creat():
    try:
        map_request = "http://static-maps.yandex.ru/1.x/?ll="+cords[0]+","+cords[1]+"&spn="+mashtab[0]+","+mashtab[1]+"&l=map"#'https://static-maps.yandex.ru/1.x/?spn=20.002,20.002&ll='136.063527%2C-25.691701'&l=map'
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
    except:
        print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")
        sys.exit(1)

    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    return map_file
pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_creat()), (0, 0))
fps = 60
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                cords[1] = str(float(cords[1]) - 2)
                print(cords[1])
        screen.blit(pygame.image.load(map_creat()), (0, 0))
    #clock.tick(fps)
    pygame.display.flip()
pygame.quit()
os.remove(map_creat())