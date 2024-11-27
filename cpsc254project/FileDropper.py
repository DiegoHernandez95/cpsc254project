import gi
import os
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from FileInfoRetriever import FileInfoRetriever
from UpdateUI import UpdateUI
from CurrentPath import CurrentPath

# this function add lets the user drag files from their desktop in to the left corner of the screen
# it will upload the file path of the selected file and update the labels with information about the file
# as well as showing a generic icon 
class DragAndDrop:
    def __init__(self, drop_target, image_widget, name_label, size_label, date_label):
        self.image_widget = image_widget
        self.name_label = name_label
        self.size_label = size_label
        self.date_label = date_label

        drop_target.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
        drop_target.drag_dest_add_uri_targets()
        drop_target.connect("drag-data-received", self.on_drag_data_received)

    def on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
        uris = data.get_uris()
        if uris:
            file_path = uris[0][7:]
            if os.path.exists(file_path):
                CurrentPath.setFilePath(file_path)
                self.handle_file(file_path)
            else:
                print("File does not exist.")

    def handle_file(self, file_path):
        try:
            file_info = FileInfoRetriever.get_file_info(file_path)
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
        except FileNotFoundError as e:
            print(e)
