import tkinter as tk
from tkinter import messagebox
from typing import Optional
from a3_support import *

class Model():
    """
    Sets the gameplay for the game using a list of lists (matrix),
    including the ability to start a new game, attempt moves, and undo moves.
    """
    def __init__(self) -> None:
        """
        Sets the variables that store the current game state,
        previous states (for undo), score, and number of undos.
        """
        self._game = []
        self._previous_state = []
        self._score = 0
        self._undos = MAX_UNDOS
    
    def new_game(self) -> None:
        """
        Turns the state of the game to a matrix of empty tiles.
        It also resets the score and number of undos.
        
        This method must be executed before starting a game.
        """
        self._score = 0
        self._undos = MAX_UNDOS
        self._game = [[None for column in range(NUM_COLS)] \
            for row in range(NUM_ROWS)]
    
    def get_score(self) -> int:
        """
        Returns:
            int: Gets the current score of the game.
        """
        return self._score
    
    def get_tiles(self) -> list[list[Optional[int]]]:
        """
        Returns:
            list[list[Optional[int]]]: Gets the current list of
                lists (matrix) of the game.
        """
        return self._game
    
    def add_tile(self) -> None:
        """
        Adds a tile to the game (list of lists) if there is an empty tile in
        the game.
        
        The new generated tile is a randomized number of either 2 or 4.
        This is done using generate_tile() from a3_support.py.
        """
        
        # Get a list of empty tiles in the game using list comprehension.
        empty_tiles = [None for row in self._game if None in row]
        
        # Generates and adds a tile to the game if there are empty tiles.
        if len(empty_tiles) != 0:
            new_tile = generate_tile(self._game)
            (row, column), tile_number = new_tile
            self._game[row][column] = tile_number
    
    def move_left(self) -> None:
        """
        Moves all the game's tiles to the left using stack_left() and
        combine_left() from a3_support.
        
        It also adds to the current score of the game.
        """
        stacked_left = stack_left(self._game)
        merged_tiles, score = combine_left(stacked_left)
        self._game = stack_left(merged_tiles)
        self._score += score
        
    def move_right(self) -> None:
        """
        Moves all the game's tiles to the right by using 
        reverse() (from a3_support) and move_left().
        
        It also adds to the current score of the game.
        """
        self._game = reverse(self._game)
        self.move_left()
        self._game = reverse(self._game)
        
    
    def move_up(self) -> None:
        """
        Moves all the game's tiles up by using
        transpose() (from a3_support) and move_left().
        
        It also adds to the current score of the game.
        """
        self._game = transpose(self._game)
        self.move_left()
        self._game = transpose(self._game)
    
    def move_down(self) -> None:
        """
        Moves all the game's tiles down by using
        transpose() (from a3_support), and move_right().
        
        It also adds to the current score of the game.
        """
        self._game = transpose(self._game)
        self.move_right()
        self._game = transpose(self._game)
    
    def get_undos_remaining(self) -> int:
        """
        Returns:
            int: Gets the current number of undos remaining.
        """
        return self._undos
    
    def attempt_move(self, move: str) -> bool:
        """
        Attempts a move from "wasd" depending on the input.
        
        Available moves:
            "w" : Executes move_up()
            "a" : Executes move_left()
            "s" : Executes move_down()
            "d" : Executes move_right()
        
        It also adds the previous state of the game to self._previous_states
        to be able to undo the game if needed.

        Parameters:
            move (str): a key or move from "wasd".

        Returns:
            bool: True if the state of the game as changed, but
                False if the game has stayed the same after the move.
        """
        previous_state = self._game
        previous_score = self._score
        
        if move == "a":
            self.move_left()
        if move == "d":
            self.move_right()
        if move == "w":
            self.move_up()
        if move == "s":
            self.move_down()
        
        # Since the game can be undoed up to 3 times, the previous 3 states of
        # the game must be stored. Hence, each state is added 
        # to self._previous state.
        
        if previous_state != self._game:
            if len(self._previous_state) != MAX_UNDOS:
                self._previous_state.append((previous_state, previous_score))
            else:
                self._previous_state.pop(0)
                self._previous_state.append((previous_state, previous_score))
        
        
        return previous_state != self._game
    
    def use_undo(self) -> None:
        """
        Undos the previous move and reverts the game to its previous state.
        
        It also removes an undo from the number of undos remaining.
        """
        # The method does not undo if there are no undos remaining or if the
        # game is back to its initial state.
        if self._undos < 1 or len(self._previous_state) == 0:
            return
        
        # Stores the index of the previous move for self._previous_state.
        previous_game = len(self._previous_state)-1
        
        # Sets the current game and score to the previous state, and removes
        # the previous state from self._previous_state.
        self._game, self._score = self._previous_state.pop(previous_game)
        self._undos -= 1
    
    def has_won(self) -> bool:
        """
        The players has won if the game has a tile with 2048.

        Returns:
            bool: Returns True if there is a tile with 2048 in the game,
                but False if there is not.
        """
        # Appends to win_tile if the game has at least one 2048 tile
        # using list comprehension.
        win_tile = [2048 for row in self._game if 2048 in row]
        
        if len(win_tile) > 0:
            return True
        else:
            return False
    
    def has_lost(self) -> bool:
        """
        The players has lost if there are 0 empty tiles left and 
        a move does not result in a change in the game.

        Returns:
            bool: Returns True if the player has lost according to the
                conditions above, but False if the player has not lost.
        """
        # Stores the previous state of the game to check if any move can 
        # change the state of the game in the future.
        previous_state = self._game
        previous_score = self._score
        
        # Appends None to empty_tile if there are any empty tiles in the game.
        empty_tiles = [None for row in self._game if None in row]
        
        if len(empty_tiles) == 0:
            # Executes all 4 moves to see if any move can change the
            # state of the game.
            self.move_left()
            self.move_right()
            self.move_up()
            self.move_down()
            
            # Player has lost if the current game state is the same as the
            # previous game state. However, if it is different, then the 
            # game is reverted back to its state at the start of has_lost().
            
            if self._game == previous_state:
                return True
            else:
                self._game = previous_state
                self._score = previous_score
                return False
        else:
            return False


