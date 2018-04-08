import pygame as pg
import random
from tools import *
from math import ceil
from pygame.locals import *
WIDHT = 1280
HEIGHT = 720
FPS = 60
class Player(pg.sprite.Sprite):
    def __init__(self,x):
        pg.sprite.Sprite.__init__(self)
        self.sheet = pg.image.load("gfx\sheet.png")
        self.image = get_image_2(self.sheet,3,491,19,503)
        self.image = pg.transform.scale(self.image,(50,40))


        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.vely = 0
        self.max_vely = 8
        self.gravity = 0.6
        self.rotate_angle = 0
        self.sprite_sheet_setup()
        

    def sprite_sheet_setup(self):
        self.sheet_idle =[]
        self.frame_1 = get_image_2(self.sheet,3,491,19,503)
        self.frame_1 = pg.transform.scale(self.frame_1,(50,40))

        self.sheet_idle.append(self.frame_1)

        self.frame_2 = get_image_2(self.sheet,31,491,47,503)
        self.frame_2 = pg.transform.scale(self.frame_2,(50,40))
        self.sheet_idle.append(self.frame_2)

        self.frame_3 = get_image_2(self.sheet,59,491,75,503)
        self.frame_3 = pg.transform.scale(self.frame_3,(50,40))
        self.sheet_idle.append(self.frame_3)

    def update(self):

        self.vely+=self.gravity
        self.rect.y+=self.vely
        if self.vely >self.max_vely:
            self.vely = self.max_vely
        self.jump()
        
    def jump(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.vely = -8

class Pipe_up(pg.sprite.Sprite):
    def __init__(self,x,color):
        pg.sprite.Sprite.__init__(self)
        self.sheet = pg.image.load("gfx\sheet.png")
        self.image = get_image_2(self.sheet,56,323,82,483)
        
        self.image = pg.transform.scale(self.image,(80,400))
        """
        self.image = pg.Surface((80,400))
        self.image.fill(color)
        self.image = self.image.convert()"""
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.velx= 3
        self.rect.bottom = random.randint(25,350)

    def update(self):
        self.rect.x-=self.velx
    
        
class Pipe_down(pg.sprite.Sprite):
    def __init__(self,x,other_pipe_bottom):
        pg.sprite.Sprite.__init__(self)
        self.sheet = pg.image.load("gfx\sheet.png")
        self.image = get_image_2(self.sheet,84,323,110,482)
        
        self.image = pg.transform.scale(self.image,(80,400))
        """
        self.image = pg.Surface((80,600))
        self.image.fill((0,255,0))
        self.image = self.image.convert()"""
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.top = other_pipe_bottom + 145

    def update(self):
        pass

class Ground(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.sheet = pg.image.load("gfx\sheet.png")
        self.image = get_image_2(self.sheet,292,0,459,55)
        self.image = pg.transform.scale(self.image,(400,80))
        self.rect =self.image.get_rect()
        self.rect.bottom = 600
    def update(self):
        pass
class Button(pg.sprite.Sprite):
    def __init__(self,x,y,image = pg.Surface((2,2))):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect=self.image.get_rect()  
        self.rect.center = (x,y)    


class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.init()
        
        self.screen = pg.display.set_mode((400, 600))
        pg.display.set_caption("lmao")
        self.sheet = pg.image.load("gfx\sheet.png")
        self.background = get_background(self.sheet,0,0,143,255,400,600)
        self.background = self.background.convert()
        self.clock = pg.time.Clock()
        self.running = True
        
        self.state = "MENU"
        
        self.pos_mouse = pg.mouse.get_pos()
        self.mouse_hitbox = Button(self.pos_mouse[0],self.pos_mouse[1])

        self.load_sounds()
    def load_sounds(self):
        self.die_sound =pg.mixer.Sound("sfx\sfx_die.wav")
        self.hit_sound = pg.mixer.Sound("sfx\sfx_hit.wav")
        self.point_sound = pg.mixer.Sound("sfx\sfx_point.wav")
        self.swooshing_sound = pg.mixer.Sound("sfx\sfx_swooshing.wav")
        self.wing_sound = pg.mixer.Sound("sfx\sfx_wing")        

    def new(self):
        
        
        self.all_sprites = pg.sprite.Group()
        self.ground_group = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.level()
        self.menu()
        self.game_over()
        self.run()

    
    def level(self):
        self.cambio = False
        self.contador_setup()
        self.top_pipe_1 = Pipe_up(400,(255,0,0))
        self.top_pipe_2 = Pipe_up(650,(255,255,0))
        self.control_pipe = Pipe_up(400,(255,0,255))
        self.bottom_pipe_1 =Pipe_down(400,self.top_pipe_1.rect.bottom)
        self.bottom_pipe_2 =Pipe_down(800,self.top_pipe_2.rect.bottom)
        self.player = Player(200)
        self.ground = Ground()
        self.player_things = pg.sprite.Group()
        self.platforms.add(self.top_pipe_2,self.top_pipe_1,self.bottom_pipe_2,self.bottom_pipe_1,self.ground)
        self.all_sprites.add(self.top_pipe_2,self.top_pipe_1,self.bottom_pipe_2,self.bottom_pipe_1,self.player)
        self.ground_group.add(self.ground)
        self.frame = 0
    def contador_setup(self):
        self.contador = 0
        self.char_0 = get_image_2(self.sheet,496,60,507,77)
        self.char_1 = get_image_2(self.sheet,136,455,143,472)
        self.char_2 = get_image_2(self.sheet,292,160,303,177)
        self.char_3 = get_image_2(self.sheet,306,160,317,177)
        self.char_4 = get_image_2(self.sheet,320,160,331,177)
        self.char_5 = get_image_2(self.sheet,334,160,345,177)
        self.char_6 = get_image_2(self.sheet,292,184,303,201)
        self.char_7 = get_image_2(self.sheet,306,184,317,201)
        self.char_8 = get_image_2(self.sheet,320,184,331,201)
        self.char_9 = get_image_2(self.sheet,334,184,345,201)
        self.char_group = []
        self.char_group.append(self.char_0)
        self.char_group.append(self.char_1)
        self.char_group.append(self.char_2)
        self.char_group.append(self.char_3)
        self.char_group.append(self.char_4)
        self.char_group.append(self.char_5)
        self.char_group.append(self.char_6)
        self.char_group.append(self.char_7)
        self.char_group.append(self.char_8)
        self.char_group.append(self.char_9)
        self.add = True
        self.puntaje_logo_unidad = Button(200,100,self.char_group[self.contador])
        self.puntaje_group = pg.sprite.Group()

        self.puntaje_group.add(self.puntaje_logo_unidad)


    def contador_update(self):
        self.unidad= self.contador%10
        self.decimal = self.contador/10

        if self.contador >= 10 and (self.add):
            self.puntaje_logo_decimal = Button(200,100,self.char_group[self.decimal])
            self.puntaje_logo_unidad.rect.x += 5
            self.puntaje_logo_decimal.rect.right = self.puntaje_logo_unidad.rect.left -5
            self.puntaje_group.add(self.puntaje_logo_decimal)
            self.add = False
        self.puntaje_logo_unidad.image = self.char_group[self.unidad]
        if self.contador >=10:
            self.puntaje_logo_decimal.image =self.char_group[self.decimal]
        
    def run(self):

        self.playing = True
        while self.playing:
            self.clock.tick(FPS) 
            
            self.events()
            self.update()
            self.draw()
  
    def collisions(self):
        hits = pg.sprite.spritecollideany(self.player,self.platforms)
        if hits:

            self.hit_sound.play()
            
            self.state = "GAME OVER"
    def animation_player(self):    
        self.frame,self.player.image,self.player.rotate_angle = animation(self.frame,self.player.sheet_idle,1,0,self.player.vely,self.player.rotate_angle)
    def score_anda_pipe_control(self):
        self.collisions()
        if self.top_pipe_1.rect.centerx < self.player.rect.centerx < self.top_pipe_1.rect.centerx + 4:
            self.contador+=1
            self.point_sound.play()
        if self.top_pipe_2.rect.centerx < self.player.rect.centerx < self.top_pipe_2.rect.centerx + 4:
            self.contador+=1
            self.point_sound.play()
            

        
        
        if self.top_pipe_1.rect.right <= 0:
            self.top_pipe_1.rect.x = 400
            self.top_pipe_1.rect.bottom = random.randint(25,350)
            self.bottom_pipe_1.rect.top = self.top_pipe_1.rect.bottom + 145
            
        if self.top_pipe_2.rect.right <= 0:
            self.top_pipe_2.rect.x = 400
            self.top_pipe_2.rect.bottom = random.randint(25,350)
            self.bottom_pipe_2.rect.top = self.top_pipe_2.rect.bottom + 145
            
        self.bottom_pipe_2.rect.x = self.top_pipe_2.rect.x
        self.bottom_pipe_1.rect.x = self.top_pipe_1.rect.x
    def update(self):
        
        self.click =pg.mouse.get_pressed()[0]

        if self.state == "MENU":
            self.pos_mouse = pg.mouse.get_pos()
            self.mouse_hitbox.rect.center = self.pos_mouse
            
            if pg.sprite.collide_rect(self.mouse_hitbox,self.button_play) and self.click:

                self.state = "LEVEL"
        elif self.state == "LEVEL":
            self.score_anda_pipe_control()
            self.animation_player()
            self.contador_update()
            self.all_sprites.update()
            
        elif self.state == "GAME OVER":
            for sprite in self.all_sprites:
                sprite.kill()

            self.mouse_hitbox.rect.center = self.pos_mouse
            if pg.sprite.collide_rect(self.mouse_hitbox,self.button_play) and pg.mouse.get_pressed()[0]:
                self.level()
                self.state = "LEVEL"
    

    def menu(self):
        self.play_logo = get_image_2(self.sheet,354,118,406,147)
        
        self.logo = get_image_2(self.sheet,351,91,440,114)
        
        
        
        self.button_play = Button(200,400,self.play_logo)
        self.button_logo = Button(200,200,self.logo)

        self.menu_sprites = pg.sprite.Group()
        self.menu_sprites.add(self.button_logo,self.button_play)

    def game_over(self):
        self.game_over_logo = get_image_2(self.sheet,395,59,491,80)
        self.button_game_over_logo = Button(200,300,self.game_over_logo)

        self.game_over_sprites = pg.sprite.Group()
        self.game_over_sprites.add(self.button_game_over_logo,self.button_play)

    def events(self):

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.swooshing_sound.play()


            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False      

    def draw(self):
        self.screen.blit(self.background,(0,0))
        
        if self.state == "MENU":
            self.menu_sprites.draw(self.screen)
        elif self.state == "LEVEL":
            self.all_sprites.draw(self.screen)
            self.puntaje_group.draw(self.screen)
        elif self.state == "GAME OVER":
            self.game_over_sprites.draw(self.screen)
            self.puntaje_group.draw(self.screen)
        self.ground_group.draw(self.screen)
        pg.display.flip()

g = Game()

while g.running:
    
    g.new()

pg.quit()