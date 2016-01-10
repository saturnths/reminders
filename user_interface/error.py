from gi.repository import Gtk


def show_dialog(parent, msg):
    error_dialog = Gtk.MessageDialog(parent, 0, Gtk.MessageType.ERROR,
                                     Gtk.ButtonsType.OK, 'Validation error')
    error_dialog.format_secondary_text(msg)
    error_dialog.run()
    error_dialog.destroy()
