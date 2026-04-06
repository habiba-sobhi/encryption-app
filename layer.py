from ciphers import caesar_encrypt, caesar_decrypt, vigenere_encrypt, vigenere_decrypt


class Layer:
    def __init__(self):
        self.__layers = []

    def add_layer(self, layer_type, **params):
        self.__layers.append({"type": layer_type.lower(), "params": params})

    def process(self, text, mode="encrypt"):
        result = text
        layers = self.__layers if mode == "encrypt" else reversed(self.__layers)

        for layer in layers:
            if layer["type"] == "caesar":
                result = caesar_encrypt(result, layer["params"]["shift"]) if mode == "encrypt" else caesar_decrypt(
                    result, layer["params"]["shift"])
            elif layer["type"] == "vigenere":
                result = vigenere_encrypt(result, layer["params"]["key"]) if mode == "encrypt" else vigenere_decrypt(
                    result, layer["params"]["key"])
        return result

    def get_layers(self):
        return [layer.copy() for layer in self.__layers]
