# WordleHints.py
from graphics import *
import constants
from button import Button
from wordle_square import WordleSquare


# Create a window to show the Wordle puzzle
win = GraphWin(width = constants.window_width,
               height = constants.window_height)

# Create a dictionary to store the five letter words
dictionary = []

# Set up a list of the Wordle squares
wordle_squares = []

# Set up a list of the results buttons
results_buttons = []

# Declare a variable to track which color is currently active
results_mode = 'gray'

# Declare a variable to track the last row that is filled with letters
last_row_filled = 1

# Set up two working lists to be used in paring down the words that
# are eligible to be the next guess
working_list_one = []
working_list_two = []

# Declare a variable to track which list is the current working list
current_list = 'initial'

# Track which columns have green squares so that other rules are not
# processed on those columns
non_green_columns = [0, 1, 2, 3, 4]

def import_dictionary():
    """Import the five letter word dictionary from the text file."""
    
    # Open the wordle_dict file and import the five letter words
    with open("wordle_dict.txt", "r") as input_file:
        lines = input_file.readlines()
        for line in lines:
            words = line.split(",")
            for word in words:
                dictionary.append(word)
    input_file.close()
    

def draw_top_label():
    """ Draw the word Wordle at the top of the main screen."""
    
    label_text = 'Wordle'
    text = Text(Point(constants.top_label_x, constants.top_label_y),
                label_text)
    text.setSize(12)
    text.draw(win)


def draw_wordle_squares():
    """Draw the five columns by six rows of squares for the Wordle
    letters."""
       
    for row in range(0, 6):
        for column in range(0, 5):
            wordle_square = WordleSquare(row, column)
            wordle_square.draw(win)
            wordle_squares.append(wordle_square)
            

def draw_results_label():
    """ Draw the Wordle Results label at the bottom of the main screen."""
    
    label_text = 'Wordle Results'
    text = Text(Point(constants.results_label_x,
                      constants.results_label_y), label_text)
    text.setSize(12)
    text.draw(win)
    

def draw_results_buttons():
    """ Draw the Wordle Results buttons at the bottom of the main
    screen."""
    
    results_button = Button('text')
    results_button.draw(win)
    results_buttons.append(results_button)
    results_button = Button('gray')
    results_button.draw(win)
    results_button.activate(win)
    results_buttons.append(results_button)
    results_button = Button('beige')
    results_button.draw(win)
    results_buttons.append(results_button)
    results_button = Button('green')
    results_button.draw(win)
    results_buttons.append(results_button)
    

def enter_first_guess(wordle_squares):
    """Fill the first row of letter squares with the first quess."""
    
    wordle_squares[0].set_letter(win, 'C')
    wordle_squares[1].set_letter(win, 'R')
    wordle_squares[2].set_letter(win, 'A')
    wordle_squares[3].set_letter(win, 'N')
    wordle_squares[4].set_letter(win, 'E')
    

def determine_if_last_row_complete():
    """Determine if the last row that has been filled with letters has
    all of its squares turned to one of the three colors. If so, it is
    time to generate the next guess."""
    
    first_square = (last_row_filled - 1) * 5
    if wordle_squares[first_square].color != 'white':
        if wordle_squares[first_square + 1].color != 'white':
            if wordle_squares[first_square + 2].color != 'white':
                if wordle_squares[first_square + 3].color != 'white':
                    if wordle_squares[first_square + 4].color != 'white':
                        return True
    return False
    

def process_green_squares():
    """For each green square the rule is, only words that contain that
    letter in that location are eligible to be a next guess. Walk through
    the current working dictionaries to eliminate words that are no
    longer eligible."""
    
    # Use the global variables instead of local ones
    global current_list
    global working_list_one
    global working_list_two
    
    square_count = -1
    for square in wordle_squares:
        square_count = square_count + 1
        if square.color == 'green':
            
            # Determine the column location of the current square
            column = square_count
            while column - 5 >= 0:
                column = column - 5
            
            # Add this column to the list of columns with green squares
            # so other rules are not processed on those columns
            if column in non_green_columns:
                non_green_columns.remove(column)
            
            # Determine the eligibility of each word in the dictionary
            if current_list == 'initial':
                for word in dictionary:
                    letters = [c for c in word]
                    if letters[column] == square.letter:
                        working_list_one.append(word)
                current_list = 'working_one'
                working_list_two = []
            elif current_list == 'working_one':
                for word in working_list_one:
                    letters = [c for c in word]
                    if letters[column] == square.letter:
                        working_list_two.append(word)
                current_list = 'working_two'
                working_list_one = []
            else:
                for word in working_list_two:
                    letters = [c for c in word]
                    if letters[column] == square.letter:
                        working_list_one.append(word)
                current_list = 'working_one'
                working_list_two = []


