import pygame

def draw_bordered_rect(surface,x,y,cell_height,cell_width,color):
    pygame.draw.rect(surface, color, (x, y,cell_width,cell_height), 0)



def grid_to_cell(grid_x,grid_y,cell_height,cell_width,top_left):
    return  (grid_y - top_left[1]) // cell_height,(grid_x - top_left[0]) // cell_width