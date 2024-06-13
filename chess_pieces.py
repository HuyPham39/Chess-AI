import tkinter as tk
from pathlib import Path

script_path = Path(__file__).resolve()

black_rook_img = tk.PhotoImage(file = script_path.parent / 'images' / 'black-rook.png')
black_knight_img = tk.PhotoImage(file = script_path.parent / 'images' / 'black-knight.png')
black_bishop_img = tk.PhotoImage(file = script_path.parent / 'images' / 'black-bishop.png')
black_queen_img = tk.PhotoImage(file = script_path.parent / 'images' / 'black-queen.png')
black_king_img = tk.PhotoImage(file = script_path.parent / 'images' / 'black-king.png')
black_pawn_img = tk.PhotoImage(file = script_path.parent / 'images' / 'black-pawn.png')

white_rook_img = tk.PhotoImage(file = script_path.parent / 'images' / 'white-rook.png')
white_knight_img = tk.PhotoImage(file = script_path.parent / 'images' / 'white-knight.png')
white_bishop_img = tk.PhotoImage(file = script_path.parent / 'images' / 'white-bishop.png')
white_queen_img = tk.PhotoImage(file = script_path.parent / 'images' / 'white-queen.png')
white_king_img = tk.PhotoImage(file = script_path.parent / 'images' / 'white-king.png')
white_pawn_img = tk.PhotoImage(file = script_path.parent / 'images' / 'white-pawn.png')
legal_move_img =  tk.PhotoImage(file = script_path.parent / 'images' / 'potential-move.png')

