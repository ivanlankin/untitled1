import pygame
import requests
import sys
import os
cords = input("кординаты 1 х 2 у").split()
mashtab = input('маштаб').split()
response = None
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

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

os.remove(map_file)
