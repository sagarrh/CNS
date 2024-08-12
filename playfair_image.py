import string

def generate_playfair_matrix(key):
    chars = string.ascii_uppercase + string.digits
    matrix = []
    used = set()
    
    key = ''.join(filter(str.isalnum, key)).upper()
    for char in key:
        if char not in used and char in chars:
            used.add(char)
            matrix.append(char)
    
    for char in chars:
        if char not in used:
            used.add(char)
            matrix.append(char)
    
    return [matrix[i:i+6] for i in range(0, 36, 6)]

def find_position(matrix, char):
    for r, row in enumerate(matrix):
        if char in row:
            return r, row.index(char)
    return None

def preprocess_text(text):
    text = ''.join(filter(str.isalnum, text)).upper()
    processed = []
    i = 0
    while i < len(text):
        processed.append(text[i])
        if i + 1 < len(text) and text[i] == text[i + 1]:
            processed.append('X')
        i += 1
    if len(processed) % 2 != 0:
        processed.append('X')
    return [processed[i:i+2] for i in range(0, len(processed), 2)]

def encrypt_digraph(matrix, digraph):
    r1, c1 = find_position(matrix, digraph[0])
    r2, c2 = find_position(matrix, digraph[1])
    
    if r1 == r2:
        return matrix[r1][(c1 + 1) % 6] + matrix[r2][(c2 + 1) % 6]
    elif c1 == c2:
        return matrix[(r1 + 1) % 6][c1] + matrix[(r2 + 1) % 6][c2]
    else:
        return matrix[r1][c2] + matrix[r2][c1]

def decrypt_digraph(matrix, digraph):
    r1, c1 = find_position(matrix, digraph[0])
    r2, c2 = find_position(matrix, digraph[1])
    
    if r1 == r2:
        return matrix[r1][(c1 - 1) % 6] + matrix[r2][(c2 - 1) % 6]
    elif c1 == c2:
        return matrix[(r1 - 1) % 6][c1] + matrix[(r2 - 1) % 6][c2]
    else:
        return matrix[r1][c2] + matrix[r2][c1]

def playfair_encrypt(key, text):
    matrix = generate_playfair_matrix(key)
    digraphs = preprocess_text(text)
    encrypted_text = ''.join(encrypt_digraph(matrix, dg) for dg in digraphs)
    return encrypted_text

def playfair_decrypt(key, text):
    matrix = generate_playfair_matrix(key)
    digraphs = [text[i:i+2] for i in range(0, len(text), 2)]
    decrypted_text = ''.join(decrypt_digraph(matrix, dg) for dg in digraphs)
    

    if decrypted_text.endswith('X'):
        decrypted_text = decrypted_text[:-1]
    return decrypted_text

key = input("Enter your key: ")
text = input("Enter your text: ")

encrypted_text = playfair_encrypt(key, text)
print("Encrypted Text:", encrypted_text)

decrypted_text = playfair_decrypt(key, encrypted_text)
print("Decrypted Text:", decrypted_text)

