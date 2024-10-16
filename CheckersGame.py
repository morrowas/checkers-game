# Author: Ashley Morrow
# GitHub username: morrowas
# Date: 03/15/2023
# Description: Allows two players to play a game of Checkers.

class InvalidSquare(Exception):
    """Exception raised if a square location does not exist on the game board."""
    pass

class OutofTurn(Exception):
    """Exception raised if a player tries to make a move when it is not their turn."""
    pass

class InvalidPlayer(Exception):
    """Exception raised if a player not listed as one of the players of the game tries to make a game move."""
    pass

class Player:
    """
    An object that represents a player in the Checkers game. Initialized with the player's name and checker color.
    The Checkers object creates a Player object using its create_player method. The Checkers object will also use the
    Player object to determine the number of kings and triple kings the player has, as well as whether the player
    has won the game using the get_captured_pieces count. If the player has captured all their opponent's pieces, they
    have won the game.
    """

    def __init__(self, player_name, checker_color):
        self._player_name = player_name
        self._checker_color = checker_color
        self._king_count = 0
        self._triple_king_count = 0
        self._captured_pieces_count = 0

    def get_king_count(self):
        """Returns the number of king pieces that the player has."""
        return self._king_count

    def get_triple_king_count(self):
        """Returns the number of triple king pieces that the player has."""
        return self._triple_king_count

    def get_captured_pieces_count(self):
        """
        Returns the number of opponent pieces that this player has captured. The Checkers object and its game_winner
        method will use this method to determine if the player has won the game by capturing all 12 of their opponent's
        pieces.
        """
        return self._captured_pieces_count

    def add_captured_piece(self):
        """Adds one captured piece to the player's captured piece count."""
        self._captured_pieces_count += 1

    def get_checker_color(self):
        """Returns the checker color assigned to the player."""
        return self._checker_color

    def add_king(self):
        """Adds a king to the player's king count."""
        self._king_count += 1

    def add_triple_king(self):
        """Adds a triple king to the player's king count."""
        self._triple_king_count += 1

