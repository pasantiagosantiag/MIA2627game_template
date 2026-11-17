from burbujatype import BurbujaType
from rectangle import Rectangle

class Burbuja:
    def __init__(self,
             burbuja_type:BurbujaType,
             speed:tuple[float,float],
             position:tuple[float,float],
             size:tuple[int,int],
             area:Rectangle):
        self._speed=speed
        self._position=position
        self._area=area
        self._size=size
        self._burbuja_type:BurbujaType=burbuja_type
    
    def get_type(self) ->BurbujaType:
        return self._burbuja_type
    def get_size(self) ->tuple[int,int]:
        return self._size
    def get_position(self) ->tuple[float,float]:
        return self._position
    def get_speed(self) -> tuple[float,float]:
        return self._speed
    def move(self):
        self._position=(self._position[0]+self._speed[0],self._position[1]+self._speed[1])
        if( self._position[0]<0):
            self._position=(0,self._position[1]+self._speed[1])
            self._speed=(self._speed[0]*-1,self._speed[1])
        elif (self._position[0]+self._size[0]>=self._area.width): 
            print(self._area.width,"--- ",self._position[0])       
            self._position=(self._area.width-self._size[0],self._position[1]+self._speed[1])
            self._speed=(self._speed[0]*-1,self._speed[1])

    def set_speed(self,speed:tuple[float,float]):
        self._speed=speed
