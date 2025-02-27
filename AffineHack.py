key_rev = {1:1, 3:9, 5:21, 7:15, 9:3, 11:19, 15:7, 17:23, 19:11, 21:5, 23:17, 25:25}
alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def generate_mapping(a, b):
    """
    Generate a dictionary mapping for uppercase letters based on Affine cypher.
    """
    a_rev = key_rev[a]
    mapping = {char: alphabets[((alphabets.index(char.upper()) - b) * a_rev) % 26] for char in alphabets}
    return mapping


def print_mapping_table(a, b):
    """
    Print the mapping for uppercase letters based on Affine cypher.
    """
    mapping = generate_mapping(a, b)
    col_width = 2  # width for each column for clarity

    # Build the border line
    border = " " + "+".join(["-" * col_width] * len(alphabets)) + " "

    # Build the row for plain letters
    plain_row = " " + " ".join(letter.center(col_width) for letter in alphabets) + " "
    # Build the row for cipher letters
    cipher_row = " " + " ".join(mapping[letter].center(col_width) for letter in alphabets) + " "

    #print(border)
    print(plain_row)
    print(border)
    print(cipher_row)
    #print(border)
    
def affineDecrypt(C, a, b):
    """
    Decrypt a cipher text using Affine cipher.
    """
    result = []
    for c in C:
        if c.upper() in alphabets:  # Kiểm tra cả chữ hoa và thường
            isLower = c.islower()
            index = alphabets.index(c.upper())
            index = (key_rev[a] * ((index - b) % 26)) % 26  # Sửa công thức
            result.append(alphabets[index].lower() if isLower else alphabets[index])
        else:
            result.append(c)  # Giữ nguyên ký tự không phải chữ cái
    return "".join(result)

    
def cryptanalysist_affine(ciphertext):
    """
    Analyze a ciphertext using Affine cypher to find possible values for a and b.
    """
    print("\nStarting cryptanalysis on the ciphertext...\n")
    for key1 in key_rev.keys():
        for key2 in range(0, 26):
            print(f"Trying a={key1} and b={key2}\n")
            print_mapping_table(key1, key2)
            decrypted_text = affineDecrypt(ciphertext, key1, key2)
            print(f"Decrypted text: {decrypted_text[:100]}")
            print("-" * 40)
            if input("Press Enter to continue or type 'q' to quit: ").strip().lower() == 'q':
                return
            
def main():
    ciphertext = input("Enter the ciphertext for cryptanalysis: ")
    cryptanalysist_affine(ciphertext)

if __name__ == "__main__":
    main()
    



    
    