class Checkers:
    """
    Initializes a game of Checkers and its board. Allows users to create a player object with their name and piece
    color. Through the methods defined for this class, the player will be able to play the game by moving their
    checkers to different locations and capturing pieces. The board can be printed out so the players can visually
    see where their pieces are on the board. Players can also use a method to get information about a particular
    location on the board and what it contains. Two players are needed to play the game.
    """

    def __init__(self):
        self._player_name = None
        self._piece_color = None
        self._current_board = [
            [None, "White", None, "White", None, "White", None, "White"],
            ["White", None, "White", None, "White", None, "White", None],
            [None, "White", None, "White", None, "White", None, "White"],
        [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None],
        ["Black", None, "Black", None, "Black", None, "Black", None],
            [None, "Black", None, "Black", None, "Black", None, "Black"],
            ["Black", None, "Black", None, "Black", None, "Black", None]]
        self._players = {} #dictionary, key = player name, value = player object
        self._player_turn = "Black"

    def create_player(self, player_name, piece_color):
        """
        Takes the player's name and their piece color and returns a Player object with this information. Two player
        objects must be created for the game to work.
        """
        new_player = Player(player_name, piece_color)
        self._players[player_name] = new_player
        return new_player

    def check_for_move_triple_king(self, row, column, checker_color, row_direction, column_direction):
        """Checks to see if any moves are possible within one diagonal direction for a triple king piece. Called by
        moves_to_check_triple_king function. Uses a recursive call if the first square in the
        diagonal entered in the function is empty."""
        if row > 7 or row < 0:
            return False
        elif row+row_direction > 7 or row+row_direction < 0 or column+column_direction > 7 or column+column_direction\
            < 0:
            return False
        elif checker_color == self._current_board[row+row_direction][column+column_direction]:
            return False
        elif self._current_board[row+row_direction][column+column_direction] is None:
            return self.check_for_move_triple_king(row+row_direction, column+column_direction, checker_color, \
                                                     row_direction, column_direction)
        elif row+row_direction+row_direction > 7 or row+row_direction+row_direction < 0 or \
                column+column_direction+column_direction > 7 or column+column_direction+column_direction < 0:
            return False
        else:
            if self._current_board[row+row_direction+row_direction][column+column_direction+column_direction] is None:
                return True
            elif self._current_board[row+row_direction+row_direction][column+column_direction+column_direction] is not\
                None:
                if self._current_board[row+row_direction+row_direction][column+column_direction+column_direction] ==\
                    checker_color:
                    return False
                else:
                    if row+row_direction+row_direction+row_direction > 7 or \
                            row+row_direction+row_direction+row_direction < 0 or \
                            column+column_direction+column_direction+column_direction > 7 or \
                            column+column_direction+column_direction+column_direction < 0:
                        return False
                    elif self._current_board[row+row_direction+row_direction+row_direction]\
                        [column+column_direction+column_direction+column_direction] is None:
                        return True
                    else:
                        return False

    def moves_to_check_triple_king(self, checker_color, destination_row, destination_column):
        """Checks to see if a move is possible for a triple king piece."""
        possible_move_up_right = self.check_for_move_triple_king(destination_row, destination_column, checker_color,\
                                                                  -1, 1)
        possible_move_up_left = self.check_for_move_triple_king(destination_row, destination_column, checker_color,\
                                                                 -1, -1)
        possible_move_down_right = self.check_for_move_triple_king(destination_row, destination_column, \
                                                                checker_color, 1, 1)
        possible_move_down_left = self.check_for_move_triple_king(destination_row, destination_column, checker_color,\
                                                               1, -1)
        if possible_move_up_right == True or possible_move_up_left == True or possible_move_down_right == True or\
                possible_move_down_left == True:
            return True
        else:
            return False
    def check_for_possible_move_king(self, row, column, checker_color, row_direction, column_direction):
        """Checks to see if any moves are possible within one diagonal direction for a king piece. Called by
        possible_moves_to_check_king function. Uses a recursive call if the space in the first square in the
        diagonal entered in the function is empty."""
        if row > 7 or row < 0:
            return False
        elif row+row_direction > 7 or row+row_direction < 0 or column+column_direction > 7 or column+column_direction\
            < 0:
            return False
        elif checker_color == self._current_board[row+row_direction][column+column_direction]:
            return False
        elif self._current_board[row+row_direction][column+column_direction] is None:
            return self.check_for_possible_move_king(row+row_direction, column+column_direction, checker_color, \
                                                     row_direction, column_direction)
        elif row+row_direction+row_direction > 7 or row+row_direction+row_direction < 0 or \
                column+column_direction+column_direction > 7 or column+column_direction+column_direction < 0:
            return False
        else:
            if self._current_board[row+row_direction+row_direction][column+column_direction+column_direction] is None:
                return True
            else:
                return False

    def possible_moves_to_check_king(self, checker_color, destination_row, destination_column):
        """Checks to see if a move is possible for a king piece."""
        possible_move_up_right = self.check_for_possible_move_king(destination_row, destination_column, checker_color,\
                                                                  -1, 1)
        possible_move_up_left = self.check_for_possible_move_king(destination_row, destination_column, checker_color,\
                                                                 -1, -1)
        possible_move_down_right = self.check_for_possible_move_king(destination_row, destination_column, \
                                                                checker_color, 1, 1)
        possible_move_down_left = self.check_for_possible_move_king(destination_row, destination_column, checker_color,\
                                                               1, -1)
        if possible_move_up_right == True or possible_move_up_left == True or possible_move_down_right == True or\
                possible_move_down_left == True:
            return True
        else:
            return False


    def check_for_possible_move(self, row, column, checker_color, row_direction, column_direction):
        """Checks to see if any moves are possible within one diagonal direction for a standard piece."""
        if row > 7 or row < 0:
            return False
        elif row+row_direction > 7 or row+row_direction < 0 or column+column_direction > 7 or column+column_direction\
            < 0:
            return False
        elif checker_color == self._current_board[row+row_direction][column+column_direction]:
            return False
        elif self._current_board[row+row_direction][column+column_direction] is None:
            return False
        elif row+row_direction+row_direction > 7 or row+row_direction+row_direction < 0 or \
                column+column_direction+column_direction > 7 or column+column_direction+column_direction < 0:
            return False
        else:
            if self._current_board[row+row_direction+row_direction][column+column_direction+column_direction] is None:
                return True
            else:
                return False

    def possible_moves_to_check(self, checker_color, destination_row, destination_column):
        """Takes a piece color as a parameter and calls the check_for_possible_move functions needed to determine
        if the player can make a move. This function only applies to standard pieces, not kings or triple kings, so
        the function only checks for possible forward moves."""
        if checker_color == "Black":
            possible_move_up_right = self.check_for_possible_move(destination_row, destination_column, checker_color,\
                                                                  -1, 1)
            possible_move_up_left = self.check_for_possible_move(destination_row, destination_column, checker_color,\
                                                                 -1, -1)
            if possible_move_up_right == True or possible_move_up_left == True:
                return True
            else:
                return False
        else:
            possible_move_down_right = self.check_for_possible_move(destination_row, destination_column, checker_color,\
                                                                    1, 1)
            possible_move_down_left = self.check_for_possible_move(destination_row, destination_column, checker_color,\
                                                                   1, -1)
            if possible_move_down_right == True or possible_move_down_left == True:
                return True
            else:
                return False

    def play_game(self, player_name, starting_square_location, destination_square_location):
        """
        The player calls this method to make a move in the game. The player inputs their name, the location of the
        piece that they want to move, and the location they want to move that piece to. Will raise an exception if
        the player attempts to move a piece out of turn, move a piece that is not theirs, move a piece to a square
        that does not exist, or if the player's name is not valid. Returns the number of pieces captured with this
        move. If the piece reaches the end of the opponent's side it becomes a king, and if it then reaches the player's
        original side it becomes a triple king.
        """

        starting_row = starting_square_location[0]
        starting_column = starting_square_location[1]
        destination_row = destination_square_location[0]
        destination_column = destination_square_location[1]
        checker_color = self._players[player_name].get_checker_color() #Holds current player's checker color
        captured_pieces_this_turn = 0

        #Exception Tests
        if starting_row < 0 or starting_column < 0 or destination_row < 0 or destination_column < 0:
            raise InvalidSquare
        if starting_row > 7 or starting_column > 7 or destination_row > 7 or destination_column > 7:
            raise InvalidSquare
        elif checker_color != self._player_turn:
            raise OutofTurn
        elif checker_color == "Black":
            if self._current_board[starting_row][starting_column] != "Black" and \
                    self._current_board[starting_row][starting_column] != "Black_king" and \
                    self._current_board[starting_row][starting_column] != "Black_Triple_King":
                raise InvalidSquare
        elif checker_color == "White":
            if self._current_board[starting_row][starting_column] != "White" and \
                    self._current_board[starting_row][starting_column] != "White_king" and \
                    self._current_board[starting_row][starting_column] != "White_Triple_King":
                raise InvalidSquare
        elif self._current_board[starting_row][starting_column] == None:
            raise InvalidSquare

        #Setting piece equal to piece at starting location, then moving that piece
        piece = self._current_board[starting_row][starting_column]
        self.move_piece(piece, starting_row, starting_column, destination_row, destination_column)

        #Determining if a piece has been captured
        if piece == "Black_king" or piece == "White_king":
            captured_pieces_this_turn += self.capture_piece_king(player_name, checker_color, starting_row, \
                                                                 starting_column, destination_row, destination_column)
        elif piece == "Black_Triple_King" or piece == "White_Triple_King":
            captured_pieces_this_turn += self.capture_piece_triple_king(player_name, checker_color, starting_row,\
                                                                   starting_column, destination_row, destination_column)
        else:
            if starting_row - destination_row == -2:
                if starting_column - destination_column == 2: #Jump down & left
                    self._players[player_name].add_captured_piece()
                    captured_pieces_this_turn += 1
                    self._current_board[starting_row+1][starting_column-1] = None
                elif starting_column - destination_column == -2: #Jump down & right
                    self._players[player_name].add_captured_piece()
                    captured_pieces_this_turn += 1
                    self._current_board[starting_row+1][starting_column+1] = None
            elif starting_row - destination_row == 2:
                if starting_column - destination_column == 2: #Jump up & left
                    self._players[player_name].add_captured_piece()
                    captured_pieces_this_turn += 1
                    self._current_board[starting_row-1][starting_column-1] = None
                elif starting_column - destination_column == -2: #Jump up & right
                    self._players[player_name].add_captured_piece()
                    captured_pieces_this_turn += 1
                    self._current_board[starting_row-1][starting_column+1] = None

        #Checks for possible moves, True returned if a move is possible, otherwise False
        if piece == "Black" or piece == "White":
            moves_possible = self.possible_moves_to_check(checker_color, destination_row, destination_column)
        elif piece == "Black_king" or piece == "White_king":
            moves_possible = self.possible_moves_to_check_king(checker_color, destination_row, destination_column)
        else:
            moves_possible = self.moves_to_check_triple_king(checker_color, destination_row, destination_column)


        if moves_possible == True:
            if captured_pieces_this_turn == 1:
                pass
            else:
                if self._player_turn == "Black":
                    self._player_turn = "White"
                else:
                    self._player_turn = "Black"
        elif moves_possible == False:
            if self._player_turn == "Black":
                self._player_turn = "White"
            else:
                self._player_turn = "Black"

        #If conditions are met, changes a piece to a king or triple king, important that this is last!
        if checker_color == "White" and destination_row == 7:
            self._current_board[destination_row][destination_column] = "White_king"
            self._players[player_name].add_king()
        elif checker_color == "Black" and destination_row == 0:
            self._current_board[destination_row][destination_column] = "Black_king"
            self._players[player_name].add_king()
        elif self._current_board[destination_row][destination_column] == "White_king" and \
            destination_row == 0:
            self._current_board[destination_row][destination_column] = "White_Triple_King"
            self._players[player_name].add_triple_king()
        elif self._current_board[destination_row][destination_column] == "Black_king" and \
                 destination_row == 7:
            self._current_board[destination_row][destination_column] = "Black_Triple_King"
            self._players[player_name].add_triple_king()

        return captured_pieces_this_turn

    def get_checker_details(self, square_location):
        """
        Takes a square location as a parameter and returns the details of the checker present in that location.
        If no piece is in the input square, returns None. Raises an exception if the input square location is not
        on the board. Otherwise, returns the color of the piece on the board, and whether it is a standard piece, king
        or triple king.
        """
        board_row = square_location[0]
        board_column = square_location[1]

        if board_row > 7:
            raise InvalidSquare
        elif board_column > 7:
            raise InvalidSquare
        else:
            return self._current_board[board_row][board_column]
    def print_board(self):
        """Prints the current board in the form of an array."""
        for element in self._current_board:
            print(element)

    def game_winner(self):
        """
        Returns the name of the player who won the game. If the game has not ended, returns message "game has not
        ended." Determines if a player has won the game by counting the number of their opponent's pieces they have
        using the get_captured_pieces_count method from the Player object.
        """
        game_over = False
        winner_of_game = None
        for player in self._players:
            if self._players[player].get_captured_pieces_count() == 12:
                game_over = True
                winner_of_game = player
        if game_over is True:
            return winner_of_game
        else:
            return "Game has not ended"


    def move_piece(self, piece, starting_row, starting_column, destination_row, destination_column):
        """
        Moves a piece from its starting location to destination. Takes the piece name (as a string), plus the starting
        row and column and ending row and column of the move as parameters.
        """
        self._current_board[starting_row][starting_column] = None  # Sets starting square to None
        self._current_board[destination_row][destination_column] = piece

    def capture_piece_king(self, player_name, checker_color, starting_row, starting_column, destination_row, \
                           destination_column):
        """
        Captures a piece based on the rules for a king piece, and changes the square of the captured piece
        to None.
        """
        if checker_color == "White":
            opponent_color = "Black"
        else:
            opponent_color = "White"

        if starting_row - destination_row <= -2:
            if starting_column - destination_column >= 2:  # Jump down & left
                self._players[player_name].add_captured_piece()
                self.remove_piece_king(opponent_color, starting_row, starting_column, 1, -1)
                return 1
            elif starting_column - destination_column <= -2:  # Jump down & right
                self._players[player_name].add_captured_piece()
                self.remove_piece_king(opponent_color, starting_row, starting_column, 1, 1)
                return 1
        elif starting_row - destination_row >= 2:
            if starting_column - destination_column >= 2:  # Jump up & left
                self._players[player_name].add_captured_piece()
                self.remove_piece_king(opponent_color, starting_row, starting_column, -1, -1)
                return 1
            elif starting_column - destination_column <= -2:  # Jump up & right
                self._players[player_name].add_captured_piece()
                self.remove_piece_king(opponent_color, starting_row, starting_column, -1, 1)
                return 1
        else:
            return 0

    def remove_piece_king(self, opponent_color, starting_row, starting_column, row_direction, column_direction):
        """Finds the piece to remove for king pieces, after it has been captured by the king."""
        if self._current_board[starting_row+row_direction][starting_column+column_direction] == opponent_color:
            self._current_board[starting_row + row_direction][starting_column + column_direction] = None
            return
        else:
            self.remove_piece_king(opponent_color, starting_row+row_direction, starting_column+column_direction, \
                              row_direction, column_direction)

    def capture_piece_triple_king(self, player_name, checker_color, starting_row, starting_column, destination_row, \
                           destination_column):
        """
        Captures one or two pieces based on the rules for a triple king piece, and changes the square of the captured
        piece(s) to None.
        """
        pieces_captured = 0
        if checker_color == "White":
            opponent_color = "Black"
        else:
            opponent_color = "White"

        if starting_row - destination_row <= -2:
            if starting_column - destination_column >= 2:  # Jump down & left
                pieces_captured = self.remove_two_pieces(player_name, opponent_color, starting_row, starting_column,\
                                                         1, -1)
                return pieces_captured
            elif starting_column - destination_column <= -2:  # Jump down & right
                pieces_captured = self.remove_two_pieces(player_name, opponent_color, starting_row, starting_column,\
                                                         1, 1)
                return pieces_captured
        elif starting_row - destination_row >= 2:
            if starting_column - destination_column >= 2:  # Jump up & left
                pieces_captured = self.remove_two_pieces(player_name, opponent_color, starting_row, starting_column,\
                                                         -1, -1)
                return pieces_captured
            elif starting_column - destination_column <= -2:  # Jump up & right
                pieces_captured = self.remove_two_pieces(player_name, opponent_color, starting_row, starting_column,\
                                                         -1, 1)
                return pieces_captured
        else:
            return 0

    def remove_two_pieces(self, player_name, opponent_color, starting_row, starting_column, row_direction, \
                          column_direction):
        """
        Checks to see if a triple king has captured two pieces in one move. If so, removes both pieces from the
        game board.
        """
        if self._current_board[starting_row+row_direction][starting_column+column_direction] == opponent_color:
            if self._current_board[starting_row+row_direction+row_direction]\
                    [starting_column+column_direction+column_direction] == opponent_color:
                self._current_board[starting_row+row_direction][starting_column+column_direction] = None
                self._current_board[starting_row+row_direction+row_direction]\
                    [starting_column+column_direction+column_direction] = None
                self._players[player_name].add_captured_piece()
                self._players[player_name].add_captured_piece()
                return 2
            else:
                self._current_board[starting_row + row_direction][starting_column + column_direction] = None
                self._players[player_name].add_captured_piece()
            return 1
        else:
            self.remove_piece_king(player_name, opponent_color, starting_row+row_direction, \
                                   starting_column+column_direction, row_direction, column_direction)

