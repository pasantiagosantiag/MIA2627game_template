import sys
import pygame
from enum import Enum
from lanzadera import Lanzadera
from burbuja import Burbuja
from burbujatype import BurbujaType
from game import Game



def calc_burbujas_dic(spriters:pygame.Surface) ->dict[BurbujaType,  pygame.Surface]:
    burbujas: dict[BurbujaType,  pygame.Surface] = {}
    burbujas[BurbujaType.ROJA]=spriters.subsurface(pygame.Rect(436, 2614, 16,16))
    burbujas[BurbujaType.VERDE]=spriters.subsurface(pygame.Rect(436, 2647, 16,16))
    burbujas[BurbujaType.AZUL]=spriters.subsurface(pygame.Rect(1, 1854, 16,16))
    burbujas[BurbujaType.AMARILLA]=spriters.subsurface(pygame.Rect(555, 1854, 16,16))
    burbujas[BurbujaType.NARANJA]=spriters.subsurface(pygame.Rect(436, 2680, 16,16))
    return burbujas
def paint_board(canvas:pygame.Surface,
                game:Game, 
                fondo:pygame.Surface,
                spriters:pygame.Surface,lanzadera:pygame.Surface,
                scale:float,
                offset_x: int = 0,
    offset_y: int = 0) ->None:
    internal_x_off_set=16
    canvas.blit(fondo, (0, 0))
    for fila_idx, fila in enumerate(game.get_board().get_board()):
        for col_idx, burbuja in enumerate(fila):
            burbuja=game.get_cell(fila_idx,col_idx)
            if burbuja is not None:
                if(fila_idx %2 ==0):
                    internal_x_off_set=0
                else:
                    internal_x_off_set=8*ESCALA
                # Posición donde se dibujará en la pantalla
                destino_x = internal_x_off_set+offset_x+(col_idx * TAM_SPRITE)
                destino_y = offset_y+ (fila_idx * TAM_SPRITE)

                trozo =burbujas[burbuja] #face(pygame.Rect(burbuja.x, burbuja.y, 16,16))
                trozo_escalado = pygame.transform.scale_by(trozo, ESCALA)
                canvas.blit(trozo_escalado, (destino_x, destino_y))
    p=game.get_lanzadera().get_position()
    #dibujar las dos burbujas del juego
    paint_burbuja(canvas=canvas,next_burbuja=game.get_next_burbuja(),scale=scale)
    if(game.get_current_burbuja()!=None):
        paint_burbuja(canvas=canvas,next_burbuja=game.get_current_burbuja(),scale=scale)

    canvas.blit(pygame.transform.scale_by(lanzadera, scale),((96+p[0])*scale,(224-60)*scale))
    #text_surface = my_font.render(str(game.get_degree()), False, (255, 0, 0)) 
    #canvas.blit(text_surface,((102+p[0])*scale,(224-50)*ESCALA))
def paint_burbuja(canvas:pygame.Surface,next_burbuja:Burbuja,scale:float):
    destino_x = (96+(next_burbuja.get_position()[0]))*scale# * TAM_SPRITE)
    destino_y =  int(24+next_burbuja.get_position()[1])*scale  
    next_trozo =burbujas[next_burbuja.get_type()] #face(pygame.Rect(burbuja.x, burbuja.y, 16,16))
    next_escalado = pygame.transform.scale_by(next_trozo, ESCALA)
    canvas.blit(next_escalado, (destino_x, destino_y))
def calc_lanzadera_spriters(spriters:pygame.Surface) ->[]:
    lanzadera_spriters=[None]*64
    #lanzadera_spriters_invertido=[None]*64
    #se leen la mitad
    for index in range(0,64,1):
        columna=int(index % 16)
        fila:int= int(index / 16)
        trozo = spriters.subsurface(pygame.Rect(columna*64+columna+1,fila*64+1545+fila, 64,64))
        lanzadera_spriters[index]=trozo
    #se copia la mitad y se hace el espejo
    lanzadera_spriters_invertidos = [
    pygame.transform.flip(sprite, True, False) for sprite in lanzadera_spriters
][::-1]    
    #se unen
    lanzadera_spriters= lanzadera_spriters_invertidos+lanzadera_spriters
    return lanzadera_spriters





ALTO, ANCHO = 640, 448
ESCALA=ALTO/320
TAM_SPRITE = 16*ESCALA
left_pressed:bool=False
rigth_pressed:bool=False

pygame.init()
pantalla = pygame.display.set_mode((ALTO,ANCHO)) 
pygame.display.set_caption("PuzzleBoubble")
pygame.mixer.init()

pygame.mixer.music.load("./sounds/song1.mp3")
reloj = pygame.time.Clock()
ejecutando = True
imagen_fondo = pygame.image.load("./images/fondos.png").convert()
spriters= pygame.image.load("./images/spriters.png").convert_alpha()



