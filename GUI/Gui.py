import pygame
import DataStructures as ds
from typing import Tuple,Dict
from Pathfinding import Dijktra
from GUI.GuiUtils import draw_bordered_rect,grid_to_cell

def draw_map(screen,
             grid: ds.Map,
             top_left:Tuple[int,int],
             cell_height:int,
            cell_width:int,
             color_map:Dict[ds.CellType,Tuple[int,int,int]]) -> None:
    """
    Function to draw the map on the screen

    screen: pygame.Surface -> Pygame Surface
    map: ds.Map -> Map Object
    left_corner: Tuple[int,int] -> Left Corner of the Map
    cell_size: int -> Size of the Cell
    color_map: Dict[ds.CellType,Tuple[int,int,int]] -> Color Map for the Cell Types
    """


    cells = grid.get_cells()

    current_x = top_left[0]
    current_y = top_left[1]

    for i in range(len(cells)):
        for j in range(len(cells[i])):

            cell=cells[i][j]
            color=color_map[cell.type]

            draw_bordered_rect(screen,current_x,current_y,cell_height,cell_width,color)

            current_x += cell_width

        current_x = top_left[0]
        current_y += cell_height



def draw_cursor_modes(screen,cell_size,top_left,cursor_modes):
    """
    Function to draw the cursor modes on the screen

    screen: pygame.Surface -> Pygame Surface
    cell_size: int -> Size of the Cell
    top_left: Tuple[int,int] -> Top Left Corner of the Map
    cursor_modes: Dict[ds.CellType,Tuple[int,int,int]] -> Cursor Modes
    """

    current_x = top_left[0]
    current_y = top_left[1]

    font = pygame.font.Font(None, 16)

    for mode,color in cursor_modes.items():

        if(mode!=ds.CellType.PATH):

            match mode:

                case ds.CellType.EMPTY:

                    text=font.render("Empty",True,"black")

                case ds.CellType.WALL:

                    text=font.render("Wall",True,"black")

                case ds.CellType.FULL:

                    text=font.render("Full",True,"black")

                case ds.CellType.ROAD:

                    text=font.render("Road",True,"black")

                case ds.CellType.START:

                    text=font.render("Start",True,"black")


            draw_bordered_rect(screen,current_x,current_y,cell_size,cell_size,color)


            screen.blit(text,(current_x+5,current_y+1.2*cell_size))
            current_x += cell_size





def draw_menu(screen,run_top_left:Tuple[int,int],clear_top_left:Tuple[int,int],cell_size):
        font = pygame.font.Font(None, 16)
        start_text = font.render("Find Closest Park", True, "black")
        clear_text= font.render("Reset Simulation",True,"black")


        start_rect=pygame.Rect(run_top_left[0],run_top_left[1],cell_size,cell_size)
        clear_rect=pygame.Rect(clear_top_left[0],clear_top_left[1],cell_size,cell_size)

        start_text_rect=start_text.get_rect(center=start_rect.center)
        clear_text_rect=clear_text.get_rect(center=clear_rect.center)

        pygame.draw.rect(screen,(255,0,0),start_rect)
        pygame.draw.rect(screen,(255,0,0),clear_rect)


        screen.blit(start_text,start_text_rect)
        screen.blit(clear_text,clear_text_rect)





def main_loop(screen_size=(800, 600),matrix_size=(10,10)):

    pygame.init()
    screen = pygame.display.set_mode(screen_size)

    # Create a Map
    map = ds.Map(matrix_size[0],matrix_size[1])

    top_left=screen_size[0]//4,screen_size[1]//4
    bottom_right = (screen_size[0]//4)*3,(screen_size[1]//4)*3

    cell_height=(bottom_right[1]-top_left[1])//matrix_size[1]
    cell_width=(bottom_right[0]-top_left[0])//matrix_size[0]



    cursor_mode=ds.CellType.EMPTY

    cursor_mode_top_left=((screen_size[0]//100*5),
                          (screen_size[1]//100)*5)

    cursor_mode_size=(screen_size[0]//100)*5


    start_top_left = (screen_size[0]//100*60),(screen_size[1]//100)*5
    clear_top_left = (screen_size[0]//100*80),(screen_size[1]//100)*5

    start_size = (screen_size[0]//100)*10
    clear_size = (screen_size[0]//100)*10



    color_map={ ds.CellType.ROAD:(0,0,0),
                ds.CellType.WALL:(15,0,255),
                ds.CellType.FULL:(255,45,0),
                ds.CellType.EMPTY: (255, 255, 255),
                ds.CellType.START: (102,255,255),
                ds.CellType.PATH: (153,51,255)}

    menu_rects = {
        ds.CellType.ROAD: pygame.Rect(cursor_mode_top_left[0],
                             cursor_mode_top_left[1],
                             cursor_mode_size, cursor_mode_size),

        ds.CellType.WALL: pygame.Rect(cursor_mode_top_left[0]+cursor_mode_size,
                             cursor_mode_top_left[1],
                             cursor_mode_size, cursor_mode_size),

        ds.CellType.FULL: pygame.Rect(cursor_mode_top_left[0]+cursor_mode_size*2,
                             cursor_mode_top_left[1],
                             cursor_mode_size, cursor_mode_size),

        ds.CellType.EMPTY: pygame.Rect(cursor_mode_top_left[0]+cursor_mode_size*3,
                                cursor_mode_top_left[1],
                                cursor_mode_size, cursor_mode_size),

        ds.CellType.START: pygame.Rect(cursor_mode_top_left[0]+cursor_mode_size*4,
                                cursor_mode_top_left[1],
                                cursor_mode_size, cursor_mode_size),

        "Run": pygame.Rect(start_top_left[0],start_top_left[1],start_size,start_size),
        "Clear": pygame.Rect(clear_top_left[0],clear_top_left[1],clear_size,clear_size)
    }




    start_cell=None


    running = True

    # Main Loop for Pygame Window
    while running:

        # Event Loop
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:  # Keyboard Event

                if (event.key == pygame.K_q):  # Q Key Pressed -> Quit
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:  # Mouse Click Event -> Print the Position
                event_pos = pygame.mouse.get_pos()

                menu_click = False

                for key, rect in menu_rects.items():
                    if rect.collidepoint(event_pos):
                        if(key=="Run"):
                            path=Dijktra(map)

                            for cell in path:
                                map.set_cell_type(cell[0],cell[1],ds.CellType.PATH)

                        elif(key=="Clear"):
                            map.reset_cells()
                            start_cell=None
                        else:
                            cursor_mode = key
                            print(f"Cursor Mode: {cursor_mode}")
                            menu_click = True

                if not menu_click:

                    x, y = grid_to_cell(event_pos[0], event_pos[1], cell_height,cell_width, top_left)
                    print(x,y)

                    if(0<=x<matrix_size[0] and 0<=y<matrix_size[1]):

                        if(cursor_mode==ds.CellType.START):


                            if start_cell is not None:
                                map.set_cell_type(start_cell[0],start_cell[1],ds.CellType.ROAD)

                            map.set_cell_type(x,y,cursor_mode)
                            start_cell=(x,y)

                        else:
                            x,y = grid_to_cell(event_pos[0],event_pos[1],cell_height,cell_width,top_left)
                            map.set_cell_type(x,y,cursor_mode)


        screen.fill("green")


        draw_map(screen,map,top_left,cell_height,cell_width,color_map)

        draw_cursor_modes(screen,cursor_mode_size,cursor_mode_top_left,color_map)

        draw_menu(screen,start_top_left,clear_top_left,start_size)
        pygame.display.flip()
