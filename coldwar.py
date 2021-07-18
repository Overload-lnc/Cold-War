import pygame
import random


def message(msg, screen, bg_color, msg_color, loc, font_size):  # bg = background
    '''
    writes a message on the whole screen
    you can only use it at either start or end
    it doesn't work in fill()-display() part
    '''
    message_font = pygame.font.SysFont("Arial", font_size)
    message_text = message_font.render(msg, False, msg_color)
    for i in range(3200):
        screen.fill(bg_color)
        screen.blit(message_text, loc)
        pygame.display.update()


def x_checker(start, end, current_x):
    return start <= current_x <= end


def y_checker(start, end, current_y):
    return start <= current_y <= end


class Clock:
    def __init__(self, tick_speed):
        self.speed = tick_speed
        self.clock = pygame.time.Clock()

    def tick(self):
        self.clock.tick(self.speed)

    def tickDifferent(self, new_speed):
        self.clock.tick(new_speed)


class Token:
    def __init__(self, x, y, width, length, trigger_x, trigger_y, spawn, resXmin, resXmax, resYmin, resYmax):
        self.x = x
        self.y = y
        self.trigger_x = trigger_x
        self.trigger_y = trigger_y
        self.width = width
        self.length = length
        self.spawn = spawn
        self.x_min = resXmin
        self.x_max = resXmax
        self.y_min = resYmin
        self.y_max = resYmax
        self.value = 0
        self.self_hitbox = RectHitbox(self.x, self.x + self.width, self.y, self.y + self.length)

    def IsTriggered(self):
        if self.self_hitbox.detect(self.trigger_x, self.trigger_y):
            self.spawn = False
            return True

    def ReValHitBox(self, mode, sx, ex, sy, ey):
        if mode == 0:
            self.self_hitbox.start_x = self.x
            self.self_hitbox.start_y = self.y
            self.self_hitbox.end_x = self.x + self.width
            self.self_hitbox.end_y = self.y + self.length
        elif mode == 1:
            self.self_hitbox.start_x = sx
            self.self_hitbox.start_y = sy
            self.self_hitbox.end_x = ex
            self.self_hitbox.end_y = ey
        elif mode == 2:
            self.self_hitbox.start_x = self.x + sx
            self.self_hitbox.start_y = self.y + sy
            self.self_hitbox.end_x = self.x + self.width + ex
            self.self_hitbox.end_y = self.y + self.length + ey

    def IsTriggeredCond(self, cond_list):
        if self.self_hitbox.detect(self.trigger_x, self.trigger_y) and all(cond_list):
            self.spawn = False
            return True

    def respawn(self):
        self.x = random.randint(self.x_min, self.x_max - self.width)
        self.y = random.randint(self.y_min, self.y_max - self.length)
        self.self_hitbox = RectHitbox(self.x, self.x + self.width, self.y, self.y + self.length)
        self.spawn = True

    def respawnNoCord(self):
        self.self_hitbox = RectHitbox(self.x, self.x + self.width, self.y, self.y + self.length)
        self.spawn = True

    def draw(self, window, color, thickness):
        if self.spawn is True:
            pygame.draw.rect(window, color, (self.x, self.y, self.width, self.length), thickness)

    def drawTexture(self, window, img):
        if self.spawn is True:
            window.blit(img, (self.x, self.y))

    def addRange(self, add_range):
        self.self_hitbox.start_x -= add_range
        self.self_hitbox.end_x += add_range
        self.self_hitbox.start_y -= add_range
        self.self_hitbox.end_y += add_range


class RectHitbox:
    def __init__(self, start_x, end_x, start_y, end_y):
        self.start_x = start_x
        self.end_x = end_x
        self.start_y = start_y
        self.end_y = end_y

    def draw(self, thickness, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.start_x, self.start_y,
                                                   (self.end_x - self.start_x),
                                                   (self.end_y - self.start_y)), thickness)

    def detect(self, target_x, target_y):
        return x_checker(self.start_x, self.end_x, target_x) and y_checker(self.start_y, self.end_y, target_y)