fondo = imagen_fondo.subsurface(pygame.Rect(16, 16, 320, 240))
burbujas: dict[BurbujaType,  pygame.Surface] = calc_burbujas_dic(spriters)
lanzadera_spriters=calc_lanzadera_spriters(spriters)
game:Game=Game(["./levels/level1.txt"])
pygame.mixer.music.load("./sounds/song1.mp3")
fondo_escalado = pygame.transform.scale_by(fondo, ESCALA)
pygame.mixer.music.play(-1)
while ejecutando:
   # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            print("Clic detectado:", evento.pos)
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                
                left_pressed=True
                #lanzadera.move_left()
            elif evento.key == pygame.K_RIGHT:
                #print("Flecha derecha")
                rigth_pressed=True
                #lanzadera.move_right() 
            elif evento.key ==pygame.K_r:
                game.reset();           
        elif evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT:
                
                left_pressed=False
                #lanzadera.move_left()
            elif evento.key == pygame.K_RIGHT:
                #print("Flecha derecha")
                rigth_pressed=False
                #lanzadera.move_right()
            elif evento.key == pygame.K_UP:
                print("Flecha arriba")
            elif evento.key == pygame.K_DOWN:
                print("Flecha abajo")
            elif evento.key == pygame.K_SPACE:
                
                game.shoot()
    #pantalla.blit(fondo_escalado, (0, 0))
    paint_board(pantalla,
                game,
                fondo_escalado,
                spriters,
                lanzadera_spriters[game.get_lanzadera_position()],
                ESCALA,
                96*ESCALA,24*ESCALA)
    pygame.display.flip()
    game.update()
    if(left_pressed):
        game.move_left()
    elif(rigth_pressed):
        game.move_right()
    #  60 FPS
    reloj.tick(60)
pygame.mixer.music.stop()  
pygame.mixer.music.unload() 
pygame.mixer.quit()
pygame.quit()
sys.exit()


def calc_burbujas_dic(spriter:pygame.Surface) ->dict[BurbujaType,  pygame.Surface]:
    burbujas: dict[BurbujaType,  pygame.Surface] = {}
    burbujas[BurbujaType.ROJA]=spriters.subsurface(pygame.Rect(436, 2614, 16,16))
    burbujas[BurbujaType.VERDE]=spriters.subsurface(pygame.Rect(436, 2647, 16,16))
    burbujas[BurbujaType.AZUL]=spriters.subsurface(pygame.Rect(1, 1854, 16,16))
    burbujas[BurbujaType.AMARILLA]=spriters.subsurface(pygame.Rect(555, 1854, 16,16))
    burbujas[BurbujaType.NARANJA]=spriters.subsurface(pygame.Rect(436, 2680, 16,16))
    return burbujas
def paint_board(canvas:pygame.Surface,
                game:Game, 
                fondo:pygame.Surface,
                spriters:pygame.Surface,lanzadera:pygame.Surface,
                scale:float,
                offset_x: int = 0,
    offset_y: int = 0) ->None:
    internal_x_off_set=16
    canvas.blit(fondo, (0, 0))
    for fila_idx, fila in enumerate(game.get_board().get_board()):
        for col_idx, burbuja in enumerate(fila):
            burbuja=game.get_cell(fila_idx,col_idx)
            if burbuja is not None:
                if(fila_idx %2 ==0):
                    internal_x_off_set=0
                else:
                    internal_x_off_set=8*ESCALA
                # Posición donde se dibujará en la pantalla
                destino_x = internal_x_off_set+offset_x+(col_idx * TAM_SPRITE)
                destino_y = offset_y+ (fila_idx * TAM_SPRITE)

                trozo =burbujas[burbuja] #face(pygame.Rect(burbuja.x, burbuja.y, 16,16))
                trozo_escalado = pygame.transform.scale_by(trozo, ESCALA)
                canvas.blit(trozo_escalado, (destino_x, destino_y))
    p=game.get_lanzadera().get_position()
    #dibujar las dos burbujas del juego
    paint_burbuja(canvas=canvas,next_burbuja=game.get_next_burbuja(),scale=scale)
    if(game.get_current_burbuja()!=None):
        paint_burbuja(canvas=canvas,next_burbuja=game.get_current_burbuja(),scale=scale)

    canvas.blit(pygame.transform.scale_by(lanzadera, scale),((96+p[0])*scale,(224-60)*scale))
    #text_surface = my_font.render(str(game.get_degree()), False, (255, 0, 0)) 
    #canvas.blit(text_surface,((102+p[0])*scale,(224-50)*ESCALA))
def paint_burbuja(canvas:pygame.Surface,next_burbuja:Burbuja,scale:float):
    destino_x = (96+(next_burbuja.get_position()[0]))*scale# * TAM_SPRITE)
    destino_y =  int(24+next_burbuja.get_position()[1])*scale  
    next_trozo =burbujas[next_burbuja.get_type()] #face(pygame.Rect(burbuja.x, burbuja.y, 16,16))
    next_escalado = pygame.transform.scale_by(next_trozo, ESCALA)
    canvas.blit(next_escalado, (destino_x, destino_y))
def calc_lanzadera_spriters(spriters:pygame.Surface) ->[]:
    lanzadera_spriters=[None]*64
    #lanzadera_spriters_invertido=[None]*64
    #se leen la mitad
    for index in range(0,64,1):
        columna=int(index % 16)
        fila:int= int(index / 16)
        trozo = spriters.subsurface(pygame.Rect(columna*64+columna+1,fila*64+1545+fila, 64,64))
        lanzadera_spriters[index]=trozo
    #se copia la mitad y se hace el espejo
    lanzadera_spriters_invertidos = [
    pygame.transform.flip(sprite, True, False) for sprite in lanzadera_spriters
][::-1]    
    #se unen
    lanzadera_spriters= lanzadera_spriters_invertidos+lanzadera_spriters
    return lanzadera_spriters
