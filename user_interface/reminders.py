import logging
import database
import notification
from datetime import datetime
from gi.repository import Gtk
from apscheduler.schedulers.background import BackgroundScheduler
from . import add, error


class Reminders(Gtk.Window):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        Gtk.Window.__init__(self, title="Reminders")
        self.set_border_width(6)
        self.set_default_size(420, 200)
        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.create_treelist()
        self.create_add_btn()
        self.create_del_btn()
        self.load_reminders()
        self.show_all()

    def create_treelist(self):
        columns = ["Id", "Name", "Description", "Date", "Time"]
        self.store = Gtk.ListStore(int, str, str, str, str)
        self.treeview = Gtk.TreeView.new_with_model(self.store)

        for i, header in enumerate(columns):
            cell = Gtk.CellRendererText()
            col = Gtk.TreeViewColumn(header, cell, text=i)
            col.set_min_width(100)
            if header == 'Id':
                col.set_visible(False)
            self.treeview.append_column(col)

        self.scrollable_treelist = Gtk.ScrolledWindow(hexpand=True)
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)
        self.scrollable_treelist.add(self.treeview)

    def create_add_btn(self):
        self.add_btn = Gtk.Button("Add")
        self.add_btn.connect("clicked", self.on_add_btn_click)
        self.grid.attach_next_to(self.add_btn, self.scrollable_treelist,
                                 Gtk.PositionType.BOTTOM, 1, 2)

    def create_del_btn(self):
        self.del_btn = Gtk.Button("Delete")
        self.del_btn.connect("clicked", self.on_del_btn_click)
        self.grid.attach_next_to(self.del_btn, self.add_btn,
                                 Gtk.PositionType.RIGHT, 1, 1)

    def on_add_btn_click(self, widget):
        dialog = add.AddDialog(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            reminder = dialog.get_new_reminder_data()
            # validation
            title = reminder[0]
            dt = reminder[2]
            if title == '':
                error.show_dialog(self, 'The title is missing.')
                dialog.destroy()
                return self.on_add_btn_click(widget)
            if dt < datetime.now():
                error.show_dialog(self, 'The date and time are set in the past.')
                dialog.destroy()
                return self.on_add_btn_click(widget)
            self.add_row(reminder)
            self.logger.info('User added a new reminder')
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    def add_row(self, reminder):
        name = reminder[0]
        description = reminder[1]
        dt = reminder[2]
        date = str(dt.date())
        time = str(dt.time())
        r_id = database.add_reminder(name, description, str(dt))
        self.store.append([r_id, name, description, date, time])
        self.add_job(r_id, name, description, dt)

    def on_del_btn_click(self, btn):
        self.remove_from_list(self.get_id_of_selected_item())

    def get_id_of_selected_item(self):
        sel = self.treeview.get_selection()
        (model, selected) = sel.get_selected_rows()
        for s in selected:
            t_iter = model.get_iter(s)
            id = model.get_value(t_iter, 0)
            return id

    def remove_from_list(self, r_id):
        for row in self.store:
            if row[0] == r_id:
                self.store.remove(row.iter)
                database.remove_reminder(r_id)
                break

    def load_reminders(self):
        reminders = database.get_reminders()

        if len(reminders) <= 0:
            self.logger.info('No reminders were available to be scheduled')
            return

        for reminder in reminders:
            r_id = reminder[0]
            name = reminder[1]
            description = reminder[2]
            date_time = datetime.strptime(reminder[3], "%Y-%m-%d %H:%M:%S")
            date = str(date_time.date())
            time = str(date_time.time())
            if date_time > datetime.now():
                self.logger.info('Scheduling an existing reminder')
                self.store.append([r_id, name, description, date, time])
                self.add_job(r_id, name, description, date_time)
            else:
                self.logger.info('Removing an expired reminder')
                database.remove_reminder(r_id)

    def add_job(self, r_id, title, msg, date_time):
        sched = BackgroundScheduler()
        sched.add_job(self.job_message, 'date', run_date=date_time,
                      args=[r_id, title, msg])
        sched.start()

    def job_message(self, r_id, title, msg):
        notification.notify_user(title, msg)
        self.remove_from_list(r_id)
        database.remove_reminder(r_id)


def init():
    win = Reminders()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
