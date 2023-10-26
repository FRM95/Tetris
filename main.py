from piece import Piece
import tetris_functions
import keyboard

if __name__ == "__main__":

    random_piece, random_state = tetris_functions.create_figure()
    piece = Piece()
    piece.generatePiece(random_piece, random_state)
    screen = tetris_functions.create_screen(20,10)
    tetris_functions.show_screen(screen)
    screen = tetris_functions.insert_figure(screen, piece.figure)
    new_rotation = 0
    while True:

        tetris_functions.show_screen(screen)
        events = keyboard.read_event()
        if events.name == 'esc':
            break
        
        elif events.event_type == keyboard.KEY_DOWN:
            if events.name == "s":
                screen, new_rotation = tetris_functions.move_piece(screen, "DOWN", piece, new_rotation)
            if events.name == "d":
                screen, new_rotation = tetris_functions.move_piece(screen, "RIGHT", piece, new_rotation)
            if events.name == "a":
                screen, new_rotation = tetris_functions.move_piece(screen, "LEFT", piece, new_rotation)
            if events.name == "space":
                screen, new_rotation = tetris_functions.move_piece(screen, "ROTATE", piece, new_rotation)
        