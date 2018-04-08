import pygame as pg

def animation(c,group,velocidad,frame_iteracion,vel ,rotate_angle):
    c+=0.1666666667
    rotate = rotate_angle
    max_rotate = 25
    min_rotate = 90
    vel_rotate = 3.5
    k = c // velocidad
    k = int(k)

    if len(group) == 1:
        k = 0
    else:
        if k == len(group):
            c = frame_iteracion*velocidad
            k = frame_iteracion

    image = group[k]
    if vel<=4.8:
        rotate = max_rotate
        image = pg.transform.rotate(image,rotate)
    elif vel<=8:

        if abs(rotate) <=90:
            
            
            rotate-=vel_rotate
            if rotate < -90:
                rotate = -90
            image = pg.transform.rotate(image,rotate)
    

    


    return c,image,rotate


def load_sheet(sheet,reverse,x,weight,height,n_sprites): 
	"""archivo,reverso,inicio = 0,ancho=50,alto"""
	image = sheet

	
	sprite_list = []
	for a in range(0,n_sprites):
		x -= weight
		ground = pg.Surface((50,height))
		ground.blit(image,(x,-5))
		
		ground = pg.transform.scale2x(ground)
		if reverse:
			ground= pg.transform.flip(ground,True,False)

        if ground.get_alpha():
            ground = ground.convert_alpha()

        else:

            ground = ground.convert()
            ground.set_colorkey((0,0,0))


		
        sprite_list.append(ground)
	return sprite_list

def get_image(sheet, x, y, xf, yf,posx=0,posy=0,reverse = False):
        """Extracts image from sprite sheet"""
        colorkey = sheet.get_at((0,0))
        width = xf - x
        height = yf - y
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(sheet, (0, 0), (x, y, width, height))
        
        image = pg.transform.scale2x(image)
        
        if image.get_alpha():
            image = image.convert_alpha()
        else:
            image = image.convert()
            image.set_colorkey(colorkey)
        if reverse:
        	image = pg.transform.flip(image,True,False)

        image_2 = pg.Surface([270,160])
        image_2.blit(image,(posx,posy))
        if image_2.get_alpha():
            image_2 = image_2.convert_alpha()
        else:
            image_2 = image_2.convert()
            image_2.set_colorkey((0,0,0))
        

        return image_2

def get_image_2(sheet, x, y, xf, yf,reverse = False):
        """Extracts image from sprite sheet"""
        colorkey = sheet.get_at((0,0))
        
        width = xf - x
        height = yf - y
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(sheet, (0, 0), (x, y, width, height))
        
        image = pg.transform.scale2x(image)
        if reverse:
        	image = pg.transform.flip(image,True,False)
        if image.get_alpha():
            image = image.convert_alpha()
        else:
            image = image.convert()
            image.set_colorkey((0,0,0))
        return image
def get_background(sheet, x, y, width, height,scalex,scaley,reverse = False):
        """Extracts image from sprite sheet"""
        
        image = pg.Surface([width, height])
        

        image.blit(sheet, (0, 0), (x, y, width, height))
        
        image = pg.transform.scale(image,(scalex,scaley))
        if reverse:
        	image = pg.transform.flip(image,True,False)
        if image.get_alpha():
            image = image.convert_alpha()
        else:
            image = image.convert()
            image.set_colorkey((0,0,0))
        return image
def collided(this,other):
    return this.hitbox.colliderect(other.rect)

def collided_1(this,other,lmao =False):
    return this.rect_ground_detector.colliderect(other.rect)

def collided_2(this,other):
	return this.hitbox_2.colliderect(other.rect)
	
def function_1(function):
	return function

def pass_events(event,objective):
    return event