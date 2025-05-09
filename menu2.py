import pygame, sys
from button import Button
from menu import Menu

pygame.init()

screen = pygame.display.set_mode((1280, 720))  # Creating display surface
pygame.display.set_caption("Crazy Chess")  # Setting title of game window

background = pygame.image.load("images2/img.png")  # Loading background image


def getFont(size):  # Function to get a specific size of font
    return pygame.font.Font("images2/font.ttf", size)


def secondMenu():  # Defining the function for the second menu of the game
    from menu import loginV1
    from menu import signupv1
    pygame.display.set_caption("Crazy Chess")  # Setting window title

    while True:  # Loop for the second menu screen
        screen.blit(background, (0, 0))  # Drawing the background

        menuMousePosition = pygame.mouse.get_pos()  # Getting the mouse cursor position

        menuText = getFont(100).render("CRAZY CHESS", True, "#b68f40")
        # Rendering the "CRAZY CHESS" text
        menuRect = menuText.get_rect(center=(640, 100))  # Centering the text

        # Creating the "LOGIN", "SIGNUP" and "BACK" buttons
        loginButton = Button(image=pygame.image.load("images2/Play Rect.png"), pos=(640, 310),
                             text_input="LOGIN", font=getFont(60), base_color="White", hovering_color="#d7fcd4")
        signupButton = Button(image=pygame.image.load("images2/Play Rect.png"), pos=(640, 450),
                              text_input="SIGNUP", font=getFont(60), base_color="White", hovering_color="#d7fcd4")
        backButton = Button(image=pygame.image.load("images2/Quit Rect.png"), pos=(150, 650),
                            text_input="BACK", font=getFont(40), base_color="White", hovering_color="#d7fcd4")

        screen.blit(menuText, menuRect)  # Drawing the text

        # Loop to change colors on hover and to update buttons
        for button in [loginButton, signupButton, backButton]:
            button.changeColor(menuMousePosition)
            button.update(screen)

        for event in pygame.event.get():  # Event loop
            if event.type == pygame.QUIT:  # Check for window quit event
                pygame.quit()  # Exiting pygame
                sys.exit()  # Exiting the script
            if event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse button down event
                if loginButton.checkForInput(menuMousePosition):  # Check if login button is pressed
                    pygame.display.set_mode((1, 1))  # Minimizing pygame display
                    loginV1.main()  # Running Tkinter main loop
                    pygame.display.set_mode((1280, 720))  # Restoring pygame display size
                    screen.blit(background, (0, 0))  # Refreshing the display background
                    pygame.display.update()  # Refreshing the whole screen

                if signupButton.checkForInput(menuMousePosition):  # Check if signup button is pressed
                    pygame.display.set_mode((1, 1))  # Minimizing pygame display
                    signupv1.main()  # Running Tkinter main loop
                    pygame.display.set_mode((1280, 720))  # Restoring pygame display size
                    screen.blit(background, (0, 0))  # Refreshing the display background
                    pygame.display.update()  # Refreshing the whole screen

                if backButton.checkForInput(menuMousePosition):  # Check if back button is pressed
                    Menu.mainMenu()  # Going back to main menu

        pygame.display.update()  # Refreshing the whole screen


if __name__ == "__main__":
    secondMenu()  # Running second menu
