class ButtonAnimation:
    """
    A class used to represent an animation for a button.

    ...

    Attributes
    ----------
    button : object
        an instance of a button class
    target_position_x : int
        the target x-coordinate for the button
    target_position_y : int
        the target y-coordinate for the button

    Methods
    -------
    animate():
        Moves the button towards the target position and updates the textRect center.
    """

    def __init__(self, button, target_position_x, target_position_y):
        """
        Constructs all the necessary attributes for the ButtonAnimation object.

        Parameters
        ----------
            button : object
                an instance of a button class
            target_position_x : int
                the target x-coordinate for the button
            target_position_y : int
                the target y-coordinate for the button
        """
        self.button = button
        self.target_position_x = target_position_x
        self.target_position_y = target_position_y

    def animate(self):
        """
        Moves the button towards the target position and updates the textRect center.
        The button's x and y coordinates are updated by 10% of the distance to the target position.
        If the button's textRect center cannot be updated, the exception is caught and ignored.
        """
        self.button.rect.x += (self.target_position_x - self.button.rect.x) * 0.1
        self.button.rect.y += (self.target_position_y - self.button.rect.y) * 0.1
        try:
            self.button.textRect.center = (
            self.button.rect[0] + (self.button.rect[2] // 2), self.button.rect[1] + (self.button.rect[3] // 2))
        except:
            pass
