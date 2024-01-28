from PIL import Image
import numpy as np
from collections import Counter

def get_colors(image_path, num_colors=1):
    img = Image.open(image_path)
    img = img.resize((150, 150))


    img = img.convert('RGB')
    img_array = np.array(img)
    reshaped_array = img_array.reshape((img_array.shape[0] * img_array.shape[1]), 3)

    color_counts = Counter(map(tuple, reshaped_array))
    most_common_colors = color_counts.most_common(num_colors)

    return [color[0] for color in most_common_colors]

