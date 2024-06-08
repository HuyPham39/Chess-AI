import tkinter as tk

# Create main window
main_window = tk.Tk()

# Set the parameters for the window
SCALE = 0.9
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
       collumns.append([])

# Handles all the chesspieces' movements
from chess_pieces import *

def clear_focus(event):
    global focus, potential_moves
    focus = None
    clear_widgets(potential_moves)

board.bind("<Button-1>", clear_focus)

# Set up the default chess game

def default_game():
    squares[0] [0] = ChessPiece(board, main_window, squares, 'black-rook', (0,0))
    squares[1] [0] = ChessPiece(board, main_window, squares, 'black-knight', (1,0))
    squares[2] [0] = ChessPiece(board, main_window, squares, 'black-bishop', (2,0))
    squares[3] [0] = ChessPiece(board, main_window, squares, 'black-queen', (3,0))
    squares[4] [0] = ChessPiece(board, main_window, squares, 'black-king', (4,0))
    squares[5] [0] = ChessPiece(board, main_window, squares, 'black-bishop', (5,0))
    squares[6] [0] = ChessPiece(board, main_window, squares, 'black-knight', (6,0))
    squares[7] [0] = ChessPiece(board, main_window, squares, 'black-rook', (7,0))
    for i in range(8):
        squares[i] [1] = ChessPiece(board, main_window, squares, 'black-pawn', (i,1))

    squares[0] [7] = ChessPiece(board, main_window, squares, 'white-rook', (0,7))
    squares[1] [7] = ChessPiece(board, main_window, squares, 'white-knight', (1,7))
    squares[2] [7] = ChessPiece(board, main_window, squares, 'white-bishop', (2,7))
    squares[3] [7] = ChessPiece(board, main_window, squares, 'white-queen', (3,7))
    squares[4] [7] = ChessPiece(board, main_window, squares, 'white-king', (4,7))
    squares[5] [7] = ChessPiece(board, main_window, squares, 'white-bishop', (5,7))
    squares[6] [7] = ChessPiece(board, main_window, squares, 'white-knight', (6,7))
    squares[7] [7] = ChessPiece(board, main_window, squares, 'white-rook', (7,7))
    for i in range(8):
        squares[i] [6] = ChessPiece(board, main_window, squares, 'white-pawn', (i,6))
default_game()



# a = squares[0] [1].potential_move(squares)
# squares[0] [1].move(a[1], squares)


main_window.mainloop()

