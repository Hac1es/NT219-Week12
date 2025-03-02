import numpy as np

# Define the alphabet and the modulus
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_ "
mod = 28 

def is_invertible(matrix):
    """ 
    Check if a given matrix has an inverse in modulo 28
    """
    det = int(round(np.linalg.det(matrix))) % mod
    try:
        pow(det, -1, mod)
        return True
    except ValueError:
        return False

def generate_valid_matrix(n):
    """ 
    Generate an n x n random matrix that is invertible modulo 28
    """
    while True:
        matrix = np.random.randint(0, mod, size=(n, n))  # Generate random values from 0 to 27
        if is_invertible(matrix):
            return matrix

def inverse_matrix(matrix):
    """
    Compute the modular inverse of an n x n matrix
    """
    n = matrix.shape[0]
    
    # Calcuate the modulo 28 determinant
    det = int(round(np.linalg.det(matrix))) % mod
    
    # Check whether the matrix has determinant or not
    try:
        inverse_det = pow(det, -1, mod)
    except ValueError:
        return None

    # Calcuate the adjugate matrix
    cofactor_matrix = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            minor = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
            cofactor = int(round(np.linalg.det(minor))) * ((-1) ** (i + j))
            cofactor_matrix[i, j] = cofactor
    adjugate_matrix = cofactor_matrix.T
    
    # Caculate 
    inverse_matrix = (inverse_det * adjugate_matrix) % mod

    return np.mod(inverse_matrix, mod)

def encrypt(text, cipherMatrix, n):
    """
    Encrypt a given text using Hill Cipher of size n x n
    """
    result = []

    # Standardize the text
    text = text.upper().replace("\n", " ").replace("\t", " ")
    while len(text) % n != 0:
        text += '_'

    text_numbers = [alphabet.index(char) for char in text]

    # Encrypt text in n-character blocks
    for i in range(0, len(text_numbers), n):
        block = np.array(text_numbers[i:i+n]).reshape(n, 1)
        encrypted_block = np.dot(cipherMatrix, block) % mod
        result.extend(encrypted_block.flatten())

    # Convert back to characters
    return ''.join(alphabet[num] for num in result)

def decrypt(encrypted_text, inverseMatrix, n):
    """
    Decrypt text that was encrypted using Hill Cipher of size n x n
    """
    result = []

    encrypted_numbers = [alphabet.index(char) for char in encrypted_text]

    # Decrypt text in n-character blocks
    for i in range(0, len(encrypted_numbers), n):
        block = np.array(encrypted_numbers[i:i+n]).reshape(n, 1)
        decrypted_block = np.dot(inverseMatrix, block) % mod
        result.extend(decrypted_block.flatten())

    return ''.join(alphabet[num] for num in result)

def print_matrix(matrix, title="Matrix"):
    """
    Pretty-print a matrix with a title.
    """
    print(f"\n{title}:")
    for row in matrix:
        print("  ".join(f"{num:2}" for num in row))

def main():
    try:
        n = int(input("Enter matrix size (2, 3, or 4): "))
        if n not in {2, 3, 4}:
            print("Only 2x2, 3x3, and 4x4 matrices are supported.")
            return

        choice = input("Do you want to enter the matrix manually? (y to Yes, others to No): ").strip().lower()
        
        if choice == 'y':
            print(f"Enter {n}x{n} encryption matrix row by row:")
            matrix_data = []
            for i in range(n):
                row = list(map(int, input(f"Row {i+1}: ").split()))
                if len(row) != n:
                    print(f"Each row must have exactly {n} numbers.")
                    return
                matrix_data.append(row)
            cipherMatrix = np.array(matrix_data)

            if not is_invertible(cipherMatrix):
                print("The entered matrix is not invertible mod 28. Please try again.")
                return
        else:
            print(f"Generating a valid {n}x{n} encryption matrix...")
            cipherMatrix = generate_valid_matrix(n)
            
        inverseMatrix = inverse_matrix(cipherMatrix)
    except ValueError:
        print("Invalid input. Please enter integers for the matrix.")
        return
    
    print_matrix(cipherMatrix, "Cipher Matrix")
    plaintext = input("\nEnter the text to encrypt: ")
    encrypted_text = encrypt(plaintext, cipherMatrix, n)
    print("\nEncrypted text:")
    print(encrypted_text)

    input("\nPress Enter to continue to decryption...")

    decrypted_text = decrypt(encrypted_text, inverseMatrix, n)
    print("\nDecrypted text:")
    print(decrypted_text)
        

if __name__ == "__main__":
    main()
