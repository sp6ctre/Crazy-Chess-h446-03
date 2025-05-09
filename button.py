class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):  # Initializing Button instance
        self.image = image  # Button image
        self.x_pos = pos[0]  # Button x position
        self.y_pos = pos[1]  # Button y position
        self.font = font  # Button font
        self.base_color, self.hovering_color = base_color, hovering_color  # Button colors
        self.text_input = text_input  # Button text
        self.text = self.font.render(self.text_input, True, self.base_color)  # Rendered text
        if self.image is None:  # If no image is assigned to the button
            self.image = self.text  # The image becomes the text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))  # Get the image rectangle
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))  # Get the text rectangle

    def update(self, screen):  # Draw button on the screen
        if self.image is not None:  # If there is an image
            screen.blit(self.image, self.rect)  # Draw image
        screen.blit(self.text, self.text_rect)  # Draw text

    def checkForInput(self, position):  # Check if button was clicked
        # If mouse position is inside button rectangle
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True  # Click was inside button
        return False  # Click was outside button

    def changeColor(self, position):  # Change button color
        # If mouse position is inside button rectangle
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True,
                                         self.hovering_color)  # Change button color to hover color
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)  # Change button color to base color
