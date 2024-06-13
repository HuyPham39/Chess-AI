import tkinter as tk

# Create main window
main_window = tk.Tk()

# Set the parameters for the window
SCALE = .8
main_window.geometry(f'{int((SCALE * main_window.winfo_screenwidth()) // 1)}x{(int(SCALE * main_window.winfo_screenheight()) // 1)}')
main_window.title('Cờ vua siêu trí tuệ, BIG BRAIN')

# Set up the board for the pieces
background_img = tk.PhotoImage(file = 'G:\\Programming\\Tests\\Chess_AI_project\\images\\cylinder-8x8.png')
board = tk.Canvas(main_window, width= background_img.width(), height= background_img.height())
board.place(relx = 0.5, rely = 0.5, anchor = 'center')
board.create_image(2,0, image = background_img, anchor= 'nw')

# Create a list representing squares on the board, the outer layer of the nested list represents the collumns 
# from A-H and the inner layer represents the row idexes
squares = []
for collumns in range(8):
    squares.append([])
for collumns in squares:
    for rows in range(8):
       collumns.append(False)

# A list linking canvas images to objects
canvas_objects = {}

# Handles all the chesspieces' movements as well as the turn-based mechanism
from chess_pieces import *

legal_move_widgets = {}
castling_move_widgets = {}
focus = None
turn = "white"

def clear_legal_move_widgets():
    global legal_move_widgets, castling_move_widgets, board
    for canvas_id in legal_move_widgets:
        board.delete(canvas_id)
    legal_move_widgets = {}
    for canvas_id in castling_move_widgets:
        board.delete(canvas_id)
    castling_move_widgets = {}

def piece_picked(chess_piece):
    global legal_move_widgets, focus, board
    clear_legal_move_widgets()
    focus = chess_piece
    if chess_piece.type[6:] != "king":
        for legal_move in chess_piece.legal_move():
            legal_move_canvas_id = board.create_image(legal_move[0] * 96 + 2, legal_move[1] * 96 - 12, anchor='nw', image = legal_move_img)
            legal_move_widgets[legal_move_canvas_id] = legal_move
    else:
        for legal_move in refined_kings_legal_moves(chess_piece):
            legal_move_canvas_id = board.create_image(legal_move[0] * 96 + 2, legal_move[1] * 96 - 12, anchor='nw', image = legal_move_img)
            legal_move_widgets[legal_move_canvas_id] = legal_move
        for castling_move in castling_moves(chess_piece):
            castling_move_canvas_id = board.create_image(castling_move[0] * 96 + 2, castling_move[1] * 96 - 12, anchor='nw', image = legal_move_img)
            castling_move_widgets[castling_move_canvas_id] = castling_move
    

def move_chose(legal_move_canvas_id):
    global focus, squares, legal_move_widgets, turn
    position = legal_move_widgets[legal_move_canvas_id]
    if squares[position[0]] [position[1]] != False:
        squares[position[0]] [position[1]].destroy()
    focus.move(position)
    focus = None
    if turn == "white":
        turn = "black"
    else:
        turn = "white"
    clear_legal_move_widgets()

def button_clicked(event):
    global board, canvas_objects, turn
    canvas_ids = board.find_overlapping(event.x, event.y, event.x + 1, event.y + 1)[1:]
    if canvas_ids != ():
        if (canvas_ids[-1] in canvas_objects) and (canvas_objects[canvas_ids[-1]].type[:5] == turn):
            piece_picked(canvas_objects[canvas_ids[-1]])
        else:
            if canvas_ids[-1] in castling_move_widgets:
                castle(castling_move_widgets[canvas_ids[-1]], focus)
            else:
                move_chose(canvas_ids[-1])
    else:
        clear_focus()

def clear_focus():
    global focus
    focus = None
    clear_legal_move_widgets()

board.bind("<Button-1>", button_clicked)

# Refining the king's legal moves

