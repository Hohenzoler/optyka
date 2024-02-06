import pygame  # Importing the pygame module
import imgtocode  # Importing the imgtocode module
import os  # Importing the os module


imgtocode.generateImages()  # Generating images if the directory does not exist

# Loading various images using the pygame module
torch_icon = pygame.image.load("images/torch_icon.png")  # Loading the torch icon image
object_icon = pygame.image.load("images/object_icon.png")  # Loading the object icon image
prism_icon = pygame.image.load("images/Prism.png")  # Loading the prism icon image
settings_icon = pygame.image.load('images/settings.png')  # Loading the settings icon image
exit_icon = pygame.image.load('images/exit.png')  # Loading the exit icon image
torch = pygame.image.load('images/torch.png')  # Loading the torch image
laser = pygame.image.load('images/black_rectangle.png')  # Loading the laser image
bin = pygame.image.load('images/trash.png')  # Loading the bin image
bad_coursor = pygame.image.load('images/bad_coursor.png')  # Loading the bad cursor image
topopisy = pygame.image.load('images/topopisy.png')  # Loading the topopisy image
pen = pygame.image.load('images/pen.png')  # Loading the pen image
water = pygame.image.load('images/materials/water.png')  # Loading the water image
clouds = pygame.image.load('images/materials/clouds.png')  # Loading the clouds image
wood = pygame.image.load('images/materials/wood.png')  # Loading the wood image
glass = pygame.image.load('images/materials/glass.png')  # Loading the glass image
papier = pygame.image.load('images/materials/paper.png')  # Loading the paper image
lens = pygame.image.load('images/glasses.png')  # Loading the lens image
glass_icon = pygame.image.load("images/glass_thing_icon.png")  # Loading the glass icon image