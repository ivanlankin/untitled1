import pygame
import requests
import sys
import os
MAX = 60
MIN = 0.0005
fps = 5
clock = pygame.time.Clock()
cords = input("кординаты 1 х 2 у через запятую ").split(',')
mashtab = input('маштаб через запятую ').split(',')
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
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if int(float(mashtab[0]) + 0.259) < MAX:
                    mashtab[0] = str(float(mashtab[0]) + 2)#0.259)
                    mashtab[1] = str(float(mashtab[1]) + 2)#0.259)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEDOWN:
                if int(float(mashtab[0]) - 0.259) > MIN:
                    mashtab[0] = str(float(mashtab[0]) - 2)# 0.259)
                    mashtab[1] = str(float(mashtab[1]) - 2)#0.259)



    screen.blit(pygame.image.load(map_creat()), (0, 0))
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()

os.remove(map_creat())
# 37.677751,55.757718
# 0.016457,0.00619
