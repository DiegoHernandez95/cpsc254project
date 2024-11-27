import gi
import os
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# using a combo box so the user can select which keys they want to use for encryption and decryption
class EncryptionMethodComboBox:
    def __init__(self):
        self.combo_box = Gtk.ComboBoxText()
        self.combo_box.set_entry_text_column(0)
        self.populate_combo_box()
    
    def populate_combo_box(self):
        aes_keys_dir = os.path.join(".keys", "aes")
        rsa_keys_dir = os.path.join(".keys", "rsa")

        os.makedirs(aes_keys_dir, exist_ok=True)
        os.makedirs(rsa_keys_dir, exist_ok=True)

        # Add AES keys
        for aes_key in os.listdir(aes_keys_dir):
            self.combo_box.append_text(f"AES: {aes_key}")

        # Add RSA keys
        for rsa_key in os.listdir(rsa_keys_dir):
            self.combo_box.append_text(f"RSA: {rsa_key}")


    def get_selected_file(self):
        return self.combo_box.get_active_text()