def is_safe(kings_position):
    global turn
    for collumn in range(8):
        for square in squares[collumn]:
            if (square != False) and (square.type[:5] != turn):
                if kings_position in square.legal_move():
                    return False
    return True

def refined_kings_legal_moves(king):
    refined_legal_moves = []
    for move in king.legal_move():
        if is_safe(move):
            refined_legal_moves.append(move)
    for move in refined_legal_moves:
        temp = squares[move[0]] [move[1]]
        origin_king_pos = king.position
        origin_king_first_move_stat = king.first_move
        king.move(move)
        if not is_safe(move):
            refined_legal_moves.remove(move)
        squares[move[0]] [move[1]] = temp
        king.move(origin_king_pos)
        king.first_move = origin_king_first_move_stat
    return refined_legal_moves

def is_check(king):
    if is_safe(king.position):
        king.status = "Safe"
    else:
        king.status = "Check"

def castling_moves(king):
    castling_moves = []
    if king.first_move == True:
        for i in (0,7):
            if (squares[i] [king.position[1]].type == king.type[:5] + "-rook") and (squares[i] [king.position[1]].first_move == True):
                if castling_helper(i, king):
                    if i < 4:
                        castling_moves.append((2, king.position[1]))
                    else:
                        castling_moves.append((6, king.position[1]))
    return castling_moves

def castling_helper(i, king):
    if i < 4:
        for j in range(i + 1, 4):
            if squares[j] [king.position[1]] != False:
                return False
    else:
        for j in range(5, i):
            if squares[j] [king.position[1]] != False:
                return False
    return True

def castle(move, king):
    global squares, turn, focus
    king.move(move)
    if move[0] < 4:
        squares[0] [king.position[1]].move((move[0] + 1, move[1]))
    else:
        squares[7] [king.position[1]].move((move[0] - 1, move[1]))
    focus = None
    if turn == "white":
        turn = "black"
    else:
        turn = "white"
    clear_legal_move_widgets()

# Set up the default chess game

def default_game():
    squares[0] [0] = ChessPiece(board, squares, canvas_objects, 'black-rook', (0,0))
    squares[1] [0] = ChessPiece(board, squares, canvas_objects, 'black-knight', (1,0))
    squares[2] [0] = ChessPiece(board, squares, canvas_objects, 'black-bishop', (2,0))
    squares[3] [0] = ChessPiece(board, squares, canvas_objects, 'black-queen', (3,0))
    squares[4] [0] = ChessPiece(board, squares, canvas_objects, 'black-king', (4,0))
    squares[5] [0] = ChessPiece(board, squares, canvas_objects, 'black-bishop', (5,0))
    squares[6] [0] = ChessPiece(board, squares, canvas_objects, 'black-knight', (6,0))
    squares[7] [0] = ChessPiece(board, squares, canvas_objects, 'black-rook', (7,0))
    for i in range(8):
        squares[i] [1] = ChessPiece(board, squares, canvas_objects, 'black-pawn', (i,1))

    squares[0] [7] = ChessPiece(board, squares, canvas_objects, 'white-rook', (0,7))
    squares[1] [7] = ChessPiece(board, squares, canvas_objects, 'white-knight', (1,7))
    squares[2] [7] = ChessPiece(board, squares, canvas_objects, 'white-bishop', (2,7))
    squares[3] [7] = ChessPiece(board, squares, canvas_objects, 'white-queen', (3,7))
    squares[4] [7] = ChessPiece(board, squares, canvas_objects, 'white-king', (4,7))
    squares[5] [7] = ChessPiece(board, squares, canvas_objects, 'white-bishop', (5,7))
    squares[6] [7] = ChessPiece(board, squares, canvas_objects, 'white-knight', (6,7))
    squares[7] [7] = ChessPiece(board, squares, canvas_objects, 'white-rook', (7,7))
    for i in range(8):
        squares[i] [6] = ChessPiece(board, squares, canvas_objects, 'white-pawn', (i,6))

default_game()

main_window.mainloop()
