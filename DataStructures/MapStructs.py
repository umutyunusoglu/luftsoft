from dataclasses import dataclass
from enum import Enum
from typing import Tuple
import logging


class CellType(Enum):
    """
    Enum of Cell Types
    """
    EMPTY = 0
    WALL = 1
    FULL = 2
    ROAD = 3
    START = 4
    PATH = 5

@dataclass
class Cell:
    """
    Basic Cell Structure For a Map

    x: int -> x coordinate of the cell
    y: int -> y coordinate of the cell
    type: CellType -> type of the cell
    """

    _x: int
    _y: int
    type: CellType = CellType.ROAD
    current_distance:float=float("inf")
    is_visited:bool=False
    previous_cell=None

    def __str__(self):

        match self.type:
            case CellType.EMPTY:
                return " "
            case CellType.WALL:
                return "#"
            case CellType.FULL:
                return "X"
            case _:
                return " "

    def __hash__(self):
        return hash((self._x,self._y))

    def get_coordinates(self)->Tuple[int,int]:
        """
        Returns coordinates of the cell

        :return: Tuple[int,int]
        """

        return self._x,self._y



class Map():

    def __init__(self, width: int, height: int):
        """
        Constructor of the Map

        width: int -> width of the map
        height: int -> height of the map
        """
        self.__width = width
        self.__height = height
        self.__cells = [[Cell(x, y) for y in range(height)] for x in range(width)]
        self.__start_cell=None


    def get_empty_cells(self):
        """
        Returns the list of empty cells
        """
        return [cell for row in self.__cells for cell in row if cell.type == CellType.EMPTY]

    def get_cells(self):

        return self.__cells


    def set_cell_type(self,x,y,cell_type:CellType):
        """
        Function to set the cell type

        :param x: int
        :param y: int
        :param cell_type: CellType
        """
        self.__cells[x][y].type=cell_type

        if cell_type==CellType.START:
            if(self.__start_cell!=None):
                start_coords=self.__start_cell.get_coordinates()

                self.__cells[start_coords[0]][start_coords[1]].current_distance=float("inf")
                self.__cells[start_coords[0]][start_coords[1]].type=CellType.ROAD

            self.__cells[x][y].current_distance=0
            self.__start_cell=self.__cells[x][y]


    def set_visited(self,x,y):
        """
        Function to set the cell as visited

        :param x: int
        :param y: int
        """
        self.__cells[x][y].is_visited=True

    def get_possible_neighbours(self,x,y):




        neighbours=[]

        if(x-1>=0 and (self.__cells[x-1][y].type==CellType.ROAD or self.__cells[x-1][y].type==CellType.EMPTY)):
            neighbours.append(self.__cells[x-1][y])

        if(x+1<self.__width and (self.__cells[x+1][y].type==CellType.ROAD or self.__cells[x+1][y].type==CellType.EMPTY)):
            neighbours.append(self.__cells[x+1][y])

        if(y-1>=0 and (self.__cells[x][y-1].type==CellType.ROAD or self.__cells[x][y-1].type==CellType.EMPTY)):
            neighbours.append(self.__cells[x][y-1])

        if(y+1<self.__height and (self.__cells[x][y+1].type==CellType.ROAD or self.__cells[x][y+1].type==CellType.EMPTY)):
            neighbours.append(self.__cells[x][y+1])

        return neighbours


    def get_start_cell(self)->Cell:
        """
        Function to get the start cell

        :return: Cell
        """
        return self.__start_cell

    def reset_cells(self):
        """
        Function to reset the cells
        """
        for row in self.__cells:
            for cell in row:
                cell.is_visited=False
                cell.current_distance=float("inf")
                cell.type=CellType.ROAD
                cell.previous_cell=None


        self.__start_cell=None

