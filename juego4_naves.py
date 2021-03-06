import pygame, sys, random

WIDTH = 800
HEIGHT = 600

BLACK   = (   0,   0,   0)
WHITE   = ( 255, 255, 255)
GREEN   = (   0, 255,   0)
RED     = ( 255,   0,   0)
BLUE    = (   0,   0, 255)

#------------------------------------------------------------------------------------------------------------------------
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Shooter 1.0")
clock = pygame.time.Clock()

#------------------------------------------------------------------------------------------------------------------------
def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)
    
def  draw_shield_bar(surface, x, y, percentage):
    BAR_LENGHT = 180
    BAR_HEIGHT = 40
    fill = (percentage / 100) * BAR_LENGHT
    border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill)
    pygame.draw.rect(surface, WHITE, border, 2)
 
def pause():
    pausado = True

    while pausado:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    pausado = False

    

#------------------------------------------------------------------------------------------------------------------------    
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.speed_y = 0
        self.full_shield = 100
        self.shield = self.full_shield
        
    def update(self):
        self.speed_x = 0
        self.speed_y = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        if keystate[pygame.K_UP]:
            self.speed_y = -5
        if keystate[pygame.K_DOWN]:
            self.speed_y = 5

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.bottom < 120:
            self.rect.bottom = 120
 
            
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        laser_sound.play()
 
 #------------------------------------------------------------------------------------------------------------------------           
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)
        
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-140, -100)
            self.speedy = random.randrange(1, 10)
            

#------------------------------------------------------------------------------------------------------------------------
def create_meteor():
    meteor = Meteor()
    all_sprites.add(meteor)
    meteor_list.add(meteor)
    
#------------------------------------------------------------------------------------------------------------------------   
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("laser1.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
        
#------------------------------------------------------------------------------------------------------------------------
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50 # how long to wait for the next frame VELOCITY OF THE EXPLOSION

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill() # if we get to the end of the animation we don't keep going.
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
 
#------------------------------------------------------------------------------------------------------------------------               
def show_go_screen():
    screen.blit(background, [0,0])
    draw_text(screen, "SHOOTER 1.0", 65, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "Para mover la nave utilice las flechas de direcci??n del teclado", 27, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "Press key", 20, WIDTH // 2, HEIGHT * 3/4)
    pygame.display.flip()
    waiting = True
    while  waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

#------------------------------------------------------------------------------------------------------------------------
#creo meteoros de distintos tama??os
meteor_images = []
meteor_list = ["meteorGrey_big1.png", "meteorGrey_big2.png", "meteorGrey_big3.png", "meteorGrey_big4.png",
                "meteorGrey_med1.png", "meteorGrey_med2.png", "meteorGrey_small1.png", "meteorGrey_small2.png",
                "meteorGrey_tiny1.png", "meteorGrey_tiny2.png"]
for img in meteor_list:
    meteor_images.append(pygame.image.load(img).convert())
    
#crear animacion de explociones
explosion_anim = []
for i in range(9):
    file = "regularExplosion0{}.png".format(i)
    img = pygame.image.load(file).convert()
    img.set_colorkey(BLACK)
    img_scale = pygame.transform.scale(img, (70,70))
    explosion_anim.append(img_scale)
    
#cargar imagen de fondo
background = pygame.image.load("background.png").convert()

#cargar los sonidos
laser_sound = pygame.mixer.Sound("laser5.ogg")

explosion_sound = pygame.mixer.Sound("explosion.wav")
explosion_sound.set_volume(0.6)

pygame.mixer.music.load("music.ogg")
pygame.mixer.music.set_volume(0.2)


#hago que la musica de fondo quede en loop
pygame.mixer.music.play(loops=-1)

game_over = True
running = True
while running:

    if game_over:
        
        show_go_screen()
        
        game_over = False
        all_sprites = pygame.sprite.Group()
        meteor_list = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        
        player = Player()
        all_sprites.add(player)
        
        score = 0
        level = 1

        for i in range(8):
            create_meteor()
        
    clock.tick(60)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            pygame.quit()
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                draw_text(screen, "Juego en pausa, presione C para seguir jugando", 25, WIDTH/2, HEIGHT/2 - 50)
                pygame.display.update()
                pause()


    all_sprites.update()
    
    #colisiones meteoro en lase
    hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
    for hit in hits:
        score += 10

        if score == level * 1000:
            level += 1
            if player.shield != player.full_shield:
                if player.full_shield - player.shield < 25:
                    player.shield += player.full_shield - player.shield
            
                if player.full_shield - player.shield >= 25:
                    player.shield += 25

        explosion_sound.play()
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        create_meteor()
        
    
    # checar colisiones - jugador - meteoro
    hits = pygame.sprite.spritecollide(player, meteor_list,  True)
    for hit in hits:
        player.shield -= 5 * level
        create_meteor()
        if player.shield <= 0:
            game_over = True
        
    
    screen.blit(background, [0,0])
    
    all_sprites.draw(screen)
    
    #marcador
    sTexto = "Puntos: " + str(score) + " --- Nivel: " + str(level)
    draw_text(screen, sTexto, 25, WIDTH // 2, 10)
    
    #escudo
    draw_shield_bar(screen, 5, 5, player.shield)
    
    pygame.display.flip()
pygame.quit()