class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Character:
    def __init__(self, x, y, width, length, key_map, window):
        self.width = width
        self.length = length

        self.x = x
        self.y = y
        self.max_x = 1000000 - self.width
        self.min_x = 0
        self.max_y = 1000000 - self.length
        self.min_y = 0

        self.window = window
        self.death = False
        self.respawnX = x
        self.respawnY = y

        self.key_binds = {
            "w": pygame.K_w, "a": pygame.K_a, "s": pygame.K_s, "d": pygame.K_d, "e": pygame.K_e,
            "q": pygame.K_q, "f": pygame.K_f, "r": pygame.K_r, "z": pygame.K_z, "x": pygame.K_x,
            "c": pygame.K_c, "v": pygame.K_v, "t": pygame.K_t, "g": pygame.K_g, "b": pygame.K_b,
            "y": pygame.K_y, "h": pygame.K_h, "n": pygame.K_n, "u": pygame.K_u, "j": pygame.K_j,
            "m": pygame.K_m, "k": pygame.K_k, "o": pygame.K_o, "l": pygame.K_l, "p": pygame.K_p,
            "up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT
        }

        if key_map[0] != "":
            self.ver_pos = self.key_binds[key_map[0]]
        else:
            self.ver_pos = ""
        if key_map[1] != "":
            self.ver_neg = self.key_binds[key_map[1]]
        else:
            self.ver_neg = ""
        if key_map[2] != "":
            self.hor_pos = self.key_binds[key_map[2]]
        else:
            self.hor_pos = ""
        if key_map[3] != "":
            self.hor_neg = self.key_binds[key_map[3]]
        else:
            self.hor_neg = ""

    def hitbox(self, trigger_x, trigger_y):
        return RectHitbox(self.x, self.y, self.x + self.width, self.y + self.length).detect(trigger_x, trigger_y)

    def respawn(self):
        self.death = False
        self.x = self.respawnX
        self.y = self.respawnY

    def drawRect(self, color, thickness):
        pygame.draw.rect(self.window, color, (self.x, self.y, self.width, self.length), thickness)

    def drawCircle(self, color, width, radius):
        pygame.draw.circle(self.window, color, (self.x, self.y), radius, width)

    def drawTexture(self, img, look_death):
        if look_death is True:
            if self.death is False:
                self.window.blit(img, (self.x, self.y))
        else:
            self.window.blit(img, (self.x, self.y))

    def centerPoint(self):
        return self.x + self.width / 2, self.y + self.length / 2

    def centerX(self):
        return self.x + self.width / 2

    def centerY(self):
        return self.y + self.length / 2

    def clamp(self):
        if self.x < self.min_x:
            self.x = self.min_x
        elif self.x > self.max_x:
            self.x = self.max_x

        if self.y < self.min_y:
            self.y = self.min_y
        elif self.y > self.max_y:
            self.y = self.max_y

    def setXLimit(self, min, max):
        self.max_x = max - self.width
        self.min_x = min

    def setYLimit(self, min, max):
        self.max_y = max - self.length
        self.min_y = min


class Effect:
    def __init__(self, limit):
        self.limit = limit + 1
        self.counter = 0
        self.loc_set = False
        self.loc = 0
        self.active = False

    def drawTex(self, window, loc, img):
        if self.active is True:
            if self.loc_set is False:
                self.loc = loc
                self.loc_set = True
            if self.counter < self.limit:
                window.blit(img, self.loc)
                self.counter += 1
            else:
                self.reset()

    def reset(self):
        self.counter = 0
        self.loc_set = False
        self.active = False

    def setLoc(self, loc):
        self.loc = loc
        self.loc_set = True


pygame.init()
window = pygame.display.set_mode((800, 700))
pygame.display.set_caption("Cold War")
clock = Clock(90)
run = True

us_speed = 2
ru_speed = 2
us_missile_speed = 3
ru_missile_speed = 3

