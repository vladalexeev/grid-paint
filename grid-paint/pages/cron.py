import datetime
import json

from bad_language import hide_bad_language
from pages import cache
from common import BasicRequestHandler
import db
import dao
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


def get_task_status(task_name):
    return db.TaskStatus.all().filter('task_name =', task_name).get()


class CronUpdateArtworks(BasicRequestHandler):
    def get(self):
        task_name = 'update_artworks_tags'
        task_status = get_task_status(task_name)
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
            'total': 0,
        }

        artworks = db.Artwork.all().filter('date >', task_status.last_date).order('date').fetch(200)
        for a in artworks:
            task_log_data['total'] = task_log_data['total'] + 1
            task_status.last_date = a.date
            changed = False
            new_name = hide_bad_language(a.name)
            new_description = hide_bad_language(a.description)
            if new_name != a.name or new_description != a.description:
                task_log_data['bad_language'] = task_log_data['bad_language'] + 1
                if 'bad_images' not in task_log_data:
                    task_log_data['bad_images'] = []
                task_log_data['bad_images'].append(a.key().id())

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


class CronUpdateGlobalTags(BasicRequestHandler):
    def get(self):
        task_name = 'update_global_tags'
        task_status = get_task_status(task_name)
        if not task_status:
            task_status = db.TaskStatus()
            task_status.task_name = task_name
            task_status.finished = False
            task_status.data = json.dumps({
                'last_url_name': 0,
            })

        if task_status.finished:
            self.response.set_status(200)
            return

        task_data = json.loads(task_status.data)
        last_url_name = task_data['last_url_name']
        tags = db.Tag.all().filter('url_name >', last_url_name).order('url_name').fetch(100, 0)
        artworks_processed = 0
        tags_processed = 0
        for t in tags:
            if artworks_processed > 1000:
                break
            tags_processed += 1
            url_name = t.url_name
            artworks = db.Artwork.all().filter('tags =', url_name)
            global_tag_count = 0
            users_tag_count = {}
            for a in artworks:
                global_tag_count += 1
                artworks_processed += 1
                author_email = a.author_email
                if author_email in users_tag_count:
                    users_tag_count[author_email] += 1
                else:
                    users_tag_count[author_email] = 1

            t.count = global_tag_count
            t.put()

            for email, count in users_tag_count:
                user = dao.get_user_profile(email)
                user_tag = db.UserTag.all().filter('user_id', user.key().id()).filter('url_name', url_name).get()
                if not user_tag:
                    user_tag = db.UserTag()
                    user_tag.user_id = user.key().id()
                    user_tag.url_name = url_name
                    user_tag.count = count
                    user_tag.put()

            last_url_name = url_name

        if tags_processed == 0:
            task_status.finished = True
        task_status.data = json.dumps({
            'last_url_name': last_url_name
        })
        task_status.put()