def process_list_for_beige(square_count, letter, working_list,
                           append_list):
    """Walk through the passed in working list to determine the
    eligibility of each word according to the beige squares rule."""
    
    # Determine the column location of the current square
    column = square_count
    while column - 5 >= 0:
        column = column - 5
                
    # For each word in the current working list, determine if it is still
    # eligible for the next guess
    for word in working_list:
        letters = [c for c in word]
        word_valid = True
        
        # Beige means that, the word must not have that letter in that
        # position
        if letters[column] == letter:
            word_valid = False
        else:
            
            # Determine if the letter is present in the other columng
            # positions
            columns = []
            for count in range(0, 5):
                if count != column:
                    columns.append(count)
            if letters[columns[0]] != letter and \
                    letters[columns[1]] != letter and \
                    letters[columns[2]] != letter and \
                    letters[columns[3]] != letter:
                word_valid = False
            if word_valid:
                append_list.append(word)               


def process_beige_squares():
    """For each beige square the rule is, only words that do contain
    that letter, but in a different location, are eligible to be a next
    guess."""
    
    # Use the global variables instead of local ones
    global current_list
    global working_list_one
    global working_list_two
    
    square_count = -1
    for square in wordle_squares:
        square_count = square_count + 1
        if square.color == 'beige':
            
            # Apply the eligibility rules to each remaining word
            if current_list == 'initial':
                process_list_for_beige(square_count, square.letter,
                                       dictionary, working_list_one)
                current_list = 'working_one'
                working_list_two = []
            elif current_list == 'working_one':
                process_list_for_beige(square_count, square.letter,
                                       working_list_one,
                                       working_list_two)
                current_list = 'working_two'
                working_list_one = []
            else:
                process_list_for_beige(square_count, square.letter,
                                       working_list_two,
                                       working_list_one)
                current_list = 'working_one'
                working_list_two = []
                    

def process_list_for_gray(letter, working_list, append_list):
    """Walk through the passed in working list to determine the
    eligibility of each word according to the gray squares rule."""
    
    for word in working_list:
        letters = [c for c in word]
        word_valid = True
        for column in non_green_columns:
            if letters[column] == letter:
                word_valid = False
        if word_valid:
            append_list.append(word)       


def process_gray_squares():
    """For each gray square the rule is, only words that do not contain
    that letter are eligible to be a next guess."""
    
    # Use the global variables instead of local ones
    global current_list
    global working_list_one
    global working_list_two
    
    for square in wordle_squares:
        if square.color == 'gray':
            
            # Determine the eligibility of each word in the dictionary
            if current_list == 'initial':
                process_list_for_gray(square.letter, dictionary,
                                      working_list_one)
                current_list = 'working_one'
                working_list_two = []
            elif current_list == 'working_one':
                process_list_for_gray(square.letter, working_list_one,
                                      working_list_two)
                current_list = 'working_two'
                working_list_one = []
            else:
                process_list_for_gray(square.letter, working_list_two,
                                      working_list_one)
                current_list = 'working_one'
                working_list_two = []


def process_list_for_letters(best_word, working_list):
    """Walk through the passed in working list to determine which word
    contains the most commonly used letters."""
    
    current_highest_score = 0
    common_letters = ['A', 'E', 'S', 'O', 'R', 'I', 'L', 'T']
    letter_scores = [8, 7, 6, 5, 4, 3, 2, 1]
    
    if len(working_list) > 1:
            
        # Ensure that something is returned from this method
        best_word = working_list[0]
            
        # Determine the word with the greatest number of commonly used
        # letters
        for word in working_list:
            word_score = 0
            letters = [c for c in word]
            for count in range(0, 8):
                if letters[0] == common_letters[count] or \
                        letters[1] == common_letters[count] or \
                        letters[2] == common_letters[count] or \
                        letters[3] == common_letters[count] or \
                        letters[4] == common_letters[count]:
                    word_score = word_score + letter_scores[count]
            if word_score > current_highest_score:
                current_highest_score = word_score
                best_word = word
    else:
        if len(working_list) > 0:
            best_word = working_list[0]
    return best_word


def process_most_frequent_letters():
    """For the remaining eligible words, determine which one contains
    the largest quantity of the most commonly used letters that appear
    in five letter words."""
    
    # Use the global variables instead of local ones
    global current_list
    global working_list_one
    global working_list_two
    
    current_best_word = ''
    if current_list == 'working_one':
        current_best_word = process_list_for_letters(current_best_word,
                                                     working_list_one)
    else:
        current_best_word = process_list_for_letters(current_best_word,
                                                     working_list_two)        
    return current_best_word
    
                    
