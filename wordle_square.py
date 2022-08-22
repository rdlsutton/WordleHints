# wordle_square.py
from graphics import *
import constants

class WordleSquare:
    """A class that represents a letter square in the Wordle puzzle."""
    
    # Define the row and column location of the square
    def __init__(self, row, column):
        self.x = constants.wordle_margin_x + \
                        column * constants.square_size + \
                        column * constants.squares_margin
        self.y = constants.wordle_margin_y + \
                        row * constants.square_size + \
                        row * constants.squares_margin
        self.right_x = self.x + constants.square_size
        self.bottom_y = self.y + constants.square_size
        self.letter = ''
        self.color = 'white'
    
    def draw(self, win):
        """Draw the square on the main window."""
        
        square = Rectangle(Point(self.x, self.y),
                        Point(self.right_x, self.bottom_y))
        square.draw(win)
    
        
    def set_letter(self, win, letter):
        """Set the letter inside the square to a value that is determined
        by the guess processing algorithm."""
        
        self.letter  = letter
        text = Text(Point(self.x + constants.square_text_x,
                        self.y + constants.square_text_y), letter)
        text.setSize(12)
        text.draw(win)
        
                
    def is_clicked(self, point):
        """Determine if the mouse click was within this wordle square."""
        
        if point.x > self.x and point.x < self.right_x:
            if point.y > self.y and point.y < self.bottom_y:
                return True
            else:
                return False
        else:
            return False
            

    def set_color(self, win, new_color):
        """Set the color of the square based on which results button is
            currently active."""
        
        # Redraw the square with the new coloer
        square = Rectangle(Point(self.x, self.y),
                        Point(self.right_x, self.bottom_y))
        if new_color == 'gray':
            square.setFill(color_rgb(211, 211, 211))
            self.color = 'gray'
        if new_color == 'beige':
            square.setFill(color_rgb(252, 186, 3))
            self.color = 'beige'
        if new_color == 'green':
            square.setFill(color_rgb(3, 250, 120))
            self.color = 'green'
        square.draw(win)
        
        # Redraw any letter that was in the square
        if self.letter != '':
            text = Text(Point(self.x + constants.square_text_x,
                        self.y + constants.square_text_y), self.letter)
            text.setSize(12)
            text.draw(win)
 
            
    def set_text_mode(self, win):
        """Set the square to text entry mode so the user can set their 
        own guess."""
        
        if self.color == 'white':
            square = Rectangle(Point(self.x, self.y),
                        Point(self.right_x, self.bottom_y))
            square.setFill(color_rgb(255, 255, 255))
            square.draw(win)
            self.letter = '_'
            text = Text(Point(self.x + constants.square_text_x,
                            self.y + constants.square_text_y), '_')
            text.setSize(12)
            text.draw(win)
        
        
    def enter_letter(self, win, letter):
        """When the user enters a valid letter into a text entry square
        set the square's letter to the entered letter and redraw."""
        
        square = Rectangle(Point(self.x, self.y),
                        Point(self.right_x, self.bottom_y))
        square.setFill(color_rgb(255, 255, 255))
        self.color = 'white'
        square.draw(win)
        self.letter = letter
        text = Text(Point(self.x + constants.square_text_x, self.y + \
                                  constants.square_text_y), self.letter)
        text.setSize(12)
        text.draw(win)
            
