from gi.repository import Notify


def notify_user(title, msg):
    Notify.init("Reminder")
    n = Notify.Notification.new("Reminder: "+title, msg, "dialog-information")
    n.show()