class GameGrid(tk.Canvas):
    """
    Sets the visual graphics of the game using tkinter,
    by inheriting tk.Canvas.
    """
    def __init__(self, master: tk.Tk, **kwargs) -> None:
        """
        Initialises the pixels size of the grid (400x400), and its
        background colour(from a3_support).

        Parameters:
            master (tk.Tk): The window in which game will be shown.
        """
        super().__init__(master,
        width=BOARD_WIDTH,
        height=BOARD_HEIGHT,
        bg=BACKGROUND_COLOUR,
        **kwargs)
        
    def _get_bbox(self, position: tuple[int, int]) \
        -> tuple[int, int, int, int]:
        """
        Gets the coordinates of the specified tile, based on the position of
        the tile in the game (list of lists), to be shown on the canvas.

        Parameters:
            position (tuple[int, int]): The indexed position of the tile in
                the form of [row, column].

        Returns:
            tuple[int, int, int, int]: The coordinates for the top left corner
                and bottom right corner for the tile to be shown on the canvas.
        """
        row, column = position
        return ((column*100)+(BUFFER-5), (row*100)+(BUFFER-5),
        ((column+1)*100)-(BUFFER-5), ((row+1)*100)-(BUFFER-5))
    
    def _get_midpoint(self, position: tuple[int, int]) -> tuple[int, int]:
        """
        Gets the midpoint of the specified tile, based on the position of
        the tile in the game (list of lists), to show the its label on
        the canvas.

        Parameters:
            position (tuple[int, int]): The indexed position of the tile in
                the form of [row, column].

        Returns:
            tuple[int, int]: The coordinates for the tile's label to be
            shown on the canvas.
        """
        row, column = position
        return ((column*100)+50, (row*100)+50)
    
    
    def clear(self) -> None:
        """
        Clears the entire canvas to draw the new state of the game.
        """
        self.delete("all")
    
    
    def redraw(self, tiles: list[list[Optional[int]]]) -> None:
        """
        Draws the current state of the game.
        
        It uses create_rectangle() to create the tile on the canvas,
        and create_text() to create the label for that tile.
        Both of these methods are inherited from tk.Canvas.

        Paramters:
            tiles (list[list[Optional[int]]]): The current state of the game,
                in the form of a list of lists.
        """
        self.clear() # Clears the canvas to draw the new state of the game.
        
        # Iterate through every tile in the game, and create a tile and 
        # label for it on the canvas based on its indexed position.
        # The colours and font are set based on a3_support.
        for row_index, row in enumerate(tiles):
            for tile_index, tile in enumerate(row):
                position = [row_index, tile_index]
                
                self.create_rectangle(
                    self._get_bbox(position),
                    fill=COLOURS.get(tile),
                    outline=BACKGROUND_COLOUR)
                
                if tile != None:
                    self.create_text(
                        self._get_midpoint(position),
                        text=str(tile),
                        font=TILE_FONT,
                        fill=FG_COLOURS.get(tile))

