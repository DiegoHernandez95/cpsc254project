import gi
import os
import time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from FileDropper import DragAndDrop
from IconFinder import IconFinder
from FileChooserWindow import FileChooserWindow
from KeyGenWindow import KeyGenWindow
from EncryptionMethodComboBox import EncryptionMethodComboBox
from CurrentPath import CurrentPath
from Encryptor import Encryptor
from Decryptor import Decryptor

css_provider = Gtk.CssProvider()
css_provider.load_from_path("styles.css")
Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(), 
    css_provider, 
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

project_dir = os.path.dirname(os.path.abspath(__file__))


# main class
# use command python3 FileEncryptor.py to run the program
# currently need to test this on other distros
# kali linux has a weird font issue
# ubuntu on wsl works just fine
class FileEncryptor:
    def __init__(self):
        # Load Glade file
        self.builder = Gtk.Builder()
        try:
            self.builder.add_from_file("FileEncryptor.glade")
        except Exception as e:
            print(f"Error loading Glade file: {e}")
            return
        self._selected_key_file = None
        # Get main window and widgets
        self.window = self.builder.get_object("MainWindow")
        self.drop_area = self.builder.get_object("DropArea")
        self.image_widget = self.builder.get_object("FileIcon")
        self.name_label = self.builder.get_object("FileNameLabel")
        self.size_label = self.builder.get_object("FileSizeLabel")
        self.date_label = self.builder.get_object("DateCreatedLabel")
        self.progress_label = self.builder.get_object("ProgressLabel")
        self.key_gen_window = self.builder.get_object("KeyGenWindow")
        self.generate_keys_button = self.builder.get_object("GenerateKeys")
        if self.generate_keys_button:
            self.generate_keys_button.connect("clicked", self.on_generate_keys_clicked)
        self.encrypt_combo_box = self.builder.get_object("EncryptionMethodComboBox")
        self.encrypt_button = self.builder.get_object("EncryptButton")
        if self.encrypt_button:
            self.encrypt_button.connect("clicked", self.on_encrypt_button_clicked)
        self.decrypt_button = self.builder.get_object("DecryptButton")
        if self.decrypt_button:
            self.decrypt_button.connect("clicked", self.on_decrypt_button_clicked)


        if not all([self.window, self.drop_area, self.image_widget, self.name_label, self.size_label, self.date_label, self.key_gen_window]):
            print("Error: One or more UI components could not be loaded.")
            return
        
        self.name_label.set_xalign(0.0)
        self.size_label.set_xalign(0.0)
        self.date_label.set_xalign(0.0)
        self.progress_label.set_xalign(0.0)

        # Connect signals
        self.builder.connect_signals(self)
        self.encrypt_combo_box.connect("changed", self.on_key_selected)
        
        # Set window properties
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.connect("destroy", Gtk.main_quit)
        self.window.show_all()
        
        self.name_label.set_visible(False)
        self.size_label.set_visible(False)
        self.date_label.set_visible(False)
        self.progress_label.set_visible(False)
        self.key_gen_window = KeyGenWindow(
            self.builder,
            on_update_callback=self.init_combo_box 
        )
        self.init_combo_box()

        # Initialize drag-and-drop functionality
        DragAndDrop(
            drop_target=self.drop_area,
            image_widget=self.image_widget,
            name_label=self.name_label,
            size_label=self.size_label,
            date_label=self.date_label,
        )
        
        # FileChooser functionality - pass builder
        self.file_chooser_window = FileChooserWindow(
            builder=self.builder,
            image_widget=self.image_widget,
            name_label=self.name_label,
            size_label=self.size_label,
            date_label=self.date_label,
        )
    
    # this is where users select their keys
    def init_combo_box(self):
        aes_keys_dir = os.path.join(".keys", "aes")
        rsa_keys_dir = os.path.join(".keys", "rsa")

        os.makedirs(aes_keys_dir, exist_ok=True)
        os.makedirs(rsa_keys_dir, exist_ok=True)

        # store the key names
        list_store = self.encrypt_combo_box.get_model()
        if list_store is None:
            list_store = Gtk.ListStore(str)
            self.encrypt_combo_box.set_model(list_store)
        else:
            list_store.clear()

        for aes_key in os.listdir(aes_keys_dir):
            list_store.append([f"AES: {aes_key}"])

        for rsa_key in os.listdir(rsa_keys_dir):
            list_store.append([f"RSA: {rsa_key}"])

        if len(self.encrypt_combo_box.get_cells()) == 0:
            renderer_text = Gtk.CellRendererText()
            self.encrypt_combo_box.pack_start(renderer_text, True)
            self.encrypt_combo_box.add_attribute(renderer_text, "text", 0)

        
    def on_key_selected(self, combo_box):
        tree_iter = combo_box.get_active_iter()
        if tree_iter is not None:
            model = combo_box.get_model()
            self._selected_key_file = model[tree_iter][0]
            print(f"Selected key file: {self._selected_key_file}")
            
    def on_encrypt_button_clicked(self, widget):
        if not self._selected_key_file:
            print("No key file selected!")
            dialog = Gtk.MessageDialog(
                parent=self.window,
                flags=0,
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.OK,
                text="Please select a key file from the combo box."
            )
            dialog.run()
            dialog.destroy()
            return

        file_path = CurrentPath.getFilePath()
        if not file_path:
            print("No file selected for encryption!")
            dialog = Gtk.MessageDialog(
                parent=self.window,
                flags=0,
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.OK,
                text="Please select a file to encrypt."
            )
            dialog.run()
            dialog.destroy()
            return

        if self._selected_key_file.startswith("AES:"):
            key_file_name = self._selected_key_file.split("AES: ")[1]
            key_file_path = os.path.join(".keys", "aes", key_file_name)
            encrypted_file = Encryptor.BeginEncryption(file_path, key_file_path, "AES")
        elif self._selected_key_file.startswith("RSA:"):
            key_file_name = self._selected_key_file.split("RSA: ")[1]
            key_file_path = os.path.join(".keys", "rsa", key_file_name)
            encrypted_file = Encryptor.BeginEncryption(file_path, key_file_path, "RSA")
        else:
            print("Unsupported key type selected!")
            dialog = Gtk.MessageDialog(
                parent=self.window,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Unsupported key type selected! Please select a valid RSA or AES key."
            )
            dialog.run()
            dialog.destroy()
            return

        if encrypted_file:
            print(f"File successfully encrypted: {encrypted_file}")
            self.progress_label.set_text(f"File successfully encrypted: {os.path.basename(encrypted_file)}")
        else:
            print("Error during encryption.")

        self.progress_label.set_visible(True)

        
    def on_decrypt_button_clicked(self, widget):
        if not self._selected_key_file:
            self._show_error_dialog("Please select a key file from the combo box.")
            return

        file_path = CurrentPath.getFilePath()
        if not file_path:
            self._show_error_dialog("Please select a file to decrypt.")
            return

        # Determine key type and path
        if self._selected_key_file.startswith("AES:"):
            key_file_name = self._selected_key_file.split("AES: ")[1]
            key_file_path = os.path.join(".keys", "aes", key_file_name)
            decrypted_file = Decryptor.BeginDecryption(file_path, key_file_path, "AES")
        elif self._selected_key_file.startswith("RSA:"):
            key_file_name = self._selected_key_file.split("RSA: ")[1]
            key_file_path = os.path.join(".keys", "rsa", key_file_name)
            decrypted_file = Decryptor.BeginDecryption(file_path, key_file_path, "RSA")
        else:
            self._show_error_dialog("Unsupported key type selected! Please select a valid RSA or AES key.")
            return

        # Handle decryption result
        if decrypted_file:
            print(f"File successfully decrypted: {decrypted_file}")
            self.progress_label.set_text(f"File successfully decrypted: {os.path.basename(decrypted_file)}")
        else:
            print("Error during decryption.")

        self.progress_label.set_visible(True)
    
    # if the secret key folder does not exist open folder creation dialog window create it
    # for the purpose of this program leave it in the project directory
    def on_generate_keys_clicked(self, widget):
        aes_keys_dir = os.path.join(project_dir, ".keys", "aes")
        rsa_keys_dir = os.path.join(project_dir, ".keys", "rsa")
    
        os.makedirs(aes_keys_dir, exist_ok=True)
        os.makedirs(rsa_keys_dir, exist_ok=True)
    
        self.key_gen_window.show()


if __name__ == "__main__":
    app = FileEncryptor()
    Gtk.main()
