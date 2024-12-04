import os
import mimetypes
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# this class uses generic icons based on the file extensions
class IconFinder:
    @staticmethod
    def load_generic_icon(file_path, size=64):
        icon_theme = Gtk.IconTheme.get_default()
        
        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lower()

        if file_extension in [".txt", ".log", ".csv", ".pem"]:
            icon_name = "text-x-generic"
        elif file_extension in [".jpg", ".jpeg", ".png", ".gif", ".bmp"]:
            icon_name = "image-x-generic"
        elif file_extension in [".mp4", ".avi", ".mkv", ".mov"]:
            icon_name = "video-x-generic"
        elif file_extension in [".mp3", ".wav", ".flac"]:
            icon_name = "audio-x-generic"
        elif file_extension in [".exe", ".bin", ".sh"]:
            icon_name = "application-x-executable"
        else:
            icon_name = "unknown"

        try:
            file_icon = icon_theme.load_icon(icon_name, size, 0)
        except Exception as e:
            print(f"Error loading icon: {e}")
            file_icon = None

        return file_icon

