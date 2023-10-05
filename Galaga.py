import pygame, random, math, io
from pygame import mixer
#iniciar pygame
pygame.init()

#iniciar pantalla
screen = pygame.display.set_mode((1080, 675))

#titulo
pygame.display.set_caption('Invasion Alienigena')

#icono
icon = pygame.image.load('./galaga/nave.png')
pygame.display.set_icon(icon)


#Fondo de pantalla pero con imagen
wallpaper = pygame.image.load('./galaga/fondo.png')

#Agregar sonido
mixer.music.load('./galaga/sonidofondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

#personaje
character = pygame.image.load('./galaga/prota.png')
pi_x = 508
pi_y = 611
pf_x = 0
pf_y = 0
def position_character(x,y):
    screen.blit(character, (pi_x, pi_y))


#Enemigo 
enemy =[]
pi_x_ufo = []
pi_y_ufo  = []
pf_x_ufo  = []
pf_y_ufo  = []
num_enemix = 10

for e in range(num_enemix):
    enemy.append(pygame.image.load('./galaga/ufo.png'))
    pi_x_ufo .append(random.randint(0, 1016))
    pi_y_ufo.append(random.randint(30, 300))
    pf_x_ufo.append(5)
    pf_y_ufo.append(10)

def position_ufo(x,y, ene):
    screen.blit(enemy[ene], (pi_x_ufo[ene], pi_y_ufo[ene]))
    
#bala
bala = pygame.image.load('./galaga/bala.png')
bala_inicio_x = 0
bala_inicio_y = 0
bala_fin_x = 0
bala_finy = 10
bala_visible = False

def shot(x,y):
    global bala_visible
    bala_visible = True        
    screen.blit(bala, (x + 24 , y - 16 ))

def fuente_bytes(fuente):
    with open(fuente, 'rb') as f:
        ttf_bytes = f.read()
    return io.BytesIO(ttf_bytes)

fuentes_como_bytes = fuente_bytes('./galaga/FreeSansBold.ttf')
'''Deteccion de colociones.
para detectar una colison debemos de tener en cuenta una formula, y es la formula de la distancia.

D = √ (x2 - x1)^2 + (y2 - y1)^2

'''
#Puntaje 
puntaje = 0
font = pygame.font.Font(fuentes_como_bytes, 24)
puntaje_screen_x = 10
puntaje_screen_y = 10

def puntaje_display(x, y):
    text = font.render(f'Puntaje: {puntaje}', True, (255,255,255))
    screen.blit(text, (x,y))

#Colisones
def detect_colision(x1, y1, x2, y2):
    distancia = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
    if distancia < 35:
        return True
    else:
        return False    

#GAME OVER

text_gameover = pygame.font.Font(fuentes_como_bytes, 60)
def text_final():
    mi_fuente_final = text_gameover.render('GAME OVER', True, (255,255,255))
    screen.blit(mi_fuente_final, (330, 307))

#mantener pantalla 
screen_on = True
while screen_on:
    #Color de fondo de pantalla
    #screen.fill((205, 144,228))
    #FONDO DE PANTALLA CON FOTO
    screen.blit(wallpaper, (0,0))
    #Recorrido de eventos
    for event in pygame.event.get():
        #si en el recorrido se detecta un pygame.QUIT
        if event.type == pygame.QUIT:
            #screen_on cambia de valor a false para que ya no se mantenga la patalla
            screen_on = False
        #si en el recorrido detecta un evendo de apretar teclas
        if event.type == pygame.KEYDOWN:
            #si en el evento de detectar teclas detecta una tecla en especifico 
            if event.key == pygame.K_LEFT:
                pf_x = -3
            elif event.key == pygame.K_RIGHT:
                pf_x = +3
            elif event.key == pygame.K_DOWN:
                pf_y = +2
            elif event.key == pygame.K_UP:
                pf_y = -2  
            elif event.key == pygame.K_a:
                pf_x = -3
            elif event.key == pygame.K_d:
                pf_x = +3
            elif event.key == pygame.K_s:
                pf_y = +2
            elif event.key == pygame.K_w:
                pf_y = -2
            elif event.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('./galaga/rayo encogedor.mp3')
                vol_deseado_bala = 0.5
                sonido_bala.set_volume(vol_deseado_bala)
                sonido_bala.play()
                if not bala_visible:
                    bala_inicio_y = pi_y
                    bala_inicio_x = pi_x
                    shot(bala_inicio_x, bala_inicio_y)
        #si en el recorrido detecta un evendo de soltar teclas
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN or event.key == pygame.K_UP or event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_s or event.key == pygame.K_w:
                pf_x = 0
                pf_y = 0
        

  
    #modificar ubicacion de personaje
    pi_x += pf_x
    #mantener dentro de bordes (PONER LIMITES AL MAPA)
    if pi_x <= -2:
        pi_x = -2
    elif pi_x >= 1019:
        pi_x = 1019
    elif pi_y >= 611:
        pi_y = 611
    elif pi_y <= 0:
        pi_y = 0
    elif pi_y <= 520:
        pi_y = 520
    pi_y += pf_y        
    position_character(pi_x, pi_y)
    
              
    for e in range(num_enemix):
        #fin del game
        if pi_y_ufo[e] > 480:
            for k in range(num_enemix):
                pf_y_ufo[k] = 1000
                
            text_final()
            break
        #modificar ubicacion del enemigo
        pi_x_ufo[e] += pf_x_ufo[e]
        #mantener dentro de bordes al enemigo (PONER LIMITES AL MAPA)
        if pi_x_ufo[e] <= 0:
            pf_x_ufo[e] = 5
            pi_y_ufo[e] += pf_y_ufo[e]
        elif pi_x_ufo[e] >= 1016:
            pf_x_ufo[e] = -5
            pi_y_ufo[e] += pf_y_ufo[e]
        elif pi_y_ufo[e]>= 610:
            pi_x_ufo [e]= 5
        pi_y += pf_y      
        #Deteccion de colision
        colision = detect_colision(pi_x_ufo[e], pi_y_ufo[e], bala_inicio_x, bala_inicio_y)
        if colision:
            explosion = mixer.Sound('./galaga/EXPLOSION.mp3')
            vol_deseado = 0.5
            explosion.set_volume(vol_deseado)
            explosion.play()
            bala_inicio_y = pi_y
            bala_visible = False
            puntaje += 1
            pi_x_ufo[e] = random.randint(0, 1016)
            pi_y_ufo[e] = random.randint(30, 300)
        position_ufo(pi_x_ufo[e], pi_y_ufo[e], e)    
    #Movimiento bala
    if bala_inicio_y <= 16:
        bala_inicio_y = pi_y
        bala_visible = False
    if bala_visible:
        shot(bala_inicio_x, bala_inicio_y)
        bala_inicio_y -= bala_finy
          
    position_character(pi_x, pi_y)    
   
    #mostrar puntaje 
    puntaje_display(puntaje_screen_x, puntaje_screen_y)
    #actualizacion de pantalla
    pygame.display.update()
    
    
    
    

