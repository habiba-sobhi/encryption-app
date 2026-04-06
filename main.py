import tkinter as tk
from tkinter import ttk, messagebox
from ciphers import caesar_encrypt, caesar_decrypt, vigenere_encrypt, vigenere_decrypt


# Include the Layer class with get_layers() method
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

    def clear_layers(self):
        self.__layers.clear()


class CipherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Cipher Encryptor")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        self.layer_manager = Layer()  # Our multi-layer manager

        self.create_widgets()

    def create_widgets(self):
        # Input Text
        tk.Label(self.root, text="Text:").pack(pady=5)
        self.text_input = tk.Text(self.root, height=5, width=70)
        self.text_input.pack()

        # Cipher Type Dropdown
        tk.Label(self.root, text="Cipher Type:").pack(pady=5)
        self.cipher_type = ttk.Combobox(self.root, values=["Caesar", "Vigenère"], state="readonly")
        self.cipher_type.current(0)
        self.cipher_type.pack()

        # Key / Shift Entry
        self.key_label = tk.Label(self.root, text="Shift (Caesar) or Key (Vigenère):")
        self.key_label.pack(pady=5)
        self.key_entry = tk.Entry(self.root, width=30)
        self.key_entry.pack()

        # Add Layer Button
        tk.Button(self.root, text="Add Layer", command=self.add_layer).pack(pady=5)

        # Layers Listbox
        tk.Label(self.root, text="Added Layers:").pack(pady=5)
        self.layer_listbox = tk.Listbox(self.root, height=8, width=50)
        self.layer_listbox.pack()

        # Remove Layer Button
        tk.Button(self.root, text="Remove Selected Layer", command=self.remove_selected_layer).pack(pady=5)
        # Clear all layers
        tk.Button(self.root, text="Clear All Layers", command=self.clear_layers).pack(pady=5)

        # Buttons for encryption/decryption using layers
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        tk.Button(frame, text="Encrypt (All Layers)", command=self.encrypt).grid(row=0, column=0, padx=10)
        tk.Button(frame, text="Decrypt (All Layers)", command=self.decrypt).grid(row=0, column=1, padx=10)

        # Output Text
        tk.Label(self.root, text="Result:").pack(pady=5)
        self.result_box = tk.Text(self.root, height=5, width=70, state='disabled')
        self.result_box.pack()

        # Copy to Clipboard Button
        tk.Button(self.root, text="Copy to Clipboard", command=self.copy_to_clipboard).pack(pady=5)

    def add_layer(self):
        cipher = self.cipher_type.get().lower()
        key = self.key_entry.get().strip()

        if cipher == "caesar":
            if not key.isdigit():
                messagebox.showerror("Error", "Shift must be a number for Caesar cipher.")
                return
            shift = int(key)
            self.layer_manager.add_layer("caesar", shift=shift)
            self.layer_listbox.insert(tk.END, f"Caesar (shift={shift})")

        elif cipher == "vigenère":
            if not key.isalpha():
                messagebox.showerror("Error", "Key must be alphabetic for Vigenère cipher.")
                return
            self.layer_manager.add_layer("vigenere", key=key)
            self.layer_listbox.insert(tk.END, f"Vigenère (key='{key}')")

        self.key_entry.delete(0, tk.END)

    def remove_selected_layer(self):
        selection = self.layer_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "No layer selected to remove.")
            return
        index = selection[0]
        self.layer_listbox.delete(index)
        # Remove from Layer manager (private, so hacky approach)
        # We'll rebuild the list minus the removed layer
        layers = self.layer_manager.get_layers()
        layers.pop(index)
        self.layer_manager.clear_layers()
        for layer in layers:
            self.layer_manager.add_layer(layer["type"], **layer["params"])

    def clear_layers(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all layers?"):
            self.layer_listbox.delete(0, tk.END)
            self.layer_manager.clear_layers()

    def encrypt(self):
        self.process_text("encrypt")

    def decrypt(self):
        self.process_text("decrypt")

    def process_text(self, mode):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("Error", "Please enter some text to process.")
            return
        if not self.layer_manager.get_layers():
            messagebox.showerror("Error", "Please add at least one encryption layer.")
            return

        try:
            result = self.layer_manager.process(text, mode=mode)
            self.result_box.configure(state='normal')
            self.result_box.delete("1.0", tk.END)
            self.result_box.insert(tk.END, result)
            self.result_box.configure(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def copy_to_clipboard(self):
        result = self.result_box.get("1.0", tk.END).strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            messagebox.showinfo("Copied", "Result copied to clipboard.")
        else:
            messagebox.showwarning("Warning", "Nothing to copy.")


if __name__ == "__main__":
    root = tk.Tk()
    app = CipherGUI(root)
    root.mainloop()
