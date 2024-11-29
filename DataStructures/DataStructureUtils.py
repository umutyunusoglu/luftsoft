from DataStructures.MapStructs import Cell

def distance(cell1: Cell, cell2: Cell) -> float:
    """
    Function to calculate the manhattan distance between two cells

    cell1: Cell -> First Cell
    cell2: Cell -> Second Cell
    """
    coords1 = cell1.get_coordinates()
    coords2 = cell2.get_coordinates()

    return abs(coords1[0] - coords2[0]) + abs(coords1[1] - coords2[1])