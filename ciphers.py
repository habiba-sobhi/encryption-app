def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            result += chr((ord(char) - offset + shift) % 26 + offset)
        else:
            result += char
    return result


def caesar_decrypt(text, shift):
    result = ""

    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            decrypted_char = chr((ord(char) - offset - shift) % 26 + offset)
            result += decrypted_char
        else:
            result += char
    return result


def vigenere_encrypt(text, key):
    result = []
    key = key.lower()
    key_index = 0
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            k = ord(key[key_index % len(key)]) - 97
            result.append(chr((ord(char) - offset + k) % 26 + offset))
            key_index += 1
        else:
            result.append(char)
    return "".join(result)


def vigenere_decrypt(text, key):
    result = []
    key = key.lower()
    key_index = 0
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            k = ord(key[key_index % len(key)]) - 97
            result.append(chr((ord(char) - offset - k + 26) % 26 + offset))
            key_index += 1
        else:
            result.append(char)
    return "".join(result)
