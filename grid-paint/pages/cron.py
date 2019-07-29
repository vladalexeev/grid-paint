import datetime
import json

from bad_language import hide_bad_language
from pages import cache
from common import BasicRequestHandler
import db
from tags import tag_url_name


class CronCleanNotifications(BasicRequestHandler):
    def get(self):
        date = datetime.datetime.now() - datetime.timedelta(days=90)
        notifications = db.Notification.all().filter('date <', date).fetch(100)
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
            task_status.finished = False
            task_status.data = json.dumps({
                'bad_language': 0,
                'tags': 0,
                'total': 0,
                'iteration': 0
            })

        if task_status.finished:
            self.response.set_status(200)
            return

        task_log_data = {
            'bad_language': 0,
            'tags': 0,
            'total': 0
        }

        artworks = db.Artwork.all().filter('date >', task_status.last_date).order('date').fetch(200)
        for a in artworks:
            task_log_data['total'] = task_log_data['total'] + 1
            task_status.last_date = a.date
            changed = False
            new_name = hide_bad_language(a.name)
            new_description = hide_bad_language(a.description)
            if new_name != a.name or new_description != a.description:
                changed = True
                a.name = new_name
                a.description = new_description
                task_log_data['bad_language'] = task_log_data['bad_language'] + 1

            if a.tags:
                new_tags = [tag_url_name(t) for t in a.tags]
                if a.tags != new_tags:
                    changed = True
                    a.tags = new_tags
                    task_log_data['tags'] = task_log_data['tags'] + 1

            if changed:
                a.put()

        task_log = db.TaskLog()
        task_log.date = datetime.datetime.now()
        task_log.task_name = task_status.task_name
        task_log.data = json.dumps(task_log_data)
        task_log.put()

        task_data = json.loads(task_status.data)
        task_data['bad_language'] = task_data['bad_language'] + task_log_data['bad_language']
        task_data['tags'] = task_data['tags'] + task_log_data['tags']
        task_data['total'] = task_data['total'] + task_log_data['total']
        task_data['iteration'] = task_data['iteration'] + 1

        task_status.data = json.dumps(task_data)
        task_status.finished = (task_log_data['total'] == 0)
        task_status.put()

        self.response.set_status(200)
