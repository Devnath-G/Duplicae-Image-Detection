from PIL import Image
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def dhash(image_path, hash_size=8):
    # Open the image, convert it to grayscale, and resize it
    image = Image.open(image_path).convert('L')
    resized = image.resize((hash_size + 1, hash_size), Image.BICUBIC)

    # Compute the horizontal gradient between adjacent pixels
    difference = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel_left = resized.getpixel((col, row))
            pixel_right = resized.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)

    # Convert the binary array to a hexadecimal string
    decimal_value = 0
    hex_string = []
    for (index, value) in enumerate(difference):
        if value:
            decimal_value += 2 ** (index % 8)
        if (index % 8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
            decimal_value = 0

    return ''.join(hex_string)


def find_duplicate_images(directory, hash_size=8):
    # Dictionary to store image hashes
    image_hashes = {}

    # Traverse the directory and calculate hashes
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(root, file)
                hash_value = dhash(file_path, hash_size)
                if hash_value in image_hashes:
                    image_hashes[hash_value].append(file_path)
                else:
                    image_hashes[hash_value] = [file_path]

    # Filter duplicates (more than one image with the same hash)
    duplicate_images = {k: v for k, v in image_hashes.items() if len(v) > 1}

    return duplicate_images


def plot_duplicate_images(duplicate_images):
    # Plot each set of duplicate images
    for hash_value, file_paths in duplicate_images.items():
        print(f"Hash: {hash_value}")
        for file_path in file_paths:
            print(f"- {file_path}")

            # Plotting the Image
            img = mpimg.imread(file_path)
            plt.imshow(img)
            plt.title(f"Hash: {hash_value}")
            plt.show()
        print()


if __name__ == "__main__":
    directory_path = r'C:\Users\devna\Downloads\New folder'
    duplicate_images = find_duplicate_images(directory_path)

    if duplicate_images:
        print("Duplicate Images Found:")
        plot_duplicate_images(duplicate_images)
    else:
        print("No duplicate images found.")
