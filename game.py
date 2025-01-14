import pygame
import os
import random

# Init and Create Window (win)
pygame.init()
win_height = 400
win_width = 800
win = pygame.display.set_mode((win_width, win_height))

# Load and Size Images
# Hero (Player)
'''left = [pygame.image.load(os.path.join("Assets/Hero", "L1.png")),
        pygame.image.load(os.path.join("Assets/Hero", "L2.png")),
        pygame.image.load(os.path.join("Assets/Hero", "L3.png")),
        pygame.image.load(os.path.join("Assets/Hero", "L4.png")),
        pygame.image.load(os.path.join("Assets/Hero", "L5.png")),
        pygame.image.load(os.path.join("Assets/Hero", "L6.png")),
        pygame.image.load(os.path.join("Assets/Hero", "L7.png")),
        pygame.image.load(os.path.join("Assets/Hero", "L8.png")),
        pygame.image.load(os.path.join("Assets/Hero", "L9.png"))
        ]
right =[pygame.image.load(os.path.join("Assets/Hero", "R1.png")),
        pygame.image.load(os.path.join("Assets/Hero", "R2.png")),
        pygame.image.load(os.path.join("Assets/Hero", "R3.png")),
        pygame.image.load(os.path.join("Assets/Hero", "R4.png")),
        pygame.image.load(os.path.join("Assets/Hero", "R5.png")),
        pygame.image.load(os.path.join("Assets/Hero", "R6.png")),
        pygame.image.load(os.path.join("Assets/Hero", "R7.png")),
        pygame.image.load(os.path.join("Assets/Hero", "R8.png")),
        pygame.image.load(os.path.join("Assets/Hero", "R9.png"))
        ]'''
left = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "gronda2.png")), (64, 64))

right = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "gronda1.png")), (64, 64))
# Enemy
''''left_enemy = [pygame.image.load(os.path.join("Assets/Enemy", "L1E.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "L2E.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "L3E.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "L4E.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "L5E.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "L6E.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "L7E.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "L8E.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "L9P.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "L10P.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "L11P.png"))
        ]'''
left_enemy = [pygame.image.load(os.path.join("Assets","cop0.png")),pygame.image.load(os.path.join("Assets","cop1.png")),pygame.image.load(os.path.join("Assets","cop2.png"))]
# Bullet
bullet_img = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Bullets", "light_bullet.png")), (25, 25))
# Background
bg = "Background1.png"
background = pygame.transform.scale(pygame.image.load(os.path.join("Assets/bg", bg)), (win_width, win_height))


# Music/Sounds
music = pygame.mixer.music.load(os.path.join("Assets/Audio", "cancion.MPEG"))
pop_sound = pygame.mixer.Sound(os.path.join("Assets/Audio", "pop.ogg"))
pygame.mixer.music.play(-1)

class Hero:
    def __init__(self, x, y):
        # Walk
        self.x = x
        self.y = y
        self.velx = 10
        self.vely = 6
        self.face_right = True
        self.face_left = False
        self.stepIndex = 0
        # Jump
        self.jump = False
        # Bullet
        self.bullets = []
        self.cool_down_count = 0
        # Health
        self.hitbox = (self.x, self.y, 64, 64)
        self.health = 30
        self.lives = 1
        self.alive = True

    def move_hero(self, userInput):
        if userInput[pygame.K_RIGHT] and self.x <= win_width - 62:
            self.x += self.velx
            self.face_right = True
            self.face_left = False
        elif userInput[pygame.K_LEFT] and self.x >= 30:
            self.x -= self.velx
            self.face_right = False
            self.face_left = True
        else:
            self.stepIndex = 0
        if userInput[pygame.K_UP] and self.y > 220:
            self.y -= self.vely
        elif userInput[pygame.K_DOWN] and self.y < 330:
            self.y += self.vely

    def draw(self, win):
        self.hitbox = (self.x + 15, self.y + 15, 30, 40)
        pygame.draw.rect(win, (255, 0, 0), (self.x + 15, self.y, 30, 10))
        if self.health >= 0:
            pygame.draw.rect(win, (0, 255, 0), (self.x + 15, self.y, self.health, 10))
        if self.stepIndex >= 9:
            self.stepIndex = 0
        if self.face_left:
            win.blit(left, (self.x, self.y))
            self.stepIndex += 1
        if self.face_right:
            win.blit(right, (self.x, self.y))
            self.stepIndex += 1

    def jump_motion(self, userInput):
        if userInput[pygame.K_SPACE] and self.jump is False:
            self.jump = True
        if self.jump:
            self.y -= self.vely * 4
            self.vely -= 1
        if self.vely < -6:
            self.jump = False
            self.vely = 6

    def direction(self):
        if self.face_right:
            return 1
        if self.face_left:
            return -1

    def cooldown(self):
        if self.cool_down_count >= 10:
            self.cool_down_count = 0
        elif self.cool_down_count > 0:
            self.cool_down_count += 1

    def shoot(self):
        self.hit()
        self.cooldown()
        if (userInput[pygame.K_f] and self.cool_down_count == 0):
            pop_sound.play()
            bullet = Bullet(self.x, self.y, self.direction())
            self.bullets.append(bullet)
            self.cool_down_count = 1
        for bullet in self.bullets:
            bullet.move()
            if bullet.off_screen():
                self.bullets.remove(bullet)

    def hit(self):
        for enemy in enemies:
            for bullet in self.bullets:
                if enemy.hitbox[0] < bullet.x < enemy.hitbox[0] + enemy.hitbox[2] and enemy.hitbox[1] < bullet.y < \
                        enemy.hitbox[1] + enemy.hitbox[3]:
                    enemy.health -= 5
                    player.bullets.remove(bullet)


