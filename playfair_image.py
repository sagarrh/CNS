import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def generate_key_square(key):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    key = key.upper().replace(" ", "") + alphabet
    key_square = ""
    for char in key:
        if char not in key_square:
            key_square += char
    return np.array(list(key_square)).reshape(6, 6)

def find_position(key_square, char):
    return np.where(key_square == char)

def encrypt_pair(key_square, a, b):
    row_a, col_a = find_position(key_square, a)
    row_b, col_b = find_position(key_square, b)
    
    if row_a == row_b:
        return key_square[row_a, (col_a + 1) % 6][0], key_square[row_b, (col_b + 1) % 6][0]
    elif col_a == col_b:
        return key_square[(row_a + 1) % 6, col_a][0], key_square[(row_b + 1) % 6, col_b][0]
    else:
        return key_square[row_a, col_b][0], key_square[row_b, col_a][0]

def decrypt_pair(key_square, a, b):
    row_a, col_a = find_position(key_square, a)
    row_b, col_b = find_position(key_square, b)
    
    if row_a == row_b:
        return key_square[row_a, (col_a - 1) % 6][0], key_square[row_b, (col_b - 1) % 6][0]
    elif col_a == col_b:
        return key_square[(row_a - 1) % 6, col_a][0], key_square[(row_b - 1) % 6, col_b][0]
    else:
        return key_square[row_a, col_b][0], key_square[row_b, col_a][0]

def playfair_encrypt(key, plaintext):
    key_square = generate_key_square(key)
    plaintext = plaintext.upper().replace(" ", "")
    ciphertext = ""
    
    i = 0
    while i < len(plaintext):
        if i == len(plaintext) - 1:
            a, b = plaintext[i], 'X'
        elif plaintext[i] == plaintext[i+1]:
            a, b = plaintext[i], 'X'
            i -= 1
        else:
            a, b = plaintext[i], plaintext[i+1]
        
        encrypted_pair = encrypt_pair(key_square, a, b)
        ciphertext += ''.join(encrypted_pair)
        i += 2
    
    return ciphertext

def playfair_decrypt(key, ciphertext):
    key_square = generate_key_square(key)
    plaintext = ""
    
    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i+1]
        decrypted_pair = decrypt_pair(key_square, a, b)
        plaintext += ''.join(decrypted_pair)
    
    return plaintext.rstrip('X')

def encrypt_image(key_image_path, normal_image_path):
    # Open the images
    key_image = Image.open(key_image_path).convert('L')
    normal_image = Image.open(normal_image_path).convert('L')
    
    # Ensure both images have the same size
    if key_image.size != normal_image.size:
        raise ValueError("Key image and normal image must have the same dimensions")
    
    # Convert images to numpy arrays for easier processing
    key_array = np.array(key_image)
    normal_array = np.array(normal_image)
    
    # XOR the key and normal arrays
    encrypted_array = np.bitwise_xor(key_array, normal_array).astype(np.uint8)
    
    # Convert the encrypted array back to an image
    encrypted_image = Image.fromarray(encrypted_array)
    
    # Display images fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(20, 5))
    
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(20, 5))
    ax1.imshow(normal_image, cmap='gray')
    ax1.set_title('Original Image')
    ax1.axis('off')
    ax2.imshow(key_image, cmap='gray')
    ax2.set_title('Key Image')
    ax2.axis('off')
    ax3.imshow(encrypted_image, cmap='gray')
    ax3.set_title('Encrypted Image')
    ax3.axis('off')
    ax4.imshow(normal_image, cmap='gray')
    ax4.set_title('Decrypted Image')
    ax4.axis('off')
    plt.tight_layout()
    plt.show()

def main():
    while True:
        print("\nPlayfair Cipher Encryption/Decryption")
        print("1. Encrypt/Decrypt Text")
        print("2. Encrypt Image")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            key = input("Enter the key: ")
            plaintext = input("Enter the text to encrypt: ")
            ciphertext = playfair_encrypt(key, plaintext)
            decrypted_text = playfair_decrypt(key, ciphertext)
            print(f"\nKey: {key}")
            print(f"Plaintext: {plaintext}")
            print(f"Ciphertext: {ciphertext}")
            print(f"Decrypted text: {decrypted_text}")
        
        elif choice == '2':
            key_image_path = input("Enter the path to the key image: ")
            normal_image_path = input("Enter the path to the normal image: ")
            try:
                encrypt_image(key_image_path, normal_image_path)
            except FileNotFoundError:
                print("Error: Image file not found. Please check the paths and try again.")
            except ValueError as e:
                print(f"Error: {str(e)}")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
        
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()