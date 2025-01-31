from PIL import Image, ImageSequence
import numpy as np

print("making a super secret note.")

def text_to_binary(text):
    """Convert text to a binary string."""
    return ''.join(format(ord(char), '08b') for char in text) + '1111111111111110'  # End delimiter

def encode_text_into_gif(input_gif, output_gif, secret_text):
    """Encodes a text message into the least significant bits of a GIF."""
    
    binary_secret = text_to_binary(secret_text)
    binary_index = 0
    binary_len = len(binary_secret)

    gif = Image.open(input_gif)
    frames = []

    for frame in ImageSequence.Iterator(gif):
        frame = frame.convert("RGB")  # Convert to RGB to prevent issues with indexed colors
        pixels = np.array(frame)

        for i in range(pixels.shape[0]):
            for j in range(pixels.shape[1]):
                for k in range(3):  # Modify R, G, B channels
                    if binary_index < binary_len:
                        pixels[i, j, k] = (pixels[i, j, k] & 0xFE) | int(binary_secret[binary_index])
                        binary_index += 1
                    else:
                        break
                if binary_index >= binary_len:
                    break
            if binary_index >= binary_len:
                break

        new_frame = Image.fromarray(pixels, "RGB")
        frames.append(new_frame)

    frames[0].save(output_gif, save_all=True, append_images=frames[1:], loop=0, duration=gif.info.get("duration", 100))

    print(f"Secret text encoded into {output_gif}")

# Example Usage
encode_text_into_gif("input.gif", "output_encoded.gif", "not working right now!")