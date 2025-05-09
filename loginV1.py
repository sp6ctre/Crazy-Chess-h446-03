import pygame
import sys
import sqlite3

from chess import ChessMain
from menu import menu2  # Import the second menu


def main():
    pygame.init()

    # Window settings
    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Setting the screen size
    pygame.display.set_caption("Login")  # Setting screen title

    # Load background image
    background = pygame.image.load("images2/chessBackground.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Scaling the background image

    # Fonts
    fontLarge = pygame.font.SysFont("Century Gothic", 24)  # Larger font size for text
    fontMedium = pygame.font.SysFont("Century Gothic", 18)  # Medium font size for text
    fontSmall = pygame.font.SysFont("Century Gothic", 14)  # Small font size for text

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    gray = (200, 200, 200)

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
            y = 295
            x = center_x - line_width // 2
            # Render the line onto the surface at the calculated position.
            surface.blit(line_surface, (x, y + i * (font.get_height() + 2)))

    # Input boxes
    class InputBox:
        def __init__(self, x, y, w, h, placeholder='', isPassword=False):  # Initializing an InputBox instance
            self.rect = pygame.Rect(x, y, w, h)  # The rectangle where the input box would be
            self.color = gray  # The idle color of the outline box
            self.text = ''  # The inputted text
            self.placeholder = placeholder  # The placeholder3 given in the parameters
            self.txt_surface = fontMedium.render(self.placeholder, True, (100, 100, 100))
            # Rendered placeholder
            self.active = False  # Is input box being interacted?
            self.isPassword = isPassword  # Is the input box a password field?

        # Event method for the InputBox class
        def Event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:  # If the mouse button is pressed
                self.active = self.rect.collidepoint(event.pos)  # If it was clicked on
                self.color = black if self.active else gray  # Switches to this color if clicked

            if event.type == pygame.KEYDOWN and self.active:  # If a key is pressed and the input box is active
                if event.key == pygame.K_BACKSPACE:  # If the Backspace key is pressed
                    self.text = self.text[:-1]  # Gets all text except for the last character (deletes last char)
                elif event.key == pygame.K_RETURN:  # If the Return key is pressed
                    self.active = False  # The box isn't being interacted with anymore
                else:  # If any other key was pressed
                    self.text += event.unicode  # Add that key

            displayText = '*' * len(self.text) if self.isPassword and self.text else self.text or self.placeholder
            color = black if self.text else (100, 100, 100)
            self.txt_surface = fontMedium.render(displayText, True, color)


        def draw(self, screen):  # Draw method for InputBox class
            screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 8))  # Renders self.txt_surface
            pygame.draw.rect(screen, self.color, self.rect, 2)  # Draws the rectangle (outline)

        def getText(self):  # Gets the current text in the input box
            return self.text

    usernameBox = InputBox(530, 180, 220, 35, placeholder="Username",)  # Username input field
    passwordBox = InputBox(530, 230, 220, 35, placeholder="Password", isPassword=True)
    # Password input field
    errorMessage = ''  # Error message (none yet because we just started the game)

    # Buttons
    loginButton = pygame.Rect(530, 315, 220, 40)  # Login button
    backButton = pygame.Rect(485, 440, 100, 35)  # Back button

    # Connect to database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    running = True
    while running:
        screen.blit(background, (0, 0))  # Renders the background
        '''Frame rectangle'''
        pygame.draw.rect(screen, white, (480, 120, 320, 360), border_radius=15)  # Central rectangle

        '''Text'''
        screen.blit(fontLarge.render("Log Into Your Account", True, black), (550, 135))
        # Title of the screen
        screen.blit(fontSmall.render("Forget Password?", True, black), (530, 275))
        # Prompt for forgotten passwords

        ''''Error message'''
        if errorMessage:
            drawText(errorMessage, fontSmall, red, screen, WIDTH // 2, 325, 280)

        '''Input boxes'''
        usernameBox.draw(screen)  # Draw the username input box
        passwordBox.draw(screen)  # Draw the password input box

        '''Login button'''
        pygame.draw.rect(screen, gray, loginButton, border_radius=15)
        screen.blit(fontMedium.render("Login", True, black), (loginButton.x + 90, loginButton.y + 10))

        '''Back button'''
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

            # If the mouse button is clicked
            # Checking for a mouse button click event.
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If clicked within login button rectangle.
                if loginButton.collidepoint(event.pos):
                    username = str(usernameBox.getText())  # Get entered username text from input box.
                    password = str(passwordBox.getText())  # Get entered password text from input box.
                    if username and password:  # If both username and password fields are filled.
                        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?",
                                       (username, password))
                        # SQLite's cursors execute method to fetch user data from users table.
                        # If a row is fetched, that means user credentials were correct.
                        if cursor.fetchone():  # If a row is fetched, that means user credentials were correct.
                            # Start the main chess game if login is successful.
                            ChessMain.main()
                            # Close the Pygame window.
                            pygame.quit()
                            # Exit from Python script.
                            sys.exit()
                            # If no row was fetched, then either the username and/or password was incorrect.
                        else:
                            # Provide error message for invalid login attempt.
                            errorMessage = "Incorrect username or password."
                            # If either username or password or both fields are empty.
                    else:
                        # Provide error message for missing details.
                        errorMessage = "Please enter both username and password."

                # If the back button is clicked
                if backButton.collidepoint(event.pos):
                    menu2.secondMenu()  # Go to the second menu
                    return

        pygame.display.update()  # Updating the game window


if __name__ == "__main__":
    main()  # Start the main function (run the game)
