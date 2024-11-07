import numpy as np
import cv2

def get_key_matrix(key, matrix_size):
    key_matrix = np.zeros((matrix_size, matrix_size), dtype=int)
    k = 0
    for i in range(matrix_size):
        for j in range(matrix_size):
            key_matrix[i, j] = ord(key[k % len(key)]) % 256
            k += 1
    return key_matrix

def encrypt_pixel(key_matrix, pixel_vector):
    result = np.dot(key_matrix, pixel_vector) % 256
    return result.astype(np.uint8)

def hill_cipher_image(input_path, output_path, key):
    # Read the input image
    image = cv2.imread(input_path)
    if image is None:
        print("Error: Could not read the image.")
        return

    # Determine the size of the key matrix (3x3 for this implementation)
    matrix_size = 3

    # Generate the key matrix
    key_matrix = get_key_matrix(key, matrix_size)

    # Create output image
    encrypted_image = np.zeros_like(image)

    # Encrypt the image
    height, width, channels = image.shape
    for y in range(0, height, matrix_size):
        for x in range(0, width, matrix_size):
            for c in range(channels):
                pixel_vector = np.zeros(matrix_size, dtype=int)
                for i in range(matrix_size):
                    if y + i < height and x < width:
                        pixel_vector[i] = image[y + i, x, c]
                    else:
                        pixel_vector[i] = 0

                encrypted_pixel = encrypt_pixel(key_matrix, pixel_vector)

                for i in range(matrix_size):
                    if y + i < height and x < width:
                        encrypted_image[y + i, x, c] = encrypted_pixel[i]

    # Save the encrypted image
    cv2.imwrite(output_path, encrypted_image)
    print(f"Encrypted image saved to: {output_path}")

def main():
    input_path = input("Enter the path of the input image: ")
    output_path = input("Enter the path for the output image: ")
    key = input("Enter the encryption key: ")

    hill_cipher_image(input_path, output_path, key)

if __name__ == "__main__":
    main()