class StatusBar(tk.Frame):
    """
    Sets the frame for the status bar, which shows the current score,
    undos remaining, and provides capability for 'new game' and 'undo game'.
    
    Since StatusBar inherits tk.Frame, the StatusBar itself becomes a frame.
    """
    
    def __init__(self, master: tk.Tk, **kwargs) -> None:
        """
        Initialises the instances of frames within the statusbar, including
        the corresponding labels and buttons.
        
        It sets up the visuals for the backgrond of the statusbar, the score,
        undos remaining, and buttons for new game and undo game.

        Parameters:
            master (tk.Tk): The window in which game will be shown.
        """
        super().__init__(master,
        **kwargs)
        
        # Frames for Score, Undo, and Buttons.
        
        # Create frames for score, undo, and buttons and pack them to show
        # on the statusbar.
        
        self._score_frame = tk.Frame(
            self,
            bg=BACKGROUND_COLOUR)
        self._score_frame.pack(
            side=tk.LEFT,
            expand=True)
        
        self._undo_frame = tk.Frame(
            self,
            bg=BACKGROUND_COLOUR)
        self._undo_frame.pack(
            side=tk.LEFT,
            expand=True)
            
        self._button_frame = tk.Frame(
            self)
        self._button_frame.pack(
            side=tk.LEFT,
            expand=True,
            fill=tk.BOTH)
        
        
        # Score and Undo Labels
        
        # Creates the labels that read "SCORE" and "UNDOS" in the corresponding
        # frames and packs them.
        
        text = [["SCORE", self._score_frame], ["UNDOS", self._undo_frame]]
        for label_name, frame in text:
            tk.Label(
                frame,
                text=label_name,
                fg=COLOURS[None],
                bg=BACKGROUND_COLOUR,
                font=("Arial bold", 20)
            ).pack(
                expand=True)
        
        NUMBER_FONT = ("Arial bold", 15)
        
        # Current Score Label
        
        # Creates the score label that showcases the current score of the 
        # game, and packs it.
        self._score_number = tk.Label(
            self._score_frame,
            text="0",
            fg=LIGHT,
            bg=BACKGROUND_COLOUR,
            font=NUMBER_FONT)
        self._score_number.pack(
            expand=True)
        
        
        # Undos Remaining Label
        
        # Creates the undos remaining label that showcases the number 
        # of undos remaining and packs them.
        self._undo_number = tk.Label(
            self._undo_frame,
            text="3",
            fg=LIGHT,
            bg=BACKGROUND_COLOUR,
            font=NUMBER_FONT)
        self._undo_number.pack(expand=True)
        
        
        # Buttons for 'new game' and 'undo game'
        # The command for the buttons will be set in the Game() class.
        
        self._new_game = tk.Button(
            self._button_frame,
            text="New Game",
            command=None)
        self._new_game.pack(
            expand=True)
        
        self._undo_move = tk.Button(
            self._button_frame,
            text="Undo Move")
        self._undo_move.pack(
            expand=True)
    
    
    def redraw_infos(self, score: int, undos: int) -> None:
        """
        Updates the score and undos remaining with the current quantities.

        Parameters:
            score (int): The current score of the game.
            undos (int): The current number of undos remaining.
        """
        self._score_number.config(
            text=str(score))
        
        self._undo_number.config(
            text=str(undos))
    
    def set_callbacks(self, new_game_command: callable, \
        undo_command: callable) -> None:
        """
        Sets the commands for the 'new game' and 'undo game' buttons.
        
        This method will be used in the Game() class.

        Parameters:
            new_game_command (callable): The method to execute at the press
                of the 'new game' button.
            undo_command (callable): The method to execute at the press
                of the 'undo game' button.
        """
        self._new_game.config(
            command=new_game_command)
        
        self._undo_move.config(
            command=undo_command)