class Bullet:
    def __init__(self, x, y, direction):
        self.x = x + 15
        self.y = y + 25
        self.direction = direction

    def draw_bullet(self):
        win.blit(bullet_img, (self.x, self.y))

    def move(self):
        if self.direction == 1:
            self.x += 15
        if self.direction == -1:
            self.x -= 15

    def off_screen(self):
        return not (self.x >= 0 and self.x <= win_width)


class Enemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.stepIndex = 0
        # Health
        self.hitbox = (self.x, self.y, 64, 64)
        self.health = 30

    def step(self):
        if self.stepIndex >= 3:
            self.stepIndex = 0

    def draw(self, win):
        self.hitbox = (self.x + 20, self.y + 10, 30, 45)
        pygame.draw.rect(win, (255, 0, 0), (self.x+16, self.y-12, 30, 10))
        if self.health >= 0:
            pygame.draw.rect(win, (0, 255, 0), (self.x+16, self.y-12, self.health, 10))
        self.step()
        win.blit(left_enemy[self.stepIndex], (self.x, self.y))
        self.stepIndex += 1

    def move(self):
        self.hit()
        self.x -= speed


    def hit(self):
        if player.hitbox[0] < enemy.x + 32 < player.hitbox[0] + player.hitbox[2] and player.hitbox[1] < enemy.y + 32 < \
                player.hitbox[1] + player.hitbox[3]:
            if player.health > 0:
                player.health -= 1
                if player.health == 0 and player.lives > 0:
                    player.lives -= 1
                    player.health = 30
                elif player.health == 0 and player.lives == 0:
                    player.alive = False

    def off_screen(self):
        return not (self.x >= -50 and self.x <= win_width + 50)


# Draw Game
def draw_game():
    global tower_health, speed
    win.fill((0, 0, 0))
    win.blit(background, (0, 0))
    # Draw Player
    player.draw(win)
    # Draw Bullets
    for bullet in player.bullets:
        bullet.draw_bullet()
    # Draw Enemies
    for enemy in enemies:
        enemy.draw(win)
    
   
    # Player Health
    if player.alive == False:
        win.fill((0, 0, 0))
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('You Died! Press R to restart', True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (win_width // 2, win_height // 2)
        win.blit(text, (200,100))
        if userInput[pygame.K_r]:
            player.alive = True
            player.lives = 1
            player.health = 30
            tower_health = 3
            speed = 2
            
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Salud: ' + str(player.lives) + ' | Salud Xulo: '+ str(tower_health) + ' |Kills: '+ str(kills), True, (255, 255, 255))
    win.blit(text, (200, 200))
    # Delay and Update
    #pygame.time.delay(30)
    pygame.display.update()



# Instance of Hero-Class
player = Hero(250, 290)

# Instance of Enemy-Class
enemies = []
speed = 2
kills = 0

# Tower
tower_health = 3

# Mainloop
run = True
while run:
    background = pygame.transform.scale(pygame.image.load(os.path.join("Assets/bg", bg)), (win_width, win_height))
    # Quit Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Input
    userInput = pygame.key.get_pressed()

    # Shoot
    player.shoot()

    # Movement
    player.move_hero(userInput)
    player.jump_motion(userInput)

    # Tower Health
    if tower_health == 0:
        player.alive = False

    # Enemy
    y_pos_enemy = random.randint(220,330)
    y_pos_enemy2 = random.randint(220,330)
    if len(enemies) == 0:
        enemy = Enemy(750, y_pos_enemy, speed)
        
        enemies.append(enemy)
        

        if kills % 3 == 0:
            enemy2 = Enemy(750, y_pos_enemy2, speed)
            enemies.append(enemy2)
        if speed <= 3:
            speed += 0.25
    

    
        




    for enemy in enemies:
        enemy.move()
        if enemy.off_screen() or enemy.health == 0:
            enemies.remove(enemy)
        if enemy.x < 50:
            enemies.remove(enemy)
            tower_health -= 1
        if enemy.health == 0:
            kills +=1



    # Draw Game in Window
    draw_game()
     # Draw Game in Window
    n = random.randint(1,4)
    if bg == "Background1.png" and n == 1:
        bg = "Background2.png"
    elif bg == "Background2.png" and n == 1:
        bg = "Background1.png"
