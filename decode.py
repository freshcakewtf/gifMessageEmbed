from PIL import Image, ImageSequence
import numpy as np

def binary_to_text(binary_str):
    """Convert binary string to text, stopping at the delimiter."""
    try:
        delimiter_index = binary_str.find('1111111111111110') # Look for the full delimiter
        if delimiter_index != -1:
            binary_str = binary_str[:delimiter_index]  # Truncate at delimiter
    except:
        pass

    chars = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
    text = ''.join(chr(int(char, 2)) for char in chars)
    return text # No need to split anymore, the delimiter is what matters

def decode_text_from_gif(encoded_gif):
    gif = Image.open(encoded_gif)
    binary_data = ""

    for frame in ImageSequence.Iterator(gif):
        # Get the palette (important!)
        palette = frame.getpalette()

        # Convert to "P" mode (palette mode) if not already
        if frame.mode != "P":
            frame = frame.convert("P", palette=palette)

        pixels = np.array(frame)

        for i in range(pixels.shape[0]):
            for j in range(pixels.shape[1]):
                binary_data += str(pixels[i, j] & 1)  # Read LSB of the pixel index

    secret_message = binary_to_text(binary_data)
    print("Extracted Message:", secret_message)
    return secret_message

# Example Usage
decode_text_from_gif("output_encoded.gif")