# player1
char_us = Character(100, 322, 52, 28, ["s", "w", "", ""], window)
char_us.setYLimit(0, 610)
cY1 = 0
us_ms_point = Point2D(char_us.x + char_us.width, char_us.y + char_us.length / 2)
us1_missile = Token(us_ms_point.x, us_ms_point.y, 28, 7, 0, 0, False, 0, 0, 0, 0)
us2_missile = Token(us_ms_point.x, us_ms_point.y, 28, 7, 0, 0, False, 0, 0, 0, 0)
us1_missile.value = 200
us2_missile.value = 200
us_score = 0

# player1 buildings
silo1 = Token(0, 20, 84, 98, 800, 700, True, 0, 0, 0, 0)
silo1.value = 700  # score for destroying
silo2 = Token(0, 218, 84, 98, 800, 700, True, 0, 0, 0, 0)
silo2.value = 700   # score for destroying
silo3 = Token(0, 418, 84, 98, 800, 700, True, 0, 0, 0, 0)
silo3.value = 700   # score for destroying
chem_us = Token(0, 128, 75, 75, 800, 700, True, 0, 0, 0, 0)
chem_us.value = 400
log_us = Token(0, 318, 75, 75, 800, 700, True, 0, 0, 0, 0)
log_us.value = 400


# player2
char_ru = Character(652, 322, 52, 28, ["down", "up", "", ""], window)
char_ru.setYLimit(0, 610)
cY2 = 0
ru_ms_point = Point2D(char_ru.x - 28, char_ru.y + char_ru.length / 2)
ru1_missile = Token(ru_ms_point.x, ru_ms_point.y, 28, 7, 0, 0, False, 0, 0, 0, 0)
ru2_missile = Token(ru_ms_point.x, ru_ms_point.y, 28, 7, 0, 0, False, 0, 0, 0, 0)
ru1_missile.value = 200
ru2_missile.value = 200
ru_score = 0

# player2 buildings
silo01 = Token(716, 20, 84, 98, 800, 700, True, 0, 0, 0, 0)
silo01.value = 700  # score for destroying
silo02 = Token(716, 218, 84, 98, 800, 700, True, 0, 0, 0, 0)
silo02.value = 700  # score for destroying
silo03 = Token(716, 418, 84, 98, 800, 700, True, 0, 0, 0, 0)
silo03.value = 700  # score for destroying
chem_ru = Token(725, 128, 75, 75, 800, 700, True, 0, 0, 0, 0)
chem_ru.value = 400
log_ru = Token(725, 318, 75, 75, 800, 700, True, 0, 0, 0, 0)
log_ru.value = 400

# us texture loads
char_us_tex = pygame.image.load("text\\us_missile.png")
us_missile_tex = pygame.image.load("text\\missile_right.png")
silo1_img = pygame.image.load("text\\us_siloA1.png")
silo2_img = pygame.image.load("text\\us_siloB1.png")
silo3_img = pygame.image.load("text\\us_siloC1.png")
chem_plant_us = pygame.image.load("text\\chem_plant_us.png")

# russian texture loads
char_ru_tex = pygame.image.load("text\\russian_missile.png")
ru_missile_tex = pygame.image.load("text\\missile_left.png")
silo01_img = pygame.image.load("text\\ru_siloA1.png")
silo02_img = pygame.image.load("text\\ru_siloB1.png")
silo03_img = pygame.image.load("text\\ru_siloC1.png")
chem_plant_ru = pygame.image.load("text\\chem_plant_ru.png")

# panel loads
ctrl_panel_us = pygame.image.load("text\\control_panel_us.png")
ctrl_panel_ru = pygame.image.load("text\\control_panel_ru.png")
us_bomb_ind = pygame.image.load("text\\bomb2.png")
ru_bomb_ind = pygame.image.load("text\\bomb2.png")
log_dep = pygame.image.load("text\\log_dep.png")

# wreck loads
exp = pygame.image.load("text\\explosion.png")
exp_silo = pygame.image.load("text\\silo_explosion.png")
exp_c_us = pygame.image.load("text\\chem_plant_us_x.png")
exp_c_ru = pygame.image.load("text\\chem_plant_ru_x.png")
exp_log_dep = pygame.image.load("text\\log_dep_x.png")

missile_exp1 = Effect(50)
missile_exp2 = Effect(50)

