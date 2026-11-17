from burbujatype import BurbujaType
from burbuja import Burbuja
from collections import deque
import math
Tablero = list[list[BurbujaType | None]]
class Board:
    ROWS:int=8
    COLUMNS:int=8 
    RADIO=8
    DIAMETRO=16
    _board:Tablero
   
    def __init__(self):
        self._board:Tablero=[[None for _ in range(self.ROWS)] for _ in range(self.COLUMNS)] 

    def add_burbuja(self,b:BurbujaType,row:int,column:int):
            self._board[row][column]=b
    def get_cell(self,row:int,column:int) ->int|None:
        if(row<0 or row>=self.ROWS or column<0 or column>=self.COLUMNS):
            return None
        else:
            return self._board[row][column]
    def get_row_free(self,column:int) ->int|None:
        vuelta:int|None=None
        if not (0 <= column < self.columnas):
            raise IndexError("Columna fuera de rango")
        # Recorremos las filas de abajo hacia arriba buscando la primera libre
        for fila in range(self.ROWS - 1, -1, -1):
            if self.matriz[fila][column] is None:
                vuelta = fila
                break
        return vuelta
    def eval_collision(self, burbuja: Burbuja) -> tuple[int, int] | None:
        
        y_burbuja = burbuja.get_position()[1]
        x_burbuja = burbuja.get_position()[0]
    
        #si la posición es menor que el radio
        if y_burbuja <= self.RADIO:
            # se calcula la 
            columna = round(x_burbuja / self.DIAMETRO)
            #por si sale algo de los bordes
            columna = max(0, min(columna, self.COLUMNS - 1))
            return (columna, 0)

        # se comprueba si colisiona con alguna celda
        # con una es suficiente
        for fila in range(self.ROWS):
            for columna in range(self.COLUMNS):
                cell = self._board[fila][columna]
                if cell is not None:
                    # Calcular el centro exacto de la celda en la matriz numero de columnas* diametro + la mita
                    cell_x = columna * self.DIAMETRO + self.RADIO
                    if fila % 2 == 1:
                        cell_x += self.RADIO  #desplazamiento de filas impares
                    cell_y = fila * self.DIAMETRO + self.RADIO
                
                    # Distancia  entre centros
                    distancia = math.hypot(x_burbuja - cell_x, y_burbuja - cell_y)
                
                    # Si la distancia es menor o igual al diámetro, hay colisión
                    if distancia <= self.DIAMETRO:
                        # puede ser que la colisión sea con más de una celda
                        # se calcula la más cercana
                        return self._encontrar_vecino_libre(x_burbuja, y_burbuja, fila, columna)
                    
        return None
    def _encontrar_vecino_libre(self, x_burbuja: float, y_burbuja: float, fila_impacto: int, col_impacto: int) -> tuple[int, int] | None:

        # Definir los desplazamientos relativos de los vecinos en una rejilla hexagonal
        # Depende de si la fila es par o impar
        if fila_impacto % 2 == 0:
            vecinos_offset = [
                (-1, -1), (0, -1),  # Arriba-izquierda, Arriba-derecha
                (-1,  0), (1,  0),  # Izquierda, Derecha
                (-1,  1), (0,  1)   # Abajo-izquierda, Abajo-derecha 
        ]
        else:
            vecinos_offset = [
                (0, -1), (1, -1),   # Arriba-izquierda, Arriba-derecha
                (-1, 0), (1,  0),   # Izquierda, Derecha
                (0,  1), (1,  1)    # Abajo-izquierda, Abajo-derecha
            ]
    
        mejor_vecino = None
        menor_distancia = float('inf')
    
        # Revisar los vecinos alrededor de la burbuja impactada
        for dcol, dfila in vecinos_offset:
            vecino_col = col_impacto + dcol
            vecino_fila = fila_impacto + dfila
        
            # Verificar que el vecino esté dentro de los límites de la matriz
            if 0 <= vecino_fila < self.ROWS and 0 <= vecino_col < self.COLUMNS:
                # Comprobar si la celda está libre (None)
                if self._board[vecino_fila][vecino_col] is None:
                    # Calcular el centro de esta celda candidata
                    cell_x = vecino_col * self.DIAMETRO + self.RADIO
                    if vecino_fila % 2 == 1:
                        cell_x += self.RADIO
                    cell_y = vecino_fila * self.DIAMETRO + self.RADIO
                
                    # Medir la distancia entre la burbuja móvil y el centro de esta celda vacía
                    dist = math.hypot(x_burbuja - cell_x, y_burbuja - cell_y)
                
                    # Nos quedamos con la celda vacía más cercana al punto donde impactó la burbuja
                    if dist < menor_distancia:
                        menor_distancia = dist
                        mejor_vecino = (vecino_col, vecino_fila)
                    
        # Si por alguna razón los vecinos directos están ocupados, puedes devolver la celda original o manejar un fallback
        return mejor_vecino if mejor_vecino else (col_impacto, fila_impacto)
    def reset(self):
        self._board:Tablero=[[None for _ in range(8)] for _ in range(8)] 
    def get_board(self):
        return self._board
    def load_board(self, path: str) -> None:
        # Diccionario para traducir cada letra del fichero a su Enum correspondiente
        mapa_burbujas: dict[str, BurbujaType] = {
            "R": BurbujaType.ROJA,
            "V": BurbujaType.VERDE,
            "A": BurbujaType.AZUL,
            "M": BurbujaType.AMARILLA,
            "N": BurbujaType.NARANJA,
        }
        with open(path, "r", encoding="utf-8") as fichero:
            for fila_idx, linea in enumerate(fichero):
                if fila_idx >= self.ROWS:
                    break  # Evita desbordar si el fichero tiene más de 8 líneas
                linea_limpia = linea.strip()
                for col_idx, caracter in enumerate(linea_limpia):
                    if col_idx >= self.COLUMNS:
                        break  # Evita desbordar si la línea tiene más de 8 caracteres

                    # .get() devuelve el Enum si existe la letra, o None si es un '.' u otro carácter
                    self._board[fila_idx][col_idx] = mapa_burbujas.get(caracter.upper())
    def remove_burbujas(self, items:list[tuple[int, int]]):
        for(fila, column) in items:
            self._board[fila][column]= None
        return None
    """
    Evalúa recursivamente el grupo de burbujas conectadas del mismo tipo.
    PARÁMETROS DE ENTRADA:
    ----------------------
    :param row: int
        Índice de la fila de la celda a evaluar.
    :param column: int
        Índice de la columna de la celda a evaluar.
    :param burbuja_type: BurbujaType
        El tipo/color de burbuja objetivo que se busca agrupar.
    :param visitados: list[list[bool]]
        Matriz bidimensional de booleanos de igual dimensión que el tablero.
        Sigue la traza de las celdas ya exploradas (True) para evitar ciclos infinitos.
    :param resultado: list[tuple[int, int]]
        Lista acumuladora de coordenadas (fila, columna) que pertenecen al grupo.
        Se va poblando progresivamente durante la fase de bajada recursiva.

    VALOR DE RETORNO:
    -----------------
    :return: list[tuple[int, int]]
        Lista con todas las coordenadas (fila, columna) pertenecientes al conjunto
        de burbujas conectadas del mismo tipo. Si la celda evaluada no es válida
        o ya fue visitada, retorna una lista vacía [].
    """
    def eval_game( self, row: int,column: int, burbuja_type: BurbujaType,visitados: list[list[bool]],
                   resultado: list[tuple[int, int]]
    ) -> list[tuple[int, int]]:
            return resultado
    
    def clear(self) ->None:
        return None