from gi.repository import Gtk
from datetime import datetime


class AddDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Add a new reminder", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_border_width(6)
        self.box = self.get_content_area()

        self.create_textentry()
        self.create_textview()
        self.create_calendar()

        self.hbox = Gtk.HBox(homogeneous=False, spacing=0)
        self.box.add(self.hbox)

        # add time picker
        self.hr_btn = self.create_hour_sb()
        self.min_btn = self.create_minute_sb()
        self.sec_btn = self.create_sec_sb()

        self.show_all()

    def create_calendar(self):
        label = Gtk.Label("Date and time:")
        label.set_alignment(xalign=0, yalign=0.5)
        self.box.add(label)
        self.cal = Gtk.Calendar()
        self.box.add(self.cal)

    def create_textentry(self):
        label = Gtk.Label("Name:")
        label.set_alignment(xalign=0, yalign=0.5)
        self.box.add(label)
        self.name_entry = Gtk.Entry()
        self.box.add(self.name_entry)

    def create_textview(self):
        label = Gtk.Label("Content:")
        label.set_alignment(xalign=0, yalign=0.5)
        self.box.add(label)
        scrolled = Gtk.ScrolledWindow()

        valign = Gtk.Alignment()
        valign.set_padding(0, 5, 0, 0)
        valign.add(scrolled)
        self.box.add(valign)

        self.textview = Gtk.TextView()
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        scrolled.add(self.textview)

    def format_display(self, btn):
        adj = btn.get_adjustment()
        btn.set_text('{:02d}'.format(int(adj.get_value())))
        return True

    def create_hour_sb(self):
        adj = Gtk.Adjustment(0, 0, 23, 1, 10, 0)
        label = Gtk.Label("Hr:")
        self.hbox.pack_start(label, False, False, 5)
        spinbutton = Gtk.SpinButton()
        spinbutton.set_adjustment(adj)
        spinbutton.connect('output', self.format_display)
        self.hbox.pack_start(spinbutton, False, False, 5)
        return spinbutton

    def create_minute_sb(self):
        adj = Gtk.Adjustment(0, 0, 59, 1, 10, 0)
        label = Gtk.Label("Min:")
        self.hbox.pack_start(label, False, False, 5)
        spinbutton = Gtk.SpinButton()
        spinbutton.set_adjustment(adj)
        spinbutton.connect('output', self.format_display)
        self.hbox.pack_start(spinbutton, False, False, 5)
        return spinbutton

    def create_sec_sb(self):
        adj = Gtk.Adjustment(0, 0, 59, 1, 10, 0)
        label = Gtk.Label("Sec:")
        self.hbox.pack_start(label, False, False, 5)
        spinbutton = Gtk.SpinButton()
        spinbutton.set_adjustment(adj)
        spinbutton.connect('output', self.format_display)
        self.hbox.pack_start(spinbutton, False, False, 5)
        return spinbutton

    def get_new_reminder_data(self):
        buf = self.textview.get_buffer()
        descr = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)
        cal_date = self.cal.get_date()
        date = (cal_date[0], cal_date[1]+1, cal_date[2])
        title = self.name_entry.get_text()
        time = (self.hr_btn.get_value_as_int(), self.min_btn.get_value_as_int(),
                self.sec_btn.get_value_as_int())
        dt = datetime(*(date+time))

        return title, descr, dt
