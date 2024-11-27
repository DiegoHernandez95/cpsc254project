import os
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# this class generates AES-256 keys and RSA keys using the pycryptodome library
# it'll be listed in the readme.
# it also uses on_update_callback to refresh the UI on closing the window
class KeyGenWindow:
    def __init__(self, builder, on_update_callback=None):
        self.builder = builder
        self.on_update_callback = on_update_callback
        self.window = self.builder.get_object("KeyGenWindow")
        self.aes_file_name_entry = self.builder.get_object("AESFileNameEntry")
        self.aes_key_gen_button = self.builder.get_object("AESKeyGenButton")
        self.rsa_file_name_entry = self.builder.get_object("RSAFileNameEntry")
        self.rsa_key_gen_button = self.builder.get_object("RSAKeyGenButton")

        self.aes_key_gen_button.connect("clicked", self.generate_aes_key)
        self.rsa_key_gen_button.connect("clicked", self.generate_rsa_key)
        self.window.connect("delete-event", self.on_close)
        self.window.set_position(Gtk.WindowPosition.CENTER)

    def show(self):
        self.window.show_all()

    def on_close(self, widget, event):
        if self.on_update_callback:
            self.on_update_callback()
        self.window.hide()
        return True 

    def generate_aes_key(self, widget):
        file_name = self.aes_file_name_entry.get_text().strip()
        if file_name:
            key = get_random_bytes(32)
            self.save_key(key, f".keys/aes/{file_name}.key")
            self.show_message(f"AES key saved as {file_name}")
        else:
            self.show_message("Please provide a valid AES file name.")

    def generate_rsa_key(self, widget):
        file_name = self.rsa_file_name_entry.get_text().strip()
        if file_name:
            key = RSA.generate(2048)
            self.save_key(key.export_key(), f".keys/rsa/{file_name}_private.pem")
            self.save_key(key.publickey().export_key(), f".keys/rsa/{file_name}_public.pem")
            self.show_message(f"RSA keys saved as {file_name}")
        else:
            self.show_message("Please provide a valid RSA file name.")

    def save_key(self, key_data, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as key_file:
            key_file.write(key_data)

    def show_message(self, message):
        dialog = Gtk.MessageDialog(
            parent=self.window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=message,
        )
        dialog.run()
        dialog.destroy()
