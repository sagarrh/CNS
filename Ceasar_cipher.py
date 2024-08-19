import os
from PIL import Image

def encrypt_text(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    return result

def decrypt_text(text, shift):
    return encrypt_text(text, -shift)

def encrypt_image(image_path, shift):
    img = Image.open(image_path)
    width, height = img.size
    encrypted_img = Image.new(img.mode, img.size)
    
    for x in range(width):
        for y in range(height):
            r, g, b = img.getpixel((x, y))
            encrypted_img.putpixel((x, y), (
                (r + shift) % 256,
                (g + shift) % 256,
                (b + shift) % 256
            ))
    
    encrypted_path = f"encrypted_{os.path.basename(image_path)}"
    encrypted_img.save(encrypted_path)
    return encrypted_path

def decrypt_image(image_path, shift):
    return encrypt_image(image_path, -shift)

def main():
    while True:
        print("\nCaesar Cipher Menu:")
        print("1. Encrypt Text")
        print("2. Decrypt Text")
        print("3. Encrypt Image")
        print("4. Decrypt Image")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            text = input("Enter text to encrypt: ")
            shift = int(input("Enter shift value: "))
            print("Encrypted text:", encrypt_text(text, shift))
        
        elif choice == '2':
            text = input("Enter text to decrypt: ")
            shift = int(input("Enter shift value: "))
            print("Decrypted text:", decrypt_text(text, shift))
        
        elif choice == '3':
            image_path = input("Enter image path to encrypt: ")
            shift = int(input("Enter shift value: "))
            encrypted_path = encrypt_image(image_path, shift)
            print(f"Encrypted image saved as: {encrypted_path}")
        
        elif choice == '4':
            image_path = input("Enter image path to decrypt: ")
            shift = int(input("Enter shift value: "))
            decrypted_path = decrypt_image(image_path, shift)
            print(f"Decrypted image saved as: {decrypted_path}")
        
        elif choice == '5':
            print("Exiting program. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()