silo1_exp = Effect(100)
silo1_exp.active = True
silo2_exp = Effect(100)
silo2_exp.active = True
silo3_exp = Effect(100)
silo3_exp.active = True
silo01_exp = Effect(100)
silo01_exp.active = True
silo02_exp = Effect(100)
silo02_exp.active = True
silo03_exp = Effect(100)
silo03_exp.active = True

chem_us_exp = Effect(100)
chem_us_exp.active = True
chem_ru_exp = Effect(100)
chem_ru_exp.active = True
log_us_exp = Effect(100)
log_us_exp.active = True
log_ru_exp = Effect(100)
log_ru_exp.active = True

winner = ""

black = (0, 0, 0)

main_font = pygame.font.SysFont("Arial", 13)
stat_font = pygame.font.SysFont("Arial", 11)
message("Game by Overload Inc.", window, black, (255, 255, 255), (276, 300), 30)

while run:
    # reval zone, reval = reValue
    spawn_str = ["Offline", "Online"]
    spawn_color = [(255, 0, 0), (0, 255, 0)]
    # US Log render
    us_stat1 = stat_font.render(spawn_str[int(silo1.spawn)], False, spawn_color[int(silo1.spawn)])
    us_stat2 = stat_font.render(spawn_str[int(silo2.spawn)], False, spawn_color[int(silo2.spawn)])
    us_stat3 = stat_font.render(spawn_str[int(silo3.spawn)], False, spawn_color[int(silo3.spawn)])
    us_stat4 = stat_font.render(spawn_str[int(chem_us.spawn)], False, spawn_color[int(chem_us.spawn)])
    us_stat5 = stat_font.render(spawn_str[int(log_us.spawn)], False, spawn_color[int(log_us.spawn)])

    ru_stat1 = stat_font.render(spawn_str[int(silo01.spawn)], False, spawn_color[int(silo01.spawn)])
    ru_stat2 = stat_font.render(spawn_str[int(silo02.spawn)], False, spawn_color[int(silo02.spawn)])
    ru_stat3 = stat_font.render(spawn_str[int(silo03.spawn)], False, spawn_color[int(silo03.spawn)])
    ru_stat4 = stat_font.render(spawn_str[int(chem_ru.spawn)], False, spawn_color[int(chem_ru.spawn)])
    ru_stat5 = stat_font.render(spawn_str[int(log_ru.spawn)], False, spawn_color[int(log_ru.spawn)])

    us_score_text = main_font.render(f"{us_score}", False, black)
    ru_score_text = main_font.render(f"{ru_score}", False, black)

    us_ms_point = Point2D(char_us.x + char_us.width, char_us.y + char_us.length / 2)
    ru_ms_point = Point2D(char_ru.x - ru1_missile.width, char_ru.y + char_ru.length / 2)

    if not us1_missile.spawn:
        us1_missile.x, us1_missile.y = us_ms_point.x, us_ms_point.y
    if not us2_missile.spawn:
        us2_missile.x, us2_missile.y = us_ms_point.x, us_ms_point.y
    if not ru1_missile.spawn:
        ru1_missile.x, ru1_missile.y = ru_ms_point.x, ru_ms_point.y
    if not ru2_missile.spawn:
        ru2_missile.x, ru2_missile.y = ru_ms_point.x, ru_ms_point.y

    # event handler
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

            if event.key == char_us.ver_pos:
                cY1 = us_speed
            elif event.key == char_us.ver_neg:
                cY1 = us_speed * -1

            if event.key == char_ru.ver_pos:
                cY2 = ru_speed
            elif event.key == char_ru.ver_neg:
                cY2 = ru_speed * -1

            if event.key == pygame.K_d:
                if us1_missile.spawn is True:
                    us2_missile.respawnNoCord()
                else:
                    us1_missile.respawnNoCord()

            if event.key == pygame.K_KP0:
                if ru1_missile.spawn is True:
                    ru2_missile.respawnNoCord()
                else:
                    ru1_missile.respawnNoCord()

        if event.type == pygame.KEYUP:
            if event.key == char_us.ver_pos or event.key == char_us.ver_neg:
                cY1 = 0

            if event.key == char_ru.ver_pos or event.key == char_ru.ver_neg:
                cY2 = 0

    char_us.y += cY1
    char_us.clamp()
    char_ru.y += cY2
    char_ru.clamp()

    # Graphics Start
    window.fill(black)

    if silo1.spawn is False and silo2.spawn is False and silo3.spawn is False:
        run = False
        winner = "russia"
        clock.tickDifferent(1)
    if silo01.spawn is False and silo02.spawn is False and silo03.spawn is False:
        run = False
        winner = "usa"
        clock.tickDifferent(1)

    window.blit(ctrl_panel_us, (0, 610))
    window.blit(ctrl_panel_ru, (410, 610))

    silo1.drawTexture(window, silo1_img)
    silo2.drawTexture(window, silo2_img)
    silo3.drawTexture(window, silo3_img)
    chem_us.drawTexture(window, chem_plant_us)

    silo01.drawTexture(window, silo01_img)
    silo02.drawTexture(window, silo02_img)
    silo03.drawTexture(window, silo03_img)
    chem_ru.drawTexture(window, chem_plant_ru)

    log_us.drawTexture(window, log_dep)
    log_ru.drawTexture(window, log_dep)

    # silo impact detect
    # us
    if (ru1_missile.spawn is True or ru2_missile.spawn is True) and silo1.spawn is True:
        silo1.trigger_x = ru1_missile.x
        silo1.trigger_y = ru1_missile.y + ru1_missile.length / 2
        if silo1.IsTriggered():
            silo1.spawn = False
            ru1_missile.spawn = False
            ru_score += silo1.value
        else:
            silo1.trigger_x = ru2_missile.x
            silo1.trigger_y = ru2_missile.y + ru1_missile.length / 2
            if silo1.IsTriggered():
                silo1.spawn = False
                ru2_missile.spawn = False
                ru_score += silo1.value

    if (ru1_missile.spawn is True or ru2_missile.spawn is True) and silo2.spawn is True:
        silo2.trigger_x = ru1_missile.x
        silo2.trigger_y = ru1_missile.y + ru1_missile.length / 2
        if silo2.IsTriggered():
            silo2.spawn = False
            ru1_missile.spawn = False
            ru_score += silo2.value
        else:
            silo2.trigger_x = ru2_missile.x
            silo2.trigger_y = ru2_missile.y + ru1_missile.length / 2
            if silo2.IsTriggered():
                silo2.spawn = False
                ru2_missile.spawn = False
                ru_score += silo2.value

    if (ru1_missile.spawn is True or ru2_missile.spawn is True) and silo3.spawn is True:
        silo3.trigger_x = ru1_missile.x
        silo3.trigger_y = ru1_missile.y + ru1_missile.length / 2
        if silo3.IsTriggered():
            silo3.spawn = False
            ru1_missile.spawn = False
            ru_score += silo3.value
        else:
            silo3.trigger_x = ru2_missile.x
            silo3.trigger_y = ru2_missile.y + ru1_missile.length / 2
            if silo3.IsTriggered():
                silo3.spawn = False
                ru2_missile.spawn = False
                ru_score += silo3.value

    if (ru1_missile.spawn is True or ru2_missile.spawn is True) and chem_us.spawn is True:
        chem_us.trigger_x = ru1_missile.x
        chem_us.trigger_y = ru1_missile.y + ru1_missile.length / 2
        if chem_us.IsTriggered():
            chem_us.spawn = False
            ru1_missile.spawn = False
            us_missile_speed = 2
            ru_score += chem_us.value
        else:
            chem_us.trigger_x = ru2_missile.x
            chem_us.trigger_y = ru2_missile.y + ru1_missile.length / 2
            if chem_us.IsTriggered():
                chem_us.spawn = False
                ru2_missile.spawn = False
                us_missile_speed = 2
                ru_score += chem_us.value

    if (ru1_missile.spawn is True or ru2_missile.spawn is True) and log_us.spawn is True:
        log_us.trigger_x = ru1_missile.x
        log_us.trigger_y = ru1_missile.y + ru1_missile.length / 2
        if log_us.IsTriggered():
            log_us.spawn = False
            ru1_missile.spawn = False
            us_speed = 1.5
            ru_score += log_us.value
        else:
            log_us.trigger_x = ru2_missile.x
            log_us.trigger_y = ru2_missile.y + ru1_missile.length / 2
            if log_us.IsTriggered():
                log_us.spawn = False
                ru2_missile.spawn = False
                us_speed = 1.5
                ru_score += log_us.value
    # ru
    if (us1_missile.spawn is True or us2_missile.spawn is True) and silo01.spawn is True:
        silo01.trigger_x = us1_missile.x
        silo01.trigger_y = us1_missile.y + us1_missile.length / 2
        if silo01.IsTriggered():
            silo01.spawn = False
            us1_missile.spawn = False
            us_score += silo01.value
        else:
            silo01.trigger_x = us2_missile.x
            silo01.trigger_y = us2_missile.y + us1_missile.length / 2
            if silo01.IsTriggered():
                silo01.spawn = False
                us2_missile.spawn = False
                us_score += silo01.value

    if (us1_missile.spawn is True or us2_missile.spawn is True) and silo02.spawn is True:
        silo02.trigger_x = us1_missile.x
        silo02.trigger_y = us1_missile.y + us1_missile.length / 2
        if silo02.IsTriggered():
            silo02.spawn = False
            us1_missile.spawn = False
            us_score += silo02.value
        else:
            silo02.trigger_x = us2_missile.x
            silo02.trigger_y = us2_missile.y + ru1_missile.length / 2
            if silo02.IsTriggered():
                silo02.spawn = False
                us2_missile.spawn = False
                us_score += silo02.value

    if (us1_missile.spawn is True or us2_missile.spawn is True) and silo03.spawn is True:
        silo03.trigger_x = us1_missile.x
        silo03.trigger_y = us1_missile.y + us1_missile.length / 2
        if silo03.IsTriggered():
            silo03.spawn = False
            us1_missile.spawn = False
            us_score += silo03.value
        else:
            silo03.trigger_x = us2_missile.x
            silo03.trigger_y = us2_missile.y + us1_missile.length / 2
            if silo03.IsTriggered():
                silo03.spawn = False
                us2_missile.spawn = False
                us_score += silo03.value

    if (us1_missile.spawn is True or us2_missile.spawn is True) and chem_ru.spawn is True:
        chem_ru.trigger_x = us1_missile.x
        chem_ru.trigger_y = us1_missile.y + us1_missile.length / 2
        if chem_ru.IsTriggered():
            chem_ru.spawn = False
            us1_missile.spawn = False
            ru_missile_speed = 2
            us_score += chem_ru.value
        else:
            chem_ru.trigger_x = us2_missile.x
            chem_ru.trigger_y = us2_missile.y + us1_missile.length / 2
            if chem_ru.IsTriggered():
                chem_ru.spawn = False
                us2_missile.spawn = False
                ru_missile_speed = 2
                us_score += chem_ru.value

    if (us1_missile.spawn is True or us2_missile.spawn is True) and log_ru.spawn is True:
        log_ru.trigger_x = us1_missile.x
        log_ru.trigger_y = us1_missile.y + us1_missile.length / 2
        if log_ru.IsTriggered():
            log_ru.spawn = False
            us1_missile.spawn = False
            ru_speed = 1.5
            us_score += log_ru.value
        else:
            log_ru.trigger_x = us2_missile.x
            log_ru.trigger_y = us2_missile.y + us1_missile.length / 2
            if log_ru.IsTriggered():
                log_ru.spawn = False
                us2_missile.spawn = False
                ru_speed = 1.5
                us_score += log_ru.value

    char_us.drawTexture(char_us_tex, False)
    char_ru.drawTexture(char_ru_tex, False)
    us1_missile.ReValHitBox(2, 0, 0, -7, 7)
    us2_missile.ReValHitBox(2, 0, 0, -7, 7)
    ru1_missile.ReValHitBox(2, 0, 0, -7, 7)
    ru2_missile.ReValHitBox(2, 0, 0, -7, 7)
    log_ru.ReValHitBox(2, 0, 0, -5, 5)
    log_us.ReValHitBox(2, 0, 0, -5, 5)
    chem_us.ReValHitBox(2, 0, 0, -5, 5)
    chem_ru.ReValHitBox(2, 0, 0, -5, 5)

    # missile us
    if us1_missile.spawn is True:
        us1_missile.drawTexture(window, us_missile_tex)
        us1_missile.x += us_missile_speed

        # despawn events
        if us1_missile.x > 828:
            us1_missile.spawn = False
        # missile collision
        us1_missile.trigger_x = ru1_missile.x
        us1_missile.trigger_y = ru1_missile.y + ru1_missile.length / 2
        if ru1_missile.spawn is True and us1_missile.IsTriggered():
            us1_missile.spawn = False
            ru1_missile.spawn = False
            missile_exp1.active = True
            window.blit(exp, (us1_missile.x, us1_missile.y))
            ru_score += us1_missile.value
            us_score += ru1_missile.value
        else:
            us1_missile.trigger_x = ru2_missile.x
            us1_missile.trigger_y = ru2_missile.y + ru2_missile.length / 2
            if ru2_missile.spawn is True and us1_missile.IsTriggered():
                us1_missile.spawn = False
                ru2_missile.spawn = False
                missile_exp1.active = True
                window.blit(exp, (us1_missile.x, us1_missile.y))
                ru_score += us1_missile.value
                us_score += ru1_missile.value
    if us2_missile.spawn is True:
        us2_missile.drawTexture(window, us_missile_tex)
        us2_missile.x += us_missile_speed

        # despawn events
        if us2_missile.x > 828:
            us2_missile.spawn = False
        # missile collision
        us2_missile.trigger_x = ru1_missile.x
        us2_missile.trigger_y = ru1_missile.y + ru1_missile.length / 2
        if ru1_missile.spawn is True and us2_missile.IsTriggered():
            us2_missile.spawn = False
            ru1_missile.spawn = False
            missile_exp2.active = True
            window.blit(exp, (us2_missile.x, us2_missile.y))
            ru_score += us1_missile.value
            us_score += ru1_missile.value
        else:
            us2_missile.trigger_x = ru2_missile.x
            us2_missile.trigger_y = ru2_missile.y + ru2_missile.length / 2
            if ru2_missile.spawn is True and us2_missile.IsTriggered():
                ru2_missile.spawn = False
                us2_missile.spawn = False
                missile_exp2.active = True
                window.blit(exp, (us2_missile.x, us2_missile.y))
                ru_score += us1_missile.value
                us_score += ru1_missile.value

    # missile ru
    if ru1_missile.spawn is True:
        ru1_missile.drawTexture(window, ru_missile_tex)
        ru1_missile.x -= ru_missile_speed

        # despawn events
        if ru1_missile.x < -28:
            ru1_missile.spawn = False
        # missile collision
        ru1_missile.trigger_x = us1_missile.x
        ru1_missile.trigger_y = us1_missile.y + us1_missile.length / 2
        if us1_missile.spawn is True and ru1_missile.IsTriggered():
            ru1_missile.spawn = False
            us1_missile.spawn = False
            window.blit(exp, (ru1_missile.x, ru1_missile.y))
            ru_score += us1_missile.value
            us_score += ru1_missile.value
        else:
            ru1_missile.trigger_x = us2_missile.x
            ru1_missile.trigger_y = us2_missile.y + us2_missile.length / 2
            if us2_missile.spawn is True and ru1_missile.IsTriggered():
                us2_missile.spawn = False
                ru1_missile.spawn = False
                window.blit(exp, (ru1_missile.x, ru1_missile.y))
                ru_score += us1_missile.value
                us_score += ru1_missile.value
    if ru2_missile.spawn is True:
        ru2_missile.drawTexture(window, ru_missile_tex)
        ru2_missile.x -= ru_missile_speed

        # despawn events
        # miss
        if ru2_missile.x < -28:
            ru2_missile.spawn = False
        # missile collision
        ru2_missile.trigger_x = us1_missile.x
        ru2_missile.trigger_y = us1_missile.y + us1_missile.length / 2
        if us1_missile.spawn is True and ru2_missile.IsTriggered():
            us1_missile.spawn = False
            ru2_missile.spawn = False
            window.blit(exp, (ru2_missile.x, ru2_missile.y))
            ru_score += us1_missile.value
            us_score += ru1_missile.value
        else:
            ru2_missile.trigger_x = us2_missile.x
            ru2_missile.trigger_y = us2_missile.y + us2_missile.length / 2
            if us2_missile.spawn is True and ru2_missile.IsTriggered():
                us2_missile.spawn = False
                ru2_missile.spawn = False
                window.blit(exp, (ru2_missile.x, ru2_missile.y))
                ru_score += us1_missile.value
                us_score += ru1_missile.value

    if us1_missile.spawn is False and us2_missile.spawn is False:
        us_bomb_ind = pygame.image.load("text\\bomb2.png")
    elif us1_missile.spawn is False or us2_missile.spawn is False:
        us_bomb_ind = pygame.image.load("text\\bomb1.png")
    else:
        us_bomb_ind = pygame.image.load("text\\bomb0.png")

    if ru1_missile.spawn is False and ru2_missile.spawn is False:
        ru_bomb_ind = pygame.image.load("text\\bomb2.png")
    elif ru1_missile.spawn is False or ru2_missile.spawn is False:
        ru_bomb_ind = pygame.image.load("text\\bomb1.png")
    else:
        ru_bomb_ind = pygame.image.load("text\\bomb0.png")

    window.blit(us_bomb_ind, (165, 638))
    window.blit(ru_bomb_ind, (575, 638))

    window.blit(us_score_text, (330, 659))
    window.blit(ru_score_text, (740, 659))

    window.blit(us_stat1, (280, 632))
    window.blit(us_stat2, (280, 645))
    window.blit(us_stat3, (280, 658))
    window.blit(us_stat4, (280, 671))
    window.blit(us_stat5, (280, 684))

    window.blit(ru_stat1, (690, 632))
    window.blit(ru_stat2, (690, 645))
    window.blit(ru_stat3, (690, 658))
    window.blit(ru_stat4, (690, 671))
    window.blit(ru_stat5, (690, 684))

    # us effects
    if missile_exp1.active is True:
        missile_exp1.drawTex(window, (us1_missile.x, us1_missile.y), exp)
    if missile_exp2.active is True:
        missile_exp2.drawTex(window, (us2_missile.x, us2_missile.y), exp)

    if silo1.spawn is False:
        silo1_exp.drawTex(window, (silo1.x, silo1.y), exp_silo)
    if silo2.spawn is False:
        silo2_exp.drawTex(window, (silo2.x, silo2.y), exp_silo)
    if silo3.spawn is False:
        silo3_exp.drawTex(window, (silo3.x, silo3.y), exp_silo)
    if chem_us.spawn is False:
        chem_us_exp.drawTex(window, (chem_us.x, chem_us.y), exp_c_us)
    if log_us.spawn is False:
        log_us_exp.drawTex(window, (log_us.x, log_us.y), exp_log_dep)

    # ru effects
    if silo01.spawn is False:
        silo01_exp.drawTex(window, (silo01.x, silo01.y), exp_silo)
    if silo02.spawn is False:
        silo02_exp.drawTex(window, (silo02.x, silo02.y), exp_silo)
    if silo03.spawn is False:
        silo03_exp.drawTex(window, (silo03.x, silo03.y), exp_silo)
    if chem_ru.spawn is False:
        chem_ru_exp.drawTex(window, (chem_ru.x, chem_ru.y), exp_c_ru)
    if log_ru.spawn is False:
        log_ru_exp.drawTex(window, (log_ru.x, log_ru.y), exp_log_dep)
    # effects end

    pygame.display.update()
    # Graphics End
    clock.tick()

if winner == "russia":
    message("Russia Wins!", window, black, (0, 255, 0), (280, 290), 50)
elif winner == "usa":
    message("U.S.A. Wins!", window, black, (0, 255, 0), (300, 290), 50)

pygame.quit()
