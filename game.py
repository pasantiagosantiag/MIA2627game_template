from board import Board
from lanzadera import Lanzadera
from burbujatype import BurbujaType
from rectangle import Rectangle
from burbuja import Burbuja
import random
from enum import Enum, auto
import math

class Game:
    ROWS:int=8
    COLUMNS:int=8
    MIN_GROUP:int=2
    
    def __init__(self,levels:list[str],width:int=128,height:int=200 ):
        self._board=Board() 
        self._rectangle=Rectangle(0,0,width,height)
        self._lanzadera=Lanzadera()
        self._board.load_board(levels[0])
        self._selected_burbuja: BurbujaType| None= None
        self._selected_column:int=0
        self._current_burbuja:Burbuja|None=None #self.generate_next()
        self._next_burbuja:Burbuja|None=self.generate_next()
        
    def next_selected_buburja(self):
        self._selected_burbuja= BurbujaType.AMARILLA
    def next_selected_column(self):
        self._selected_column+=1
        if(self._selected_column>=Game.COLUMNS):
            self._selected_column=0
    def last_selected_column(self):
        self._selected_column-=1
        if(self._selected_column<0):
            self._selected_column=Game.COLUMNS-1
    def add_burbuja(self,b:BurbujaType,row:int,column:int):
        self._board.add_burbuja(b,row,column)
    def get_cell(self,row:int,column:int) ->BurbujaType| None:
        return self._board.get_cell(row,column)
    def move_left(self):
        self._lanzadera.move_left()
    def move_right(self):
        self._lanzadera.move_right()
    def get_lanzadera_position(self) ->int:
        return self._lanzadera.get_current()
    def get_board(self) ->Board:
        return self._board
    def update(self):
        
        if(self._current_burbuja!=None):
            
            self._current_burbuja.move()
            type=self._current_burbuja.get_type()
            collision=self._board.eval_collision(self._current_burbuja)
            if(collision!=None):
                x=collision[1]
                y=collision[0]   
                self._board.add_burbuja(self._current_burbuja.get_type(),collision[1],collision[0])
                self._current_burbuja=None
                visitados: list[list[bool]] = [[False] * Game.COLUMNS for _ in range(Game.ROWS)]
                grupo_encontrado: list[tuple[int, int]] = []
                self._board.eval_game(x,y,type,visitados,grupo_encontrado)
                if grupo_encontrado!=None and len(grupo_encontrado)>Game.MIN_GROUP:
                    self._board.remove_burbujas(grupo_encontrado)
                self._board.clear()

    def shoot(self):
        if self._current_burbuja==None :
            self._current_burbuja=self._next_burbuja
            speed=self.calc_speed()
            self._current_burbuja.set_speed(speed)
            self._next_burbuja=self.generate_next()
        
    def get_current_burbuja(self) ->Burbuja|None:
        return self._current_burbuja
    def get_next_burbuja(self) -> Burbuja| None:
        return self._next_burbuja
    def get_lanzadera(self) ->Lanzadera:
        return self._lanzadera
    def generate_next(self) ->Burbuja:
        burbuja_type: BurbujaType = random.choice(list(BurbujaType)) #BurbujaType.ROJA #random.choice(list(BurbujaType))
        burbuja=Burbuja(burbuja_type=burbuja_type,
                                       speed=(-1,-0.3),
                                       position=(self._lanzadera.get_center()[0]-8,
                                                 self._lanzadera.get_center()[1]-4), #(56,208),#self._lanzadera._position,
                                       size=(16,16),
                                       area=self._rectangle
                                       )
        return burbuja
    def calc_speed(self,velocidad=3.0) ->tuple[float,float]:
        # Obtener el ángulo actual de la lanzadera en grados
        angulo = self._lanzadera.get_degree()
        angulo_radianes = math.radians(angulo)
        # Calcular las componentes X e Y
        # +cos para X (derecha positivo, izquierda negativo)
        #-sin para Y (arriba es negativo en coordenadas de pantalla)
        v_x = -velocidad * math.cos(angulo_radianes)
        v_y = -velocidad * math.sin(angulo_radianes)
    
        return (v_x, v_y)
    def get_degree(self) ->float:
        return self._lanzadera.get_degree()
    def reset(self)->None:
        self._board.reset()