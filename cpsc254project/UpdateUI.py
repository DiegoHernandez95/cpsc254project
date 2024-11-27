import gi
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import GdkPixbuf

from IconFinder import IconFinder

# this class will update the file information screen with information about the file
# as soon as a file is loaded either through drag and drop or file search
# it will display information about the file
class UpdateUI:
    @staticmethod
    def update_ui_with_file(file_path, image_widget, name_label, size_label, date_label, file_info):
        # Truncate the file name if it's too long
        name = file_info["name"]
        truncated_name = name[:30] + "..." if len(name) > 30 else name
        name_label.set_markup(f'<span font="16">{truncated_name}</span>')
        name_label.set_tooltip_text(file_info["name"])
        # Set labels
        size_label.set_text(f"Size: {file_info['size_kb']:.2f} KB")
        date_label.set_text(f"Date Created: {file_info['formatted_time']}")

        # Update the icon
        pixbuf = IconFinder.load_generic_icon(file_path)
        if pixbuf:
            image_widget.set_from_pixbuf(pixbuf)
        else:
            print(f"Could not load icon for file: {file_path}")

