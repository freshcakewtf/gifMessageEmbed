from PIL import Image, ImageSequence
import numpy as np

print("decoder Ring, ACTIVATE!!")

def binary_to_text(binary_str):
    """Convert binary string to text, stopping at the delimiter."""
    chars = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
    text = ''.join(chr(int(char, 2)) for char in chars)
    return text.split('þ')[0]  # Stop at delimiter

def decode_text_from_gif(encoded_gif):
    """Extracts a hidden message from the least significant bits of a GIF."""
    
    gif = Image.open(encoded_gif)
    binary_data = ""

    for frame in ImageSequence.Iterator(gif):
        frame = frame.convert("RGB")  # Convert to RGB to match encoding
        pixels = np.array(frame)

        for i in range(pixels.shape[0]):
            for j in range(pixels.shape[1]):
                for k in range(3):  # Read R, G, B channels
                    binary_data += str(pixels[i, j, k] & 1)

    secret_message = binary_to_text(binary_data)
    print("Extracted Message:", secret_message)
    return secret_message

# Example Usage
decode_text_from_gif("output_encoded.gif")