class ChessPiece:
    def __init__(self, board, squares, canvas_objects, type, position):
        type_dict = {'black-rook': black_rook_img, 'black-knight': black_knight_img, 'black-bishop': black_bishop_img, 'black-queen': black_queen_img, 
                     'black-king': black_king_img, 'black-pawn': black_pawn_img,
                     
                     'white-rook': white_rook_img, 'white-knight': white_knight_img, 'white-bishop': white_bishop_img, 'white-queen': white_queen_img, 
                     'white-king': white_king_img, 'white-pawn': white_pawn_img
                     } 
        self.type = type
        self.position = position
        self.board = board
        self.squares = squares
        self.canvas_id = board.create_image(self.position[0] * 96 + 2, self.position[1] * 96 - 12, anchor='nw', 
                                          image = type_dict[self.type])
        canvas_objects[self.canvas_id] = self
        self.canvas_objects = canvas_objects
        self.first_move = True
        if self.type[6:] == "king":
            self.status = "Safe"



    def destroy(self):
        self.board.delete(self.canvas_id)
        self.canvas_objects.pop(self.canvas_id)

    def move(self, new_position):
        self.squares[self.position[0]] [self.position[1]] = False
        self.board.move(self.canvas_id, (new_position[0] - self.position[0]) * 96, (new_position[1] - self.position[1]) * 96)
        self.position = (new_position[0], new_position[1])
        self.squares[new_position[0]] [new_position[1]] = self
        self.first_move = False

    def legal_move(self):
        legal_moves = []
        if self.type == 'black-pawn':
            if self.squares[self.position[0]] [self.position[1] + 1] == False:
                legal_moves.append((self.position[0], self.position[1] + 1))
                if (self.first_move == True) and (self.squares[self.position[0]] [self.position[1] + 2] == False):
                    legal_moves.append((self.position[0], self.position[1] + 2))
            if ((self.position[0] + 1) < 8 and self.position[1] + 1 < 8) and self.squares[self.position[0] + 1] [self.position[1] + 1] != False:
                if "black" not in self.squares[self.position[0] + 1] [self.position[1] + 1].type:
                    legal_moves.append((self.position[0] + 1, self.position[1] + 1))
            if ((self.position[0] - 1) >= 0 and self.position[1] + 1 < 8) and self.squares[self.position[0] - 1] [self.position[1] + 1] != False:
                if "black" not in self.squares[self.position[0] - 1] [self.position[1] + 1].type:
                    legal_moves.append((self.position[0] - 1, self.position[1] + 1))

        if self.type == 'white-pawn':
            if self.squares[self.position[0]] [self.position[1] - 1] == False:
                legal_moves.append((self.position[0], self.position[1] - 1))
                if (self.first_move == True) and (self.squares[self.position[0]] [self.position[1] - 2] == False):
                    legal_moves.append((self.position[0], self.position[1] - 2))
            if ((self.position[0] + 1) < 8 and self.position[1] - 1 >= 0) and self.squares[self.position[0] + 1] [self.position[1] - 1] != False:
                if "white" not in self.squares[self.position[0] + 1] [self.position[1] - 1].type:
                    legal_moves.append((self.position[0] + 1, self.position[1] - 1))
            if ((self.position[0] - 1) >= 0 and self.position[1] - 1 >= 0) and self.squares[self.position[0] - 1] [self.position[1] - 1] != False:
                if "white" not in self.squares[self.position[0] - 1] [self.position[1] - 1].type:
                    legal_moves.append((self.position[0] - 1, self.position[1] - 1))

        if self.type == 'black-rook':
            basis_vector = (0,1)
            for j in range(4):
                change_in_pos = [basis_vector[0], basis_vector[1]]
                while ((0 <= self.position[0] + change_in_pos[0] < 8) and (0 <= self.position[1] + change_in_pos[1] < 8) and 
                       (self.squares[self.position[0] + change_in_pos[0]] [self.position[1] + change_in_pos[1]] == False)):
                    legal_moves.append((self.position[0] + change_in_pos[0], self.position[1] + change_in_pos[1]))
                    change_in_pos[0] += basis_vector[0]
                    change_in_pos[1] += basis_vector[1]
                if (((0 <= self.position[0] + change_in_pos[0] < 8) and (0 <= self.position[1] + change_in_pos[1] < 8)) and 
                    ("black" not in self.squares[self.position[0] + change_in_pos[0]] [self.position[1] + change_in_pos[1]].type)):
                    legal_moves.append((self.position[0] + change_in_pos[0], self.position[1] + change_in_pos[1]))
                basis_vector = (-basis_vector[1], basis_vector[0])

        if self.type == 'white-rook':
            basis_vector = [0,1]
            for j in range(4):
                change_in_pos = [basis_vector[0], basis_vector[1]]
                while ((0 <= self.position[0] + change_in_pos[0] < 8) and (0 <= self.position[1] + change_in_pos[1] < 8) and 
                       (self.squares[self.position[0] + change_in_pos[0]] [self.position[1] + change_in_pos[1]] == False)):
                    legal_moves.append((self.position[0] + change_in_pos[0], self.position[1] + change_in_pos[1]))
                    change_in_pos[0] += basis_vector[0]
                    change_in_pos[1] += basis_vector[1]
                if (((0 <= self.position[0] + change_in_pos[0] < 8) and (0 <= self.position[1] + change_in_pos[1] < 8)) and 
                    ("white" not in self.squares[self.position[0] + change_in_pos[0]] [self.position[1] + change_in_pos[1]].type)):
                    legal_moves.append((self.position[0] + change_in_pos[0], self.position[1] + change_in_pos[1]))
                basis_vector = (-basis_vector[1], basis_vector[0])

        if self.type == 'black-knight':
            basis_vector = (1,2)
            for i in range(4):
                if (0 <= self.position[0] + basis_vector[0] < 8) and (0 <= self.position[1] + basis_vector[1] < 8):
                    if (self.squares[self.position[0] + basis_vector[0]] [self.position[1] + basis_vector[1]] == False):
                        legal_moves.append((self.position[0] + basis_vector[0], self.position[1] + basis_vector[1]))
                    elif ("black" not in self.squares[self.position[0] + basis_vector[0]] [self.position[1] + basis_vector[1]].type):
                        legal_moves.append((self.position[0] + basis_vector[0], self.position[1] + basis_vector[1]))
                basis_vector = (-basis_vector[1], basis_vector[0])
            basis_vector = (2,1)
            for i in range(4):
                if (0 <= self.position[0] + basis_vector[0] < 8) and (0 <= self.position[1] + basis_vector[1] < 8):
                    if (self.squares[self.position[0] + basis_vector[0]] [self.position[1] + basis_vector[1]] == False):
                        legal_moves.append((self.position[0] + basis_vector[0], self.position[1] + basis_vector[1]))
                    elif ("black" not in self.squares[self.position[0] + basis_vector[0]] [self.position[1] + basis_vector[1]].type):
                        legal_moves.append((self.position[0] + basis_vector[0], self.position[1] + basis_vector[1]))
                basis_vector = (-basis_vector[1], basis_vector[0])

        if self.type == 'white-knight':
            basis_vector = (1,2)
            for i in range(4):
                if (0 <= self.position[0] + basis_vector[0] < 8) and (0 <= self.position[1] + basis_vector[1] < 8):
                    if (self.squares[self.position[0] + basis_vector[0]] [self.position[1] + basis_vector[1]] == False):
                        legal_moves.append((self.position[0] + basis_vector[0], self.position[1] + basis_vector[1]))
                    elif ("white" not in self.squares[self.position[0] + basis_vector[0]] [self.position[1] + basis_vector[1]].type):
                        legal_moves.append((self.position[0] + basis_vector[0], self.position[1] + basis_vector[1]))
                basis_vector = (-basis_vector[1], basis_vector[0])
            basis_vector = (2,1)
            for i in range(4):
                if (0 <= self.position[0] + basis_vector[0] < 8) and (0 <= self.position[1] + basis_vector[1] < 8):
                    if (self.squares[self.position[0] + basis_vector[0]] [self.position[1] + basis_vector[1]] == False):
                        legal_moves.append((self.position[0] + basis_vector[0], self.position[1] + basis_vector[1]))
                    elif ("white" not in self.squares[self.position[0] + basis_vector[0]] [self.position[1] + basis_vector[1]].type):
                        legal_moves.append((self.position[0] + basis_vector[0], self.position[1] + basis_vector[1]))
                basis_vector = (-basis_vector[1], basis_vector[0])

        if self.type == 'black-bishop':
            basis_vector = (1,1)
            for j in range(4):
                change_in_pos = [basis_vector[0], basis_vector[1]]
                while ((0 <= self.position[0] + change_in_pos[0] < 8) and (0 <= self.position[1] + change_in_pos[1] < 8) and 
                       (self.squares[self.position[0] + change_in_pos[0]] [self.position[1] + change_in_pos[1]] == False)):
                    legal_moves.append((self.position[0] + change_in_pos[0], self.position[1] + change_in_pos[1]))
                    change_in_pos[0] += basis_vector[0]
                    change_in_pos[1] += basis_vector[1]
                if (((0 <= self.position[0] + change_in_pos[0] < 8) and (0 <= self.position[1] + change_in_pos[1] < 8)) and 
                    ("black" not in self.squares[self.position[0] + change_in_pos[0]] [self.position[1] + change_in_pos[1]].type)):
                    legal_moves.append((self.position[0] + change_in_pos[0], self.position[1] + change_in_pos[1]))
                basis_vector = (-basis_vector[1], basis_vector[0])

        if self.type == 'white-bishop':
            basis_vector = (1,1)
            for j in range(4):
                change_in_pos = [basis_vector[0], basis_vector[1]]
                while ((0 <= self.position[0] + change_in_pos[0] < 8) and (0 <= self.position[1] + change_in_pos[1] < 8) and 
                       (self.squares[self.position[0] + change_in_pos[0]] [self.position[1] + change_in_pos[1]] == False)):
                    legal_moves.append((self.position[0] + change_in_pos[0], self.position[1] + change_in_pos[1]))
                    change_in_pos[0] += basis_vector[0]
                    change_in_pos[1] += basis_vector[1]
                if (((0 <= self.position[0] + change_in_pos[0] < 8) and (0 <= self.position[1] + change_in_pos[1] < 8)) and 
                    ("white" not in self.squares[self.position[0] + change_in_pos[0]] [self.position[1] + change_in_pos[1]].type)):
                    legal_moves.append((self.position[0] + change_in_pos[0], self.position[1] + change_in_pos[1]))
                basis_vector = (-basis_vector[1], basis_vector[0])

        if self.type == 'black-queen':
            basis_vector = (0,1)
            for j in range(4):
                change_in_pos = [basis_vector[0], basis_vector[1]]
                while ((0 <= self.position[0] + change_in_pos[0] < 8) and (0 <= self.position[1] + change_in_pos[1] < 8) and 
                       (self.squares[self.position[0] + change_in_pos[0]] [self.position[1] + change_in_pos[1]] == False)):
                    legal_moves.append((self.position[0] + change_in_pos[0], self.position[1] + change_in_pos[1]))
                    change_in_pos[0] += basis_vector[0]
                    change_in_pos[1] += basis_vector[1]
                if (((0 <= self.position[0] + change_in_pos[0] < 8) and (0 <= self.position[1] + change_in_pos[1] < 8)) and 
                    ("black" not in self.squares[self.position[0] + change_in_pos[0]] [self.position[1] + change_in_pos[1]].type)):
                    legal_moves.append((self.position[0] + change_in_pos[0], self.position[1] + change_in_pos[1]))
                basis_vector = (-basis_vector[1], basis_vector[0])
            basis_vector = (1,1)
            for j in range(4):
                change_in_pos = [basis_vector[0], basis_vector[1]]
                while ((0 <= self.position[0] + change_in_pos[0] < 8) and (0 <= self.position[1] + change_in_pos[1] < 8) and 
                       (self.squares[self.position[0] + change_in_pos[0]] [self.position[1] + change_in_pos[1]] == False)):
                    legal_moves.append((self.position[0] + change_in_pos[0], self.position[1] + change_in_pos[1]))
                    change_in_pos[0] += basis_vector[0]
                    change_in_pos[1] += basis_vector[1]
                if (((0 <= self.position[0] + change_in_pos[0] < 8) and (0 <= self.position[1] + change_in_pos[1] < 8)) and 
                    ("black" not in self.squares[self.position[0] + change_in_pos[0]] [self.position[1] + change_in_pos[1]].type)):
                    legal_moves.append((self.position[0] + change_in_pos[0], self.position[1] + change_in_pos[1]))
                basis_vector = (-basis_vector[1], basis_vector[0])

        if self.type == 'white-queen':
            basis_vector = (0,1)
            for j in range(4):
                change_in_pos = [basis_vector[0], basis_vector[1]]
                while ((0 <= self.position[0] + change_in_pos[0] < 8) and (0 <= self.position[1] + change_in_pos[1] < 8) and 
                       (self.squares[self.position[0] + change_in_pos[0]] [self.position[1] + change_in_pos[1]] == False)):
                    legal_moves.append((self.position[0] + change_in_pos[0], self.position[1] + change_in_pos[1]))
                    change_in_pos[0] += basis_vector[0]
                    change_in_pos[1] += basis_vector[1]
                if (((0 <= self.position[0] + change_in_pos[0] < 8) and (0 <= self.position[1] + change_in_pos[1] < 8)) and 
                    ("white" not in self.squares[self.position[0] + change_in_pos[0]] [self.position[1] + change_in_pos[1]].type)):
                    legal_moves.append((self.position[0] + change_in_pos[0], self.position[1] + change_in_pos[1]))
                basis_vector = (-basis_vector[1], basis_vector[0])
            basis_vector = (1,1)
            for j in range(4):
                change_in_pos = [basis_vector[0], basis_vector[1]]
                while ((0 <= self.position[0] + change_in_pos[0] < 8) and (0 <= self.position[1] + change_in_pos[1] < 8) and 
                       (self.squares[self.position[0] + change_in_pos[0]] [self.position[1] + change_in_pos[1]] == False)):
                    legal_moves.append((self.position[0] + change_in_pos[0], self.position[1] + change_in_pos[1]))
                    change_in_pos[0] += basis_vector[0]
                    change_in_pos[1] += basis_vector[1]
                if (((0 <= self.position[0] + change_in_pos[0] < 8) and (0 <= self.position[1] + change_in_pos[1] < 8)) and 
                    ("white" not in self.squares[self.position[0] + change_in_pos[0]] [self.position[1] + change_in_pos[1]].type)):
                    legal_moves.append((self.position[0] + change_in_pos[0], self.position[1] + change_in_pos[1]))
                basis_vector = (-basis_vector[1], basis_vector[0])

        if self.type == 'black-king':
            basis_vector = (0,1)
            for j in range(4):
                if ((0 <= self.position[0] + basis_vector[0] < 8) and (0 <= self.position[1] + basis_vector[1] < 8) and 
                       (self.squares[self.position[0] + basis_vector[0]] [self.position[1] + basis_vector[1]] == False)):
                    legal_moves.append((self.position[0] + basis_vector[0], self.position[1] + basis_vector[1]))
                elif (((0 <= self.position[0] + basis_vector[0] < 8) and (0 <= self.position[1] + basis_vector[1] < 8)) and 
                      ("black" not in self.squares[self.position[0] + basis_vector[0]] [self.position[1] + basis_vector[1]].type)):
                    legal_moves.append((self.position[0] + basis_vector[0], self.position[1] + basis_vector[1]))
                basis_vector = (-basis_vector[1], basis_vector[0])
            basis_vector = (1,1)
            for j in range(4):
                if ((0 <= self.position[0] + basis_vector[0] < 8) and (0 <= self.position[1] + basis_vector[1] < 8) and 
                       (self.squares[self.position[0] + basis_vector[0]] [self.position[1] + basis_vector[1]] == False)):
                    legal_moves.append((self.position[0] + basis_vector[0], self.position[1] + basis_vector[1]))
                elif (((0 <= self.position[0] + basis_vector[0] < 8) and (0 <= self.position[1] + basis_vector[1] < 8)) and 
                      ("black" not in self.squares[self.position[0] + basis_vector[0]] [self.position[1] + basis_vector[1]].type)):
                    legal_moves.append((self.position[0] + basis_vector[0], self.position[1] + basis_vector[1]))
                basis_vector = (-basis_vector[1], basis_vector[0])

        if self.type == 'white-king':
            basis_vector = (0,1)
            for j in range(4):
                if ((0 <= self.position[0] + basis_vector[0] < 8) and (0 <= self.position[1] + basis_vector[1] < 8) and 
                       (self.squares[self.position[0] + basis_vector[0]] [self.position[1] + basis_vector[1]] == False)):
                    legal_moves.append((self.position[0] + basis_vector[0], self.position[1] + basis_vector[1]))
                elif (((0 <= self.position[0] + basis_vector[0] < 8) and (0 <= self.position[1] + basis_vector[1] < 8)) and 
                      ("white" not in self.squares[self.position[0] + basis_vector[0]] [self.position[1] + basis_vector[1]].type)):
                    legal_moves.append((self.position[0] + basis_vector[0], self.position[1] + basis_vector[1]))
                basis_vector = (-basis_vector[1], basis_vector[0])
            basis_vector = (1,1)
            for j in range(4):
                if ((0 <= self.position[0] + basis_vector[0] < 8) and (0 <= self.position[1] + basis_vector[1] < 8) and 
                       (self.squares[self.position[0] + basis_vector[0]] [self.position[1] + basis_vector[1]] == False)):
                    legal_moves.append((self.position[0] + basis_vector[0], self.position[1] + basis_vector[1]))
                elif (((0 <= self.position[0] + basis_vector[0] < 8) and (0 <= self.position[1] + basis_vector[1] < 8)) and 
                      ("white" not in self.squares[self.position[0] + basis_vector[0]] [self.position[1] + basis_vector[1]].type)):
                    legal_moves.append((self.position[0] + basis_vector[0], self.position[1] + basis_vector[1]))
                basis_vector = (-basis_vector[1], basis_vector[0])
        return legal_moves