class Game():
    """
    Uses Model(), GameGrid(), and StatusBar() to coordinate the gameplay and
    show the visuals to the player.
    """
    
    def __init__(self, master: tk.Tk) -> None:
        """
        Initialises the game by creating an instance of Model(), GameGrid(),
        and StatusBar().
        
        It also sets the title of the window and the title_label of the game.

        Parameters:
            master (tk.Tk): The window in which game will be shown.
        """
        self._root = master
        self._game = Model() # Initialises the model of the game.
        self._root.title("CSSE1001/7030 2022 Semester 2 A3")
        
        # Creates the title_label that goes on top of the GameGrid()
        tk.Label(
            master,
            text="2048",
            bg=COLOURS.get(2048),
            fg="white",
            font=TITLE_FONT
        ).pack(
            fill=tk.X)
        
        # Initialises the visual aspects of the game.
        self._view = GameGrid(self._root)
        self._statusbar = StatusBar(self._root)
        
        # Sets the commands for the 'new game' and 'undo game' buttons.
        self._statusbar.set_callbacks(
            self.start_new_game,
            self.undo_previous_move)
        
        # Creates an grid with empty tiles and adds 2 tiles.
        self.start_new_game()
        
        # Makes a move based on the corresponding key press.
        # It also checks if player has won or lost, and adds a new tile to
        # the game.
        self._root.bind("<Key>", self.attempt_move)
        
        # This packs the current state of GameGrid and StatusBar to the window
        # whenever a move is attempted.
        self._view.pack()
        self._statusbar.pack(expand=True, fill=tk.BOTH)
        
    
    def draw(self) -> None:
        """
        Draws the current state of the game in the canvas within the window.
        Updates the label for score and undos remaining in StatusBar.
        """
        self._view.redraw(self._game.get_tiles())
        self._statusbar.redraw_infos(self._game.get_score(),
        self._game.get_undos_remaining())
    
    def message_box(self, message: str) -> None:
        """
        Shows a messagebox if the player has won or lost with the
        corresponding message.
        
        The 'yes' button in the messagebox starts a new game, and the
        'no' button closes the window.
        
        It uses the messagebox submodule from tkinter.

        Parameters:
            message (str): the message to show at either win or loss.
                It can either be WIN_MESSAGE or LOSS_MESSAGE from a3_support.
        """
        message_box = messagebox.askyesno(None, message)
        if message_box:
            self.start_new_game()
        else:
            self._root.destroy()
    
    def attempt_move(self, event: tk.Event) -> None:
        """
        Attempts a move based on the corresponding keypress, and redraws the
        new state of the game with draw().

        Parameters:
            event (tk.Event): the key press of the player.
        """
        if event.char not in "wasd":
            return
        
        self._game.attempt_move(event.char)
        self.draw()
        
        # A message box is displayed if the game has been won, but a new tile
        # is added to Model() and GameGrid() (after 150ms) if not won.
        if self._game.has_won():
            self.message_box(WIN_MESSAGE) # Opens the messagebox for a win.
        else:
            self._view.after(NEW_TILE_DELAY, self.new_tile)
    
    def new_tile(self) -> None:
        """
        Adds a new tile to Model() and GameGrid(), and new the current state
        of the game.
        
        It also displays a message box for a loss if the game has been lost
        after the addition of a new tile.
        """
        self._game.add_tile()
        self.draw()
        if self._game.has_lost():
            self.message_box(LOSS_MESSAGE) # Opens the messagebox for a loss.
    
    def undo_previous_move(self) -> None:
        """
        Undos the Model to its previous state and redraws the current state
        of the game.
        """
        self._game.use_undo()
        self.draw()
    
    def start_new_game(self) -> None:
        """
        Starts a new game by resetting Model to an empty grid, and redraws
        the new state of the game with two tiles to begin with.
        """
        self._game.new_game()
        self.draw()
        for num in range(2):
            self.new_tile()

def play_game(root: tk.Tk) -> None:
    """
    Executes Game(), which opens a window and coordinates the gameplay based
    on the corresponding visuals, buttons, and keypress.
    
    The player has won if there is a 2048 tile in the grid.
    The player has lost if the grid is full and no moves can change the state
    of the game.
    
    Valid Input Keypresses:
        "w" : Moves all tiles up.
        "a" : Moves all tiles left.
        "s" : Moves all tiles down.
        "d" : Moves all tiles right.
    
    Parameters:
        root (tk.Tk): The window in which the game is played.
    """
    Game(root)

if __name__ == '__main__':
    root = tk.Tk()
    play_game(root)
    root.mainloop()
