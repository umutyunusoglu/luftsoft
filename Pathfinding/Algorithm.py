from DataStructures import Map,CellType,distance
from typing import Tuple,List
from math import inf


def Dijktra(grid:Map)->List[Tuple[int,int]]:

    empty_cells = grid.get_empty_cells()

    start_cell=grid.get_start_cell()

    if(len(empty_cells)==0):
        print("No Empty Cells")
        return []

    if(start_cell==None):
        print("No Start Cell")
        return []
    target_cell=None
    target_cell_dist=float("inf")



    for cell in empty_cells:

        dist=distance(start_cell,cell)

        if dist<target_cell_dist:
            target_cell=cell
            target_cell_dist=dist


    cells_Grid=grid.get_cells()

    cells=[]
    for row in cells_Grid:
        for cell in row:
            if cell.type!=CellType.WALL:
                cells.append(cell.get_coordinates())

    dist_dict={cell : inf for cell in cells}
    prev={cell : None for cell in cells}

    dist_dict[start_cell.get_coordinates()]=0

    while cells:

        u=min(cells,key=dist_dict.__getitem__)

        cells.remove(u)

        for v in grid.get_possible_neighbours(*u):

            alt=dist_dict[u]+1

            if(alt<dist_dict[v.get_coordinates()]):
                dist_dict[v.get_coordinates()]=alt
                prev[v.get_coordinates()]=u


    if(dist_dict[target_cell.get_coordinates()]==inf):
        print("No Path")
        return []
    grid.set_cell_type(*target_cell.get_coordinates(),CellType.END)
    path=[]
    cur=target_cell.get_coordinates()

    while prev[cur]!=None:
        path.append(prev[cur])
        cur=prev[cur]

    return list(reversed(path))


























