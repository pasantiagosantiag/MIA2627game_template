
class Lanzadera:
    _step:float=180/128
    def __init__(self,position:tuple[int,int]=(32,200-64)):
        self._current=0
        self._position=position
    def move_left(self):
        self._current-=1
        if(self._current<0):
            self._current=0
    def move_right(self):
            self._current+=1
            if(self._current>127):
                self._current=127
    def get_current(self) ->int:
        return self._current
    def get_center(self) ->tuple[int,int]:
    
        return (self._position[0]+32,self._position[1]+32)
    def get_position(self):
        return self._position
    def get_degree(self) ->float:
         return self._current*180/128