#симулятор вождения 2D
import random
import pygame
import math

pygame.init()

# частота кадров
FPS = 60
# размеры окна
W = 600
H = 800

# цвета
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
GREEN = (0, 200, 100)
RED = (255, 70, 70)
BLUE = (90, 110, 240)

# шрифт для интерфейса
FONT = pygame.font.SysFont('garamond', 25)

# основная поверхность
sc = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

# класс пользовательской машинки, которой необходимо управлять
class UserCar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        picture = pygame.image.load('CarB.png').convert_alpha()
        self.width = 30
        self.height = self.width * 2
        self.original_image = pygame.transform.scale(picture, (self.width, self.height))
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (W // 2, H - 160))
        self.speed = 0
        self.angle = 0
        self.dx = 0
        self.dy = 0
        self.status = 'STOP'
        self.turn_status = 'NONE'
        self.speed_forward_max = 20
        self.speed_backward_max = -3
        self.speedup = 0.2
        self.brake_power = -1
        self.handling = 1
        self.friction = 0.5
        self.autopilot = False
        self.drive_status = 'MOVE'

    def turn(self):
        if self.status != 'STOP':
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            if self.status == 'FORWARD' or self.status == 'BRAKE' or self.status == 'NEUTRAL':
                handling_value = self.handling
                if self.turn_status == 'LEFT':
                    self.angle += handling_value
                elif self.turn_status == 'RIGHT':
                    self.angle -= handling_value
                else:
                    pass
            elif self.status == 'BACKWARD' or self.status == 'NEUTRAL_BACKWARD':
                handling_value = self.handling * 5
                if self.turn_status == 'LEFT':
                    self.angle += self.handling
                elif self.turn_status == 'RIGHT':
                    self.angle -= self.handling
                else:
                    pass
            else:
                pass
        else:
            self.image = pygame.transform.rotate(self.original_image, self.angle)

    def movement_calculation(self):
        self.direction = self.angle * 1.5
        self.direction *= 0.0174533
        self.dx = self.speed * math.sin(-self.direction)
        if self.drive_status == 'STATION':
            pass
        else:
            self.dy = self.speed * math.cos(self.direction)

    def movement(self):
        self.rect.x += self.dx
        self.rect.y -= self.dy

    def accelerate(self):
        if self.status == 'FORWARD':
            if self.speed < (self.speed_forward_max - self.speedup):
                self.speed += self.speedup
        elif self.status == 'BRAKE':
            if self.speed > -self.brake_power:
                self.speed += self.brake_power
            elif self.speed <= -self.brake_power:
                self.speed = 0
                self.status = 'STOP'
            elif self.speed == 0:
                self.status = 'STOP'
            else:
                self.speed < -self.brake_power
                self.status == 'STOP'
        elif self.status == 'BACKWARD':
            if self.speed > self.speed_backward_max:
                self.speed -= self.speedup
        elif self.status == 'NEUTRAL':
            if self.speed >= 1:
                self.speed -= self.friction
            elif self.speed < 1:
                self.speed = 0
                self.status = 'STOP'
            else:
                pass
        elif self.status == 'NEUTRAL_BACKWARD':
            if self.speed <= -1:
                self.speed += self.friction
        elif self.status == 'STOP':
            self.speed = 0
        else:
            pass

    def main(self):
        self.movement_calculation()
        self.movement()
        if user.autopilot == False:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                user.status = 'FORWARD'
                user.turn_status = 'NONE'
                if keys[pygame.K_LEFT]:
                    user.turn_status = 'LEFT'
                elif keys[pygame.K_RIGHT]:
                    user.turn_status = 'RIGHT'
                user.accelerate()
            elif keys[pygame.K_DOWN]:
                if user.speed > 1:
                    user.status = 'BRAKE'
                else:
                    user.status = 'BACKWARD'
                user.accelerate()
                if user.status == 'BRAKE':
                    if keys[pygame.K_LEFT]:
                        user.turn_status = 'LEFT'
                    elif keys[pygame.K_RIGHT]:
                        user.turn_status = 'RIGHT'
                elif user.status == 'BACKWARD':
                    if keys[pygame.K_LEFT]:
                        user.turn_status = 'RIGHT'
                    elif keys[pygame.K_RIGHT]:
                        user.turn_status = 'LEFT'
                else:
                    pass
            elif keys[pygame.K_RIGHT]:
                if user.status == 'BRAKE' or user.status == 'NEUTRAL':
                    user.turn_status = 'RIGHT'
                elif user.status == 'BACKWARD' or user.status == 'NEUTRAL_BACKWARD':
                    user.turn_status = 'LEFT'
                else:
                    pass
            elif keys[pygame.K_LEFT]:
                if user.status == 'BRAKE' or user.status == 'NEUTRAL':
                    user.turn_status = 'LEFT'
                elif user.status == 'BACKWARD' or user.status == 'NEUTRAL_BACKWARD':
                    user.turn_status = 'RIGHT'
                else:
                    pass
            elif user.speed >= 1:
                user.status = 'NEUTRAL'
                user.accelerate()
            elif user.speed <= -1:
                user.status = 'NEUTRAL_BACKWARD'
                user.accelerate()
            elif user.speed > -1 and user.speed < 1:
                user.status = 'STOP'
                user.speed = 0
                user.turn_status = 'NONE'
            else:
                pass
            user.turn()
        else:
            user.accelerate()
            user.turn()
            if user.status != 'STOP':
                if (user.rect.y - 100) <= 0:
                    user.status = 'BRAKE'

    def reset(self):
        self.angle = 0
        self.speed = 0
        self.dx = 0
        self.dy = 0
        self.rect = user.image.get_rect(center = (W // 2, H - 160))
        self.turn()
        button_Autopilot.status = 'NOT ACTIVE'
        self.autopilot = False
        button_Forward.status = 'NOT ACTIVE'
        button_Brake.status = 'NOT ACTIVE'
    def freeze(self):
        pass
class Button(pygame.sprite.Sprite):
    def __init__(self, text, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.status = 'NOT ACTIVE'
        self.rect = self.image.get_rect()
        self.txt = FONT.render(text, True, BLACK)
        self.txt_rect = self.txt.get_rect(center = self.rect.center)
        self.rect.topleft = x, y

    def is_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def colorize(self):
        if self.status == 'NOT ACTIVE':
            self.image.fill(GRAY)
        elif self.status == 'ACTIVE' or self.status == 'GREEN':
            self.image.fill(GREEN)
        elif self.status == 'RED':
            self.image.fill(RED)
        elif self.status == 'BLUE':
            self.image.fill(BLUE)
        self.image.blit(self.txt, self.txt_rect)
class StatMenu(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.status = 'NOT ACTIVE'
        self.rect = self.image.get_rect()
        self.text = ''
        self.txt = FONT.render(self.text, True, BLACK)
        self.txt_rect = self.txt.get_rect()
        self.rect.topleft = x, y

    def colorize(self):
        if self.status == 'NOT ACTIVE':
            self.image.fill(WHITE)
        elif self.status == 'ACTIVE':
            self.image.fill(GREEN)
        self.image.blit(self.txt, self.txt_rect)

    def update_text(self):
        self.text = 'Mode:' + str(user.drive_status) + ' Status:' + str(user.status) + ' Turn:' + str(user.turn_status) + ' Speed:' + str('%.1f' % user.speed)
        self.txt = FONT.render(self.text, True, BLACK)
class GameField(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        picture = pygame.image.load('CarB.png').convert_alpha()
        self.width = 30
        self.height = self.width * 2
        self.original_image = pygame.transform.scale(picture, (self.width, self.height))
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (W // 2, H - 160))

# инициализация элементов интерфейса и пользователя на поле
user = UserCar()
button_Mode = Button('Mode', 10, H - 340, 100, 40)
button_Mode.status = 'BLUE'
button_Autopilot = Button('Autopilot', 10, H - 300, 100, 40)
button_Forward = Button('Forward', 10, H - 250, 100, 40)
button_Brake = Button('Brake', 10, H - 210, 100, 40)
button_Reset = Button('Reset', 10, H - 80, 100, 40)
button_Left = Button('<', 10, H - 170, 50, 40)
button_Right = Button('>', 10 + 50, H - 170, 50, 40)
buttons_group = pygame.sprite.Group(button_Mode, button_Autopilot, button_Forward, button_Brake, button_Reset, button_Left, button_Right)
status = StatMenu(0, H - 20, W, 20)
status_group = pygame.sprite.Group(status)

def buttons_update():
    if user.status == 'STOP':
        button_Right.status = 'NOT ACTIVE'
        button_Left.status = 'NOT ACTIVE'
    for i in buttons_group:
        i.colorize()
    for i in status_group:
        i.colorize()
        i.update_text()
    buttons_group.draw(sc)
    status_group.draw(sc)
def events_tracker():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif button_Autopilot.is_pressed(event):
            if user.autopilot == False:
                user.autopilot = True
                button_Autopilot.status = 'ACTIVE'
            else:
                user.autopilot = False
                button_Autopilot.status = 'NOT ACTIVE'
                button_Brake.status = 'NOT ACTIVE'
                button_Forward.status = 'NOT ACTIVE'
        elif button_Forward.is_pressed(event):
            if user.autopilot == True:
                if user.status != 'FORWARD':
                    user.status = 'FORWARD'
                    button_Forward.status = 'ACTIVE'
                else:
                    user.status = 'NEUTRAL'
                    button_Forward.status = 'NOT ACTIVE'
        elif button_Brake.is_pressed(event):
            user.status = 'BRAKE'
            button_Forward.status = 'NOT ACTIVE'
        elif button_Reset.is_pressed(event):
            user.reset()
        elif button_Mode.is_pressed(event):
            user.reset()
            if user.drive_status == 'MOVE':
                user.drive_status = 'STATION'
                button_Mode.status = 'RED'
            elif user.drive_status == 'STATION':
                user.drive_status = 'MOVE'
                button_Mode.status = 'BLUE'
        elif button_Left.is_pressed(event):
            if button_Left.status == 'NOT ACTIVE':
                if user.autopilot == True and (user.status != 'STOP'):
                    user.turn_status = 'LEFT'
                    button_Right.status = 'NOT ACTIVE'
                    button_Left.status = 'ACTIVE'
                else:
                    pass
            else:
                button_Left.status = 'NOT ACTIVE'
                user.turn_status = 'NONE'
        elif button_Right.is_pressed(event):
            if button_Right.status == 'NOT ACTIVE':
                if user.autopilot == True and (user.status != 'STOP'):
                    user.turn_status = 'RIGHT'
                    button_Right.status = 'ACTIVE'
                    button_Left.status = 'NOT ACTIVE'
                else:
                    pass
            else:
                button_Right.status = 'NOT ACTIVE'
                user.turn_status = 'NONE'
        else:
            pass

sc.fill(LIGHT_GRAY)

while 1:
    # отслеживание действий пользователя
    events_tracker()
    sc.fill(LIGHT_GRAY)
    user.main()
    buttons_update()
    sc.blit(user.image, user.rect)

    pygame.display.update()
    clock.tick(FPS)
