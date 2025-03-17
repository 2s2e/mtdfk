import re
from PIL import Image
import numpy as np
from collections import Counter
import os


def extract_emblem(image_path, output_path):
    # Open the image and convert it to RGBA
    img = Image.open(image_path).convert("RGBA")
    img_array = np.array(img)

    # Get the top-left corner color
    top_left_color = tuple(img_array[0, 0])

    # Flatten the image array into a list of colors (excluding the alpha channel)
    colors = img_array.reshape(-1, 4)

    # Count occurrences of each color
    color_counts = Counter(map(tuple, colors))

    # Remove the top-left color from consideration
    color_counts.pop(top_left_color, None)

    if not color_counts:
        raise ValueError("No distinct colors found aside from the top-left color.")

    # Get the most common non-background color
    most_common_color = color_counts.most_common(1)[0][0]

    # Define replacement colors
    transparent = (0, 0, 0, 0)
    solid_red = (255, 0, 0, 255)

    # Process the image
    mask_top_left = (
        (img_array[:, :, 0] == top_left_color[0])
        & (img_array[:, :, 1] == top_left_color[1])
        & (img_array[:, :, 2] == top_left_color[2])
        & (img_array[:, :, 3] == top_left_color[3])
    )

    mask_common = (
        (img_array[:, :, 0] == most_common_color[0])
        & (img_array[:, :, 1] == most_common_color[1])
        & (img_array[:, :, 2] == most_common_color[2])
        & (img_array[:, :, 3] == most_common_color[3])
    )

    # Apply the transformations
    new_img_array = np.zeros_like(img_array)
    new_img_array[:, :, :] = transparent  # Default to transparent
    new_img_array[mask_common] = solid_red  # Set most common color to red
    new_img_array[mask_top_left] = transparent  # Ensure background is transparent

    # Create and save the new image
    new_img = Image.fromarray(new_img_array, "RGBA")
    new_img.save(output_path)


# Example usage
# extract_emblem("path_to_input_image.png", "path_to_output_image.png")
# def convert_svg_to_png(svg_path, png_path, dpi=300):
#     """
#     Converts an SVG file to a PNG file.

#     :param svg_path: Path to the input SVG file.
#     :param png_path: Path to save the output PNG file.
#     :param dpi: Resolution in DPI (default: 300 for high quality).
#     """
#     cairosvg.svg2png(url=svg_path, write_to=png_path, dpi=dpi)


def extract_prefecture_name(filename):
    match = re.search(r"Flag_of_(.+?)_Prefecture", filename)
    return match.group(1) if match else None


for img in os.listdir("flags"):
    png_path_name = "flags/" + img
    name = extract_prefecture_name(img)
    extract_emblem(f"{png_path_name}", f"output/{name}_Emblem.png")
