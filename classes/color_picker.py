from PIL import Image
import numpy as np
from collections import Counter

def get_colors(image_path, num_colors=1):
    """
    This function takes an image path and a number of colors as input, and returns the most common colors in the image.

    Args:
        image_path (str): The path to the image file.
        num_colors (int, optional): The number of most common colors to return. Defaults to 1.

    Returns:
        list: A list of tuples, where each tuple represents a color in RGB format. The list is sorted by the frequency of the colors in the image, in descending order.
    """
    # Open the image file
    img = Image.open(image_path)
    # Resize the image to 150x150 pixels
    img = img.resize((150, 150))

    # Convert the image to RGB format
    img = img.convert('RGB')
    # Convert the image to a numpy array
    img_array = np.array(img)
    # Reshape the array to a 2D array, where each row represents a pixel and the columns are the RGB values
    reshaped_array = img_array.reshape((img_array.shape[0] * img_array.shape[1]), 3)

    # Count the frequency of each color in the image
    color_counts = Counter(map(tuple, reshaped_array))
    # Get the most common colors
    most_common_colors = color_counts.most_common(num_colors)

    # Return the most common colors
    return [color[0] for color in most_common_colors]