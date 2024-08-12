def to_lower_case(s):
    return s.lower()

def remove_spaces(s):
    return ''.join(s.split())

def generate_key_table(key):
    key = key.lower()
    key = remove_spaces(key)
    key = key.replace('j', 'i')

    key_table = []
    used_chars = set()

    
    for char in key:
        if char not in used_chars and (char.isalpha() or char.isdigit()):
            used_chars.add(char)
            key_table.append(char)

    for char in 'abcdefghijklmnopqrstuvwxyz0123456789':
        if char not in used_chars and char != 'j':
            used_chars.add(char)
            key_table.append(char)

    key_table = [key_table[i:i + 6] for i in range(0, 36, 6)] 
    return key_table

def prepare(plain):
    if len(plain) % 2 != 0:
        plain += 'x'
    return plain

def mod6(a):
    return a % 6

def search(key_table, a, b):
    if a == 'j':
        a = 'i'
    if b == 'j':
        b = 'i'

    pos = {}
    for i, row in enumerate(key_table):
        for j, char in enumerate(row):
            pos[char] = (i, j)

    return pos[a], pos[b]

def encrypt(plain, key_table):
    plain = prepare(plain)
    encrypted_text = []

    for i in range(0, len(plain), 2):
        a, b = plain[i], plain[i + 1]
        (r1, c1), (r2, c2) = search(key_table, a, b)

        if r1 == r2:
            encrypted_text.append(key_table[r1][mod6(c1 + 1)])
            encrypted_text.append(key_table[r1][mod6(c1 + 2)])
        elif c1 == c2:
            encrypted_text.append(key_table[mod6(r1 + 1)][c1])
            encrypted_text.append(key_table[mod6(r2 + 1)][c2])
        else:
            encrypted_text.append(key_table[r1][c2])
            encrypted_text.append(key_table[r2][c1])

    return ''.join(encrypted_text)

def decrypt(cipher, key_table):
    cipher = prepare(cipher)
    decrypted_text = []

    for i in range(0, len(cipher), 2):
        a, b = cipher[i], cipher[i + 1]
        (r1, c1), (r2, c2) = search(key_table, a, b)

        if r1 == r2:
            decrypted_text.append(key_table[r1][mod6(c1 - 1)])
            decrypted_text.append(key_table[r1][mod6(c1 - 2)])
        elif c1 == c2:
            decrypted_text.append(key_table[mod6(r1 - 1)][c1])
            decrypted_text.append(key_table[mod6(r2 - 1)][c2])
        else:
            decrypted_text.append(key_table[r1][c2])
            decrypted_text.append(key_table[r2][c1])

    return ''.join(decrypted_text).replace('x', '')  

def encrypt_by_playfair_cipher(plaintext, key):
    generated_table = generate_key_table(key)
    plaintext = to_lower_case(plaintext)
    plaintext = remove_spaces(plaintext)
    return encrypt(plaintext, generated_table)

def decrypt_by_playfair_cipher(ciphertext, key):
    generated_table = generate_key_table(key)
    ciphertext = to_lower_case(ciphertext)
    ciphertext = remove_spaces(ciphertext)
    return decrypt(ciphertext, generated_table)

if __name__ == "__main__":
    key = input("Enter the key: ")
    plaintext = input("Enter plaintext: ")

    ciphered_text = encrypt_by_playfair_cipher(plaintext, key)
    decrypted_text = decrypt_by_playfair_cipher(ciphered_text, key)

    print(f"Key is: {key}")
    print(f"Plaintext is: {plaintext}")
    print(f"Ciphered text is: {ciphered_text}")
    print(f"Decrypted text is: {decrypted_text}")
