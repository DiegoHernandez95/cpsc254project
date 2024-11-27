import gi
import os
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from FileInfoRetriever import FileInfoRetriever
from UpdateUI import UpdateUI
from CurrentPath import CurrentPath

# this class lets the user select a file from the file explorer
class FileChooserWindow:
    def __init__(self, builder, image_widget, name_label, size_label, date_label):
        self.image_widget = image_widget
        self.name_label = name_label
        self.size_label = size_label
        self.date_label = date_label

        self.builder = builder
        self.file_chooser_button = self.builder.get_object("FileChooserButton")
        
        # I probably should have put this in FileEncryptor.py
        # but I don't want to mess with the current structure of the program
        # getting this to work was such a nightmare
        if self.file_chooser_button:
            self.file_chooser_button.connect("file-set", self.FileChooserButton_file_set_cb)
        else:
            print("Error: FileChooserButton not found in Glade file.")

    def FileChooserButton_file_set_cb(self, widget):
        file_path = widget.get_filename()
        print(f"Retrieved file path: {file_path}")

        # in case the file path is none or an empty string
        if file_path and os.path.exists(file_path):
            CurrentPath.setFilePath(file_path)
            self.handle_file(file_path)
        else:
            print("File does not exist or path is invalid.")

    # kind of jank because FileDropper uses the same code.
    def handle_file(self, file_path):
        try:
            file_info = FileInfoRetriever.get_file_info(file_path)
            print(f"File info: {file_info}")  
            UpdateUI.update_ui_with_file(
                file_path,
                self.image_widget,
                self.name_label,
                self.size_label,
                self.date_label,
                file_info
            )
            self.name_label.set_visible(True)
            self.size_label.set_visible(True)
            self.date_label.set_visible(True)
        except Exception as e:
            print(f"Error handling file: {e}")
