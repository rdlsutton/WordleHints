# button.py
from graphics import *
import constants


class Button:
    """A class that creates a menu option button and allows it to be
    drawn on the screen."""
    
    # Define the locations for drawing the menu buttons
    def __init__(self, type):
        self.type = type
        if self.type == 'text':
            self.x = constants.button_margin
            self.y = constants.button_y
            self.right_x = constants.button_margin + \
                        constants.button_width
            self.bottom_y = constants.button_y + \
                        constants.button_height
        if self.type == 'gray':
            self.x = constants.button_margin * 2 + constants.button_width
            self.y = constants.button_y
            self.right_x = constants.button_margin * 2 + \
                        constants.button_width * 2
            self.bottom_y = constants.button_y + \
                        constants.button_height
        if self.type == 'beige':
            self.x = constants.button_margin * 3 + \
                    constants.button_width * 2
            self.y = constants.button_y
            self.right_x = constants.button_margin * 3 + \
                        constants.button_width * 3
            self.bottom_y = constants.button_y + \
                        constants.button_height
        if self.type == 'green':
            self.x = constants.button_margin * 4 + \
                    constants.button_width * 3
            self.y = constants.button_y
            self.right_x = constants.button_margin * 4 + \
                        constants.button_width * 4
            self.bottom_y = constants.button_y + \
                        constants.button_height
                    

    def draw(self, win):
        """Draw a selected button on the main window."""
                       
        # Draw the outer menu option border
        rect = Rectangle(Point(self.x, self.y), Point(self.right_x,
                        self.bottom_y))
        if self.type == 'text':
            rect.setFill(color_rgb(255, 255, 255))
            rect.draw(win)
            text = Text(Point(constants.button_margin + \
                        constants.button_text_x,
                        constants.button_y + constants.button_text_y),
                        'abc')
            text.setSize(10)
            text.draw(win)
        if self.type == 'gray':
            rect.setFill(color_rgb(211, 211, 211))
            rect.draw(win)
        if self.type == 'beige':
            rect.setFill(color_rgb(252, 186, 3))
            rect.draw(win)
        if self.type == 'green':
            rect.setFill(color_rgb(3, 250, 120))
            rect.draw(win)
        
        
    def activate(self, win):
        """Draw a border around the button to indicate it is active."""
        
        border_factor = 1
        
        # Draw additional borders in order to present a thicker looking
        # menu option border when the option is active
        for count in range(1, 3):
            rect = Rectangle(Point(self.x + border_factor * count,
                        self.y + border_factor * count),
                        Point(self.right_x - border_factor * count,
                        self.bottom_y - border_factor * count))
            rect.draw(win)


    def deactivate(self, win):
        """Draw the original rectangle so the button no longer appears
            to be active."""
        
        # Draw the original rectangle
        self.draw(win)
        
    
    def is_clicked(self, point):
        """Determine if the mouse click was within this menu option."""
        
        if point.x > self.x and point.x < self.right_x:
            if point.y > self.y and point.y < self.bottom_y:
                return True
            else:
                return False
        else:
            return False
