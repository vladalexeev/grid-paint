import datetime

from pages import cache
from common import BasicRequestHandler
import db


class CronCleanNotifications(BasicRequestHandler):
    def get(self, *args):
        date = datetime.datetime.now() - datetime.timedelta(days=90)
        notifications = db.Notification.all().filter('date <', date).fetch(200)
        for n in notifications:
            if n.recipient_email:
                cache.delete(cache.MC_USER_NOTIFICATION_PREFIX + n.recipient_email)
            n.delete()

        self.response.set_status(200)
        return
