from PIL import Image
import numpy as np

def process_image(image_path, key):
    # Open the image
    img = Image.open(image_path)
    img_array = np.array(img)

    # Apply the XOR math to every pixel using the key
    processed_array = np.bitwise_xor(img_array, key)

    # Turn the math back into an image
    return Image.fromarray(processed_array)