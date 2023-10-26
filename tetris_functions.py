
from piece import Piece
import random


def create_screen(rows:int, cols:int):
    my_screen = [[0]*cols for _ in range(rows)]
    return my_screen

def show_screen(screen:list) -> None:
    for row in screen:
        print("".join(map(lambda x: "⬜" if x == 0 else '⬛', row)))
    print("\n")
    return None

def create_figure():
    posibilities = {'O':["initial"],
                    'I':["vertical","horizontal"],
                    'J':["horizontal_down","vertical_left","horizontal_up","vertical_right"],
                    'L':["horizontal_down","vertical_left","horizontal_up","vertical_right"],
                    'T':["horizontal_down","left","horizontal_up","right"],
                    'S':["horizontal","vertical"],
                    'Z':["horizontal","vertical"]
            }
    random_selection = random.choice(list(posibilities.items()))
    random_piece = random_selection[0]
    random_state = random.choice(random_selection[1])
    return random_piece, random_state

def insert_figure(screen:list, figure:list):
    position = random.randint(0, len(screen[0]))
    max_position = len(screen[0]) - len(max(figure, key= len))
    if position > max_position:
        position = max_position
    for row in range(len(figure)):
        for col in range(len(figure[row])):
            if figure[row][col] == 1:
                screen[row][col+position] = 1
    return screen

def move_piece(screen:list, movement: str, piece:Piece, rotation_state: int = 0):
    
    # Get piece properties
    rotations_dict = piece.getCurrentRotation() # Piece rotations allowed
    current_state = rotation_state # Current piece state rotation
    rotation_index = 0 # Rotation position iterator

    # Check piece state
    if current_state > 3:
        current_state = 0
    elif current_state < 0:
        current_state = 0

    # New screen creation for next iteration
    final = False
    new_screen = []
    pixel_change = lambda x:x if x==2 else 0
    for i in range(len(screen)):
        new_screen.append(list(map(pixel_change, screen[i])))

    # Screen iteration in search of movements
    for row_index, row in enumerate(screen):
        for col_index, pixel, in enumerate(row):

            if pixel == 1:

                new_row_index = 0
                new_col_index = 0
                
                match movement:

                    case 'DOWN':
                        new_row_index = row_index + 1
                        new_col_index = col_index

                    case 'RIGHT':
                        new_row_index = row_index
                        new_col_index = col_index + 1

                    case 'LEFT':
                        new_row_index = row_index
                        new_col_index = col_index - 1

                    case 'ROTATE':
                        new_row_index = row_index + rotations_dict.get(current_state)[rotation_index][0]
                        new_col_index = col_index + rotations_dict.get(current_state)[rotation_index][1]
                        rotation_index+=1

                    case _:
                        break

                # Border cases
                if new_col_index < 0 or new_col_index == len(screen[0]):
                    return screen, current_state
                
                # Floor case
                elif new_row_index == len(screen):
                    return screen, current_state
                
                # Piece collision
                elif new_screen[new_row_index][new_col_index] == 2:
                    return screen, current_state
                
                # Movement allowed
                else:

                    new_screen[new_row_index][new_col_index] = 1

                    # If movement finished with final screen or piece collision
                    if new_row_index == len(screen) - 1 or new_screen[new_row_index+1][new_col_index] == 2:
                      final = True        

    if movement == 'ROTATE':
        if current_state == 3:
            current_state = 0
        else: 
            current_state +=1        
    else:
        current_state = 0         

    # If piece reached final
    if final:
        for i_y, y in enumerate(new_screen):
            for i_x, x, in enumerate(y):
                    if x == 1:
                        new_screen[i_y][i_x] = 2

    # if there is a row full
    for row_i, row in enumerate(new_screen):
        if all(el == 2 for el in row):
            new_screen.pop(row_i)
            new_screen.insert(0, [0]*len(row))
    
    if final:
        random_piece, random_state = create_figure()
        piece.generatePiece(random_piece,random_state)
        new_screen = insert_figure(new_screen, piece.figure)
            
    return new_screen, current_state