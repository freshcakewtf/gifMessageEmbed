from PIL import Image, ImageSequence
import numpy as np

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text) + '1111111111111110'

def encode_text_into_gif(input_gif, output_gif, secret_text):
    binary_secret = text_to_binary(secret_text)
    binary_index = 0
    binary_len = len(binary_secret)

    gif = Image.open(input_gif)
    frames = []

    for frame in ImageSequence.Iterator(gif):
        # Get the palette (important!)
        palette = frame.getpalette()

        # Convert to "P" mode (palette mode) if not already
        if frame.mode != "P":
            frame = frame.convert("P", palette=palette) # Use original palette, or None for automatic

        pixels = np.array(frame)

        for i in range(pixels.shape[0]):
            for j in range(pixels.shape[1]):
                if binary_index < binary_len:
                    # Modify the pixel index directly (LSB of the index)
                    pixels[i, j] = (pixels[i, j] & 0xFE) | int(binary_secret[binary_index])
                    binary_index += 1
                else:
                    break
            if binary_index >= binary_len:
                break
        if binary_index >= binary_len:
            break

        new_frame = Image.fromarray(pixels, "P") # Create a new palette image
        new_frame.putpalette(palette)  # Restore the original palette!!
        frames.append(new_frame)

    frames[0].save(output_gif, save_all=True, append_images=frames[1:], loop=0, duration=gif.info.get("duration", 100))

    print(f"Secret text encoded into {output_gif}")


# Example Usage
encode_text_into_gif("input.gif", "output_encoded.gif", "This should work now!")