def show_next_guess(next_guess):
    """Write the next Wordle guess into the Wordle squares."""
    
    # Use the global variables instead of local ones
    global last_row_filled
    
    # Determine which row is the next one to be filled
    first_square = (last_row_filled) * 5
    if next_guess != '':
        letters = [c for c in next_guess]
        wordle_squares[first_square].set_letter(win, letters[0])
        wordle_squares[first_square + 1].set_letter(win, letters[1])
        wordle_squares[first_square + 2].set_letter(win, letters[2])
        wordle_squares[first_square + 3].set_letter(win, letters[3])
        wordle_squares[first_square + 4].set_letter(win, letters[4])
        
    # If there are no words in the dictionary that meet the results 
    # criteria then just show asterisks
    else:
        wordle_squares[first_square].set_letter(win, '*')
        wordle_squares[first_square + 1].set_letter(win, '*')
        wordle_squares[first_square + 2].set_letter(win, '*')
        wordle_squares[first_square + 3].set_letter(win, '*')
        wordle_squares[first_square + 4].set_letter(win, '*')
    last_row_filled = last_row_filled + 1
    
    
def create_next_guess():
    """Check each filled in square, determine what rule is in the square.
    Check for words that are in the dictionary, and fill in the next
    guess."""

    # If all the Wordle squares are filled, there is no row for a next
    #guess
    if last_row_filled < 6:
        
        # Process the current guess results in order to generate the
        # next guess
        process_green_squares()
        process_beige_squares()
        process_gray_squares()
        next_guess = process_most_frequent_letters()
        show_next_guess(next_guess)
    
 
def reset_all_squares():
    """Take any squares that are in text entry mode out of text entry mode
    so that there is not the possibility of having multiple sguares in
    text entry mode."""
    
    for square in wordle_squares:
        if square.letter == '_':
            square.enter_letter(win, ' ')
            
            
def mouse_handler(point):
    """Respond to mouse clicks for menu buttons or squares."""

    # Use the global variable to store the results mode
    global results_mode
    
    last_row_is_done = False
    
    # Determine if a Wordle square was clicked
    reset_all_squares()
    for square in wordle_squares:
        if square.is_clicked(point):
            if square.letter != '':
                if results_mode == 'text':
                    square.set_text_mode(win)
                if results_mode == 'gray':
                    square.set_color(win, 'gray')
                if results_mode == 'beige':
                    square.set_color(win, 'beige')
                if results_mode == 'green':
                    square.set_color(win, 'green')
                last_row_is_done = determine_if_last_row_complete()
                if last_row_is_done:
                    create_next_guess()
                
    # Determine if a menu item was clicked
    for button in results_buttons:
        if button.is_clicked(point):
            if button.type == 'text':
                results_buttons[0].activate(win)
                results_buttons[1].deactivate(win)
                results_buttons[2].deactivate(win)
                results_buttons[3].deactivate(win)
                results_mode = 'text'
            if button.type == 'gray':
                results_buttons[0].deactivate(win)
                results_buttons[1].activate(win)
                results_buttons[2].deactivate(win)
                results_buttons[3].deactivate(win)
                results_mode = 'gray'
            if button.type == 'beige':
                results_buttons[0].deactivate(win)
                results_buttons[1].deactivate(win)
                results_buttons[2].activate(win)
                results_buttons[3].deactivate(win)
                results_mode = 'beige'
            if button.type == 'green':
                results_buttons[0].deactivate(win)
                results_buttons[1].deactivate(win)
                results_buttons[2].deactivate(win)
                results_buttons[3].activate(win)
                results_mode = 'green'
                
   
def key_handler(key):
    """Respond to key presses on the keyboard."""
    
    # If a letter key was pressed, enter that letter into the square
    if key in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
        for square in wordle_squares:
            if square.letter == '_':
                square.enter_letter(win, key.upper())
                        
                            
def main():
    """Run the main loop for the wordle app."""
    
    # Import the five letter words from the text file
    import_dictionary()

    # Draw the top label at the top of the main window
    draw_top_label()
 
    # Draw the five columns by six rows of squares for the Wordle letters
    draw_wordle_squares()
    
    # Draw the results label at the bottom of the main window
    draw_results_label()
    
    # Draw the results buttons at the bottom of the main window
    draw_results_buttons()

    # Fill in the first row of letter squares with the first quess
    enter_first_guess(wordle_squares)
    
    # Add a mouse handler to catch mouse clicks
    win.setMouseHandler(mouse_handler)
        
    while True:
        try:
            key = win.checkKey()
        except GraphicsError:
            break  # Window closed by user.
        if key:
            key_handler(key)
        time.sleep(.01)
            
            
# Run the main loop for the app
if __name__ == '__main__':
    main()
    
