import pygame
import requests
import sys
import os

MAX = 60
MIN = 0.0015
fps = 5
clock = pygame.time.Clock()
cords = input("кординаты 1 х 2 у через запятую ").split(',')
mashtab = input('маштаб через запятую ').split(',')
response = None
layer = "&l=map"
asd = 0

class GUI:
    def __init__(self):
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

    def render(self, surface):
        for element in self.elements:
            render = getattr(element, "render", None)
            if callable(render):
                element.render(surface)

    def update(self):
        for element in self.elements:
            update = getattr(element, "update", None)
            if callable(update):
                element.update()

    def get_event(self, event):
        for element in self.elements:
            get_event = getattr(element, "get_event", None)
            if callable(get_event):
                element.get_event(event)

class Label:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.bgcolor = pygame.Color("white")
        self.font_color = pygame.Color("black")
        self.font = pygame.font.SysFont(None, self.rect.height - 30)
        self.rendered_text = None
        self.rendered_rect = None


    def render(self, surface):
        surface.fill(self.bgcolor, self.rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 2, centery=self.rect.centery)
        surface.blit(self.rendered_text, self.rendered_rect)

class Button(Label):
    def __init__(self, rect, text):
        super().__init__(rect, text)
        self.bgcolor = pygame.Color("white")
        self.pressed = False

    def render(self, surface):
        surface.fill(self.bgcolor, self.rect)
        self.rendered_text = self.font.render(self.text, 2, self.font_color)
        if not self.pressed:
            color1 = pygame.Color("white")
            color2 = pygame.Color("black")
            self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 5, centery=self.rect.centery)
        else:
            color1 = pygame.Color("black")
            color2 = pygame.Color("white")
            self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 7, centery=self.rect.centery + 2)

        # рисуем границу
        pygame.draw.rect(surface, color1, self.rect, 2)
        pygame.draw.line(surface, color2, (self.rect.right - 1, self.rect.top), (self.rect.right - 1, self.rect.bottom), 2)
        pygame.draw.line(surface, color2, (self.rect.left, self.rect.bottom - 1),
                         (self.rect.right, self.rect.bottom - 1), 2)
        # выводим текст
        surface.blit(self.rendered_text, self.rendered_rect)

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.pressed = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.pressed = False

class TextBox(Label):
    def __init__(self, rect, text):
        super().__init__(rect, text)
        self.active = True
        self.blink = True
        self.blink_timer = 0

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.execute()
            elif event.key == pygame.K_BACKSPACE:
                if len(self.text) > 0:
                    self.text = self.text[:-1]
            else:
                self.text += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)

    def update(self):
        if pygame.time.get_ticks() - self.blink_timer > 200:
            self.blink = not self.blink
            self.blink_timer = pygame.time.get_ticks()

    def render(self, surface):
        super(TextBox, self).render(surface)
        if self.blink and self.active:
            pygame.draw.line(surface, pygame.Color("White"),
                             (self.rendered_rect.right + 2, self.rendered_rect.top + 2),
                             (self.rendered_rect.right + 2, self.rendered_rect.bottom - 2))
    def qwer(self):
        return self.text

# "http://geocode-maps.yandex.ru/1.x/?geocode=Якутск&format=json"
def map_creat():
    try:
        map_request = "http://static-maps.yandex.ru/1.x/?ll="+cords[0]+","+cords[1]+"&spn="+mashtab[0]+","+mashtab[1]+layer#'https://static-maps.yandex.ru/1.x/?spn=20.002,20.002&ll='136.063527%2C-25.691701'&l=map'
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

def finder():
    print(town)
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?geocode=" + town + "&format=json"
    response = None
    try:
        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            cen_pos = toponym["Point"]['pos'].split()
            return cen_pos
        else:
            print("Ошибка выполнения запроса:")
            print(geocoder_request)

            print("Http статус:", response.status_code, "(", response.reason, ")")
    except:
        print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")


pygame.init()
screen = pygame.display.set_mode((600, 450))
search = Button (((200, 0),(50, 50)),'Найти')
switch = Button(((550, 0), (50, 50)), 'схема')
textbox = TextBox (((0,0),(200,50)),'')
gui = GUI()
gui.add_element(switch)
gui.add_element(search)
gui.add_element(textbox)
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
                else:
                    mashtab[0] = str(MAX)
                    mashtab[1] = str(MAX)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEDOWN:
                if int(float(mashtab[0]) - 0.259) > MIN:
                    mashtab[0] = str(float(mashtab[0]) - 2)# 0.259)
                    mashtab[1] = str(float(mashtab[1]) - 2)#0.259)
                else:
                    mashtab[0] = str(MIN)
                    mashtab[1] = str(MIN)
            print(mashtab)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                cords[1] = str(float(cords[1]) + float(mashtab[0]))
                print(cords[1])
            if event.key == pygame.K_DOWN:
                cords[1] = str(float(cords[1]) - float(mashtab[0]))
                print(cords[1])
            if event.key == pygame.K_RIGHT:
                cords[0] = str(float(cords[0]) + float(mashtab[1]))
                print(cords[0])
            if event.key == pygame.K_LEFT:
                cords[0] = str(float(cords[0]) - float(mashtab[1]))
                print(cords[0])
            gui.get_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if (550 <= event.pos[0] <= 600) and (0 <= event.pos[1] <= 50):
                if asd == 0:
                    asd = 1
                elif asd == 1:
                    asd = 2
                elif asd == 2:
                    asd = 0
            if (200 <= event.pos[0] <= 250) and(0 <= event.pos[1] <= 50):
                if (textbox.qwer != ''):
                    print(textbox.qwer())
                    town = textbox.qwer()
                    cords = finder()
                    print(cords)
            gui.get_event(event)
    if asd == 0:
        layer = "&l=map"
    elif asd == 1:
        layer = "&l=sat"
    else:
        layer = "&l=skl"

    screen.blit(pygame.image.load(map_creat()), (0, 0))
    gui.render(screen)
    gui.update()
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()

os.remove(map_creat())
# 37.677751,55.757718
# 0.016457,0.00619
