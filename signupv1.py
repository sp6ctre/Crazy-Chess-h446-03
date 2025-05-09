import pygame
import sys
from chess import ChessMain
from menu import menu2  # Import the second menu
from menu import loginV1
import sqlite3

# Create/connect to the database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Runs SQL command to create 'users' table if it doesn't exist.
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT)''')

conn.commit()  # Save changes to database.



def main():
    pygame.init()

    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Setting the screen size
    pygame.display.set_caption("Sign up")  # Setting window title

    background = pygame.image.load("images2/chessBackground.png")  # Loading background image
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Scaling background to fit screen resolution

    # Fonts
    fontLarge = pygame.font.SysFont("Century Gothic", 24)  # Large font
    fontMedium = pygame.font.SysFont("Century Gothic", 18)  # Medium font
    fontSmall = pygame.font.SysFont("Century Gothic", 14)  # Small font

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    gray = (200,200,200)

    # The drawText function is designed to create text fields in pygame.
    def drawText(text, font, color, surface, center_x, y, max_width):
        words = text.split(' ')  # The text is split into individual words.
        lines = []  # Initialize an empty list to store lines of text.
        current_line = ''  # Initialize an empty string to store the current line of text.

        # This for loop processes each word in the text.
        for word in words:
            test_line = current_line + word + ' '  # A temporary line that adds the next word to the current line.

            # This if statement checks if the width of the text line still fits within the specified maximum width.
            if font.size(test_line)[0] <= max_width:
                current_line = test_line  # If it fits, the test line becomes the current line.
            else:
                lines.append(current_line.strip())  # If it doesn't fit, the current line is added to the line list.
                current_line = word + ' '  # Start a new line with the word that didn't fit.
        lines.append(current_line.strip())  # Add the final current line to the line list.

        # This for loop processes each line of text.
        for i, line in enumerate(lines):
            line_surface = font.render(line, True, color)  # Render the line as a pygame surface.
            line_width = line_surface.get_width()  # Get the width of the rendered line.
            # Calculate the x-coordinate to center each line.
            x = center_x - line_width // 2
            # Render the line onto the surface at the calculated position.
            surface.blit(line_surface, (x, y + i * (font.get_height() + 2)))

    # Input box class
    class InputBox:
        def __init__(self, x, y, w, h, placeholder='', isPassword=False):  # Initializing an InputBox instance
            self.rect = pygame.Rect(x, y, w, h)  # The rectangle for the input box
            self.color = gray  # The idle color of the outline box
            self.text = ''  # The inputted text
            self.placeholder = placeholder  # The placeholder to display when there is no input
            self.txt_surface = fontMedium.render(self.placeholder, True, (100, 100, 100))
            # Rendered placeholder
            self.active = False  # Is the input box active?
            self.isPassword = isPassword  # Is the input box a password field?

        def Event(self, event):  # Event for the InputBox class
            if event.type == pygame.MOUSEBUTTONDOWN:  # If the mouse is pressed
                self.active = self.rect.collidepoint(event.pos)  # InputBox was clicked on
                self.color = black if self.active else gray  # Switches to this color when clicked

            if event.type == pygame.KEYDOWN and self.active:  # If a key is pressed and the input box is active
                if event.key == pygame.K_BACKSPACE:  # If the Backspace key is pressed
                    self.text = self.text[:-1]  # Gets all text except for the last character
                elif event.key == pygame.K_RETURN:  # If the Return key is pressed
                    self.active = False  # InputBox stops being active
                else:  # If any other key was pressed
                    self.text += event.unicode  # Add that key to the text

            displayText = '*' * len(self.text) if self.isPassword and self.text else self.text or self.placeholder
            color = black if self.text else (100, 100, 100)
            self.txt_surface = fontMedium.render(displayText, True, color)

        def draw(self, screen):  # Draw method for InputBox class
            screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 8))  # Renders self.txt_surface
            pygame.draw.rect(screen, self.color, self.rect, 2)  # Draw the rectangle (outline box)

        def getText(self):  # Get the current text in the input box
            return self.text

    usernameBox = InputBox(530, 180, 220, 35, placeholder="Create a Username")  # Username input field
    passwordBox = InputBox(530, 230, 220, 35, placeholder="Create a Password", isPassword=True)
    # password input field
    passwordBox2 = InputBox(530, 280, 220, 35, placeholder="Confirm Your Password", isPassword=True)
    # password input field

    errorMessage = ''  # Error message # Error message (none yet because we just started the game)

    # Buttons
    signupButton = pygame.Rect(530, 350, 220, 40) # signin button
    backButton = pygame.Rect(485, 440, 100, 35)  # Back button

    running = True
    while running:
        screen.blit(background, (0, 0))  # Renders the background

        # Frame rectangle
        pygame.draw.rect(screen, white, (480, 120, 320, 360), border_radius=15)  # Central rectangle

        # Title of the screen
        screen.blit(fontLarge.render("Create An Account", True, black), (570, 135))

        # Error message
        if errorMessage:
            drawText(errorMessage, fontSmall, red, screen, WIDTH // 2, 325, 280)

        # Draw input boxes
        usernameBox.draw(screen)  # Draw the username input box
        passwordBox.draw(screen)  # Draw the password input box
        passwordBox2.draw(screen)  # Draw the confirmation password input box

        # sign up button
        pygame.draw.rect(screen, gray, signupButton, border_radius=15) # Button rectangle
        screen.blit(fontMedium.render("Sign up", True, black), (signupButton.x + 90, signupButton.y
                                                                + 10))
        # Button text

        # Back button
        pygame.draw.rect(screen, gray, backButton, border_radius=15)  # Button rectangle
        screen.blit(fontSmall.render("Back", True, black), (backButton.x + 35, backButton.y + 12))
        # Button text

        for event in pygame.event.get():  # Event loop
            if event.type == pygame.QUIT:  # Closing the game
                running = False  # Stop the main loop
                pygame.quit()  # Stop Pygame
                sys.exit()  # Stop the script (program)

            usernameBox.Event(event)  # Username box events
            passwordBox.Event(event)  # Password box events
            passwordBox2.Event(event)  # Confirmation password box events

            # On mouse click:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if signupButton.collidepoint(event.pos):  # If signup button clicked.
                    # Get entered username and passwords.
                    username = str(usernameBox.getText())
                    password = str(passwordBox.getText())
                    password2 = str(passwordBox2.getText())

                    if username and password == password2:  # If both passwords match.
                        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
                        if cursor.fetchone():  # If username exists, show error.
                            errorMessage = "Username exists."
                        elif len(password) < 8 or not any(char.isdigit() for char in password) or not any(
                                char.isupper() for char in password):
                            errorMessage = ("Password must have atleast 8 characters, include atleast one number, "
                                            "and at least one capital letter.")
                        elif password == "" or password2 == "":
                            errorMessage = "Enter a password."
                        else:  # Apply the changes to database and exit.
                            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                                           (username, password))
                            conn.commit()
                            loginV1.main()
                            pygame.quit()
                            sys.exit()
                    elif username and password != password2:  # If passwords don't match, show error.
                        errorMessage = "Passwords don't match."
                    else:  # If username/password is empty, show error.
                        errorMessage = "Enter a username and a password."

                # If the back button is clicked
                if backButton.collidepoint(event.pos):
                    menu2.secondMenu()  # Go to the second menu
                    return

        pygame.display.update()  # Updating the game window

if __name__ == "__main__":
    main()  # Start the main function (run the game)
