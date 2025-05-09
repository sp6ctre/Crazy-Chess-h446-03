import pygame, sys
from button import Button

pygame.init()

screen = pygame.display.set_mode((1280, 720))  # Setting screen resolution
pygame.display.set_caption("Crazy Chess")  # Setting window title

background = pygame.image.load("images2/img.png")  # Loading the background image

def getFont(size):
    return pygame.font.Font("images2/font.ttf", size)  # Returns Press-Start-2P in the desired size


def mainMenu():
    from menu import menu2
    pygame.display.set_caption("Crazy Chess")  # Setting window title

    while True:  # Loop for the main menu screen
        screen.blit(background, (0, 0))

        menuMousePosition = pygame.mouse.get_pos()  # Gets the current position of the mouse

        menuText = getFont(100).render("CRAZY CHESS", True, "#b68f40")
        #  Creates a text based on the getFont function and render it into an image
        menuRect = menuText.get_rect(center=(640, 100))  # Center the text on the given position

        playButton = Button(image=pygame.image.load("images2/Play Rect.png"), pos=(640, 310),
                             text_input="PLAY", font=getFont(75), base_color="White", hovering_color="#d7fcd4")
        quitButton = Button(image=pygame.image.load("images2/Quit Rect.png"), pos=(640, 450),
                             text_input="QUIT", font=getFont(75), base_color="White", hovering_color="#d7fcd4")
        # Creates two buttons for the menu: "PLAY" and "QUIT"

        screen.blit(menuText, menuRect) # Draws the text image on the screen at the rectangle position

        for button in [playButton, quitButton]:
            button.changeColor(menuMousePosition)  # Changes the color of the button upon hovering
            button.update(screen)  # Draws the button on the screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the close window button is clicked
                pygame.quit()  # Stop all the Pygame modules
                sys.exit()  # Close Python
            if event.type == pygame.MOUSEBUTTONDOWN:  # If the "PLAY" button is clicked
                if playButton.checkForInput(menuMousePosition):
                    menu2.secondMenu()  # Start the main function of the login/sign up
                if quitButton.checkForInput(menuMousePosition):  # If the "QUIT" button is clicked
                    pygame.quit()  # Stop all the Pygame modules
                    sys.exit()  # Close Python

        pygame.display.update()  # Refresh the whole screen

if __name__ == "__main__":
    mainMenu()