#def main():
    #"""Runs the below code when called by this file only."""
    #game = Checkers()
    #game.create_player("Ashley", "Black")
    #game.create_player("Tiffany", "White")
    #print(game.get_checker_details((7,4)))
    #print(game.play_game("Ashley", (5,0), (4,1)))
    #print(game.play_game("Tiffany", (2,1), (3,2)))
    #print(game.play_game("Ashley", (4,1), (3,0)))
    #print(game.play_game("Tiffany", (1,0), (2,1)))
    #print(game.play_game("Ashley", (5,6), (4,7)))
    #print(game.play_game("Tiffany", (3,2), (4,3)))
    #print(game.play_game("Ashley", (5,4), (3,2)))
    #print(game.play_game("Ashley", (3,2), (1,0)))
    #print(game.play_game("Tiffany", (1,2), (2,1)))
    #print(game.play_game("Ashley", (3,0), (1,2)))
    #print(game.play_game("Tiffany", (0,3), (2,1)))
    #print(game.play_game("Ashley", (5,2), (4,3)))
    #print(game.play_game("Tiffany", (0,1), (1,2)))
    #print(game.play_game("Ashley", (1,0), (0,1)))
    #print(game.play_game("Tiffany", (2,1), (3,0)))
    #print(game.play_game("Ashley", (6,1), (5,2)))
    #print(game.play_game("Tiffany", (1,2), (2,1)))
    #print(game.play_game("Ashley", (0,1), (3,4)))
    #print(game.play_game("Tiffany", (2,1), (3,2)))
    #print(game.play_game("Ashley", (4,3), (2,1)))
    #print(game.play_game("Tiffany", (2,7), (3,6)))
    #print(game.play_game("Ashley", (3,4), (4,3)))
    #print(game.play_game("Tiffany", (1,6), (2,7)))
    #print(game.play_game("Ashley", (2,1), (1,0)))
    #print(game.play_game("Tiffany", (0,5), (1,6)))
    #print(game.play_game("Ashley", (1,0), (0,1)))
    #print(game.play_game("Tiffany", (3,6), (4,5)))
    #print(game.play_game("Ashley", (0,1), (5,6)))
    #print(game.play_game("Tiffany", (2,7), (3,6)))
    #print(game.play_game("Ashley", (6,5), (5,4)))
    #print(game.play_game("Tiffany", (3,6), (4,5)))
    #print(game.play_game("Ashley", (5,4), (3,6)))
    #print(game.play_game("Tiffany", (1,6), (2,7)))
    #print(game.play_game("Ashley", (4,3), (1,6)))
    #print(game.play_game("Tiffany", (0,7), (2,5)))
    #print(game.play_game("Ashley", (5,6), (6,5)))
    #print(game.play_game("Tiffany", (2,5), (3,4)))
    #print(game.play_game("Ashley", (6,7), (5,6)))
    #print(game.play_game("Tiffany", (2,7), (4,5)))
    #print(game.play_game("Tiffany", (4,5), (6,7)))
    #print(game.play_game("Ashley", (6,3), (5,4)))
    #print(game.play_game("Tiffany", (1,4), (2,5)))
    #print(game.play_game("Ashley", (7,4), (6,3)))
    #print(game.play_game("Tiffany", (2,5), (3,6)))
    #print(game.play_game("Ashley", (4,7), (2,5)))
    #print(game.play_game("Tiffany", (3,4), (4,3)))
    #print(game.play_game("Ashley", (6,5), (7,4)))
    #print(game.play_game("Tiffany", (4,3), (6,5)))
    #print(game.play_game("Ashley", (5,2), (4,3)))
    #print(game.play_game("Tiffany", (6,7), (5,6)))
    #print(game.play_game("Ashley", (7,4), (4,7)))
    #print(game.play_game("Tiffany", (3,0), (4,1)))
    #print(game.play_game("Ashley", (7,0), (6,1)))
    #print(game.play_game("Tiffany", (4,1), (5,2)))
    #print(game.play_game("Ashley", (6,3), (4,1)))
    #game.print_board()
    #print(game.game_winner())

#if __name__ == '__main__':
    #main()