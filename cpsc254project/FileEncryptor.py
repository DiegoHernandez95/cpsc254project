import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MyApplication:
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("FileEncryptorGUI.glade")
        
        self.window = builder.get_object("MainWindow")
        self.Pub_Key_Entry = builder.get_object("Pub_Key_Entry")
        self.Pri_Key_Entry = builder.get_object("Pri_Key_Entry")
        
        builder.connect_signals({
            "GenPubKey_clicked_cb": self.GenPubKey_clicked_cb,
            "GenPriKey_clicked_cb": self.GenPriKey_clicked_cb,
            "on_main_window_destroy": Gtk.main_quit
        })
        
        self.window.show_all()
        
    def GenPubKey_clicked_cb(self, button):
        self.Pub_Key_Entry.set_text("Add Logic to generate a public key")
        
    def GenPriKey_clicked_cb(self, button):
        self.Pri_Key_Entry.set_text("Add Logic to generate a private key")
        
        
if __name__ == "__main__":
    app = MyApplication()
    Gtk.main()