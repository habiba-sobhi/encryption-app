from ciphers import caesar_encrypt, caesar_decrypt, vigenere_encrypt, vigenere_decrypt


def main():
    text = "Hello, Friend"

    print("=== Caesar ===")
    c_encrypted = caesar_encrypt(text, 3)
    c_decrypted = caesar_decrypt(c_encrypted, 3)
    print("Encrypted:", c_encrypted)
    print("Decrypted:", c_decrypted)

    print("\n=== Vigenère ===")
    v_encrypted = vigenere_encrypt(text, "KEY")
    v_decrypted = vigenere_decrypt(v_encrypted, "KEY")
    print("Encrypted:", v_encrypted)
    print("Decrypted:", v_decrypted)


if __name__ == "__main__":
    main()
