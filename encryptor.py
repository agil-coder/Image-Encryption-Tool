from PIL import Image, ImageDraw, ImageFont
import numpy as np

def hide_message(image_path, secret_message):
    img = Image.open(image_path).convert('RGB')
    pixels = np.array(img, dtype=np.int16) # Change to int16 (allows negative math temporarily)
    
    binary_msg = ''.join(format(ord(i), '08b') for i in secret_message) + '00000000'
    
    flattened = pixels.flatten()
    
    if len(binary_msg) > len(flattened):
        raise ValueError("Message too long for this image!")

    for i in range(len(binary_msg)):
        # This bitwise logic is now safer with int16
        flattened[i] = (int(flattened[i]) & ~1) | int(binary_msg[i])
        
    # Convert back to uint8 ONLY when saving the image
    new_pixels = flattened.reshape(pixels.shape).astype(np.uint8)
    return Image.fromarray(new_pixels)
    
    # 3. SAFETY CHECK: Compare message size to image size
    if len(binary_msg) > max_capacity:
        raise ValueError(f"Message too long! Image can only hold {max_capacity // 8} characters.")

    flattened = pixels.flatten()
    
    # 4. Hide the bits
    for i in range(len(binary_msg)):
        flattened[i] = (flattened[i] & ~1) | int(binary_msg[i])
        
    new_pixels = flattened.reshape(pixels.shape)
    return Image.fromarray(new_pixels.astype('uint8'))

def reveal_and_annotate(image_path):
    # 1. First, get the secret string (using your fast NumPy logic)
    img = Image.open(image_path).convert('RGB')
    pixels = np.array(img).flatten()
    extracted_bits = pixels & 1
    byte_data = np.packbits(extracted_bits)
    
    message = ""
    for b in byte_data:
        if b == 0: break
        message += chr(b)

    # 2. Now, "draw" that message onto the image
    if message:
        draw = ImageDraw.Draw(img)
        
        # We pick a simple font size based on image width
        font_size = img.width // 20 
        
        # Try to load a default font, otherwise use basic
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        # Draw a black shadow for readability, then white text
        # Positioned at the bottom-center
        text_pos = (img.width // 10, img.height - (font_size * 2))
        draw.text(text_pos, f"Secret: {message}", fill="black", font=font, stroke_width=2)
        draw.text(text_pos, f"Secret: {message}", fill="yellow", font=font)
        
        return img, message
    
    return None, "No message found"
