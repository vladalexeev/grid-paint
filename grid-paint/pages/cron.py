import datetime

from pages import cache
from common import BasicRequestHandler
import db


class CronCleanNotifications(BasicRequestHandler):
    def get(self):
        date = datetime.datetime.now() - datetime.timedelta(days=90)
        notifications = db.Notification.all().filter('date <', date).fetch(200)
        for n in notifications:
            if n.recipient_email:
                cache.delete(cache.MC_USER_NOTIFICATION_PREFIX + n.recipient_email)
            n.delete()

        self.response.set_status(200)
        return


class CronUpdateArtworks(BasicRequestHandler):
    def get(self):
        task_name = 'update_artworks_tags'
        task_status = db.TaskStatus.all().filter('task_name =', task_name).get()
        if not task_status:
            task_status = db.TaskStatus()
            task_status.task_name = task_name
            task_status.last_date = datetime.datetime(2012, 1, 1)

        artworks = db.Artwork.all().filter('date >', task_status.last_date).order('date').fetch(200)
        for a in artworks:
            task_status.last_date = a.date

        task_status.put()