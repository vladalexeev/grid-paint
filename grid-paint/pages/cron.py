import datetime
import json

from bad_language import hide_bad_language
from pages import cache
from common import BasicRequestHandler
import db
import dao
from tags import tag_url_name


class CronCleanNotifications(BasicRequestHandler):
    """
    Delete notifications older than 90 days
    """
    def get(self):
        date = datetime.datetime.now() - datetime.timedelta(days=90)
        notifications = db.Notification.all().filter('date <', date).fetch(100)
        for n in notifications:
            if n.recipient_email:
                cache.delete(cache.MC_USER_NOTIFICATION_PREFIX + n.recipient_email)
            n.delete()

        self.response.set_status(200)


class CronCleanOldNews(BasicRequestHandler):
    """
    Delete old news from newsfeed older than 90 days
    """
    def get(self):
        date = datetime.datetime.now() - datetime.timedelta(days=90)
        news = db.NewsFeed.all().filter('date <', date).fetch(200)
        for n in news:
            n.delete()
        self.response.set_status(200)


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
                'tags_processed': 0,
                'artworks_processed': 0,
            })

        if task_status.finished:
            self.response.set_status(200)
            return

        limit = 100
        max_artworks = 1000

        task_data = json.loads(task_status.data)
        last_url_name = task_data['last_url_name']
        tags = db.Tag.all().filter('url_name >', last_url_name).order('url_name').fetch(limit, 0)
        artworks_processed = 0
        tags_processed = 0
        for t in tags:
            if artworks_processed >= max_artworks:
                break
            tags_processed += 1
            url_name = t.url_name
            artworks = db.Artwork.all().filter('tags =', url_name)
            global_tag_count = 0
            users_tag_count = {}
            users_tag_last_date = {}
            users_tag_cover = {}
            min_artwork_date = None
            max_artwork_date = None
            for a in artworks:
                global_tag_count += 1
                artworks_processed += 1
                author_email = a.author_email
                if min_artwork_date is None:
                    min_artwork_date = a.date
                elif a.date < min_artwork_date:
                    min_artwork_date = a.date

                if max_artwork_date is None:
                    max_artwork_date = a.date
                elif a.date > max_artwork_date:
                    max_artwork_date = a.date

                if author_email in users_tag_count:
                    users_tag_count[author_email] += 1
                    if a.date > users_tag_last_date[author_email]:
                        users_tag_last_date[author_email] = a.date
                        users_tag_cover[author_email] = a
                else:
                    users_tag_count[author_email] = 1
                    users_tag_cover[author_email] = a
                    users_tag_last_date[author_email] = a.date

            t.count = global_tag_count
            t.date = min_artwork_date
            t.last_date = max_artwork_date
            t.put()

            for email, count in users_tag_count.iteritems():
                if email is None:
                    continue
                user = dao.get_user_profile(email)
                user_tag = db.UserTag.all().filter('user_id', user.key().id()).filter('url_name', url_name).get()
                if not user_tag:
                    user_tag = db.UserTag()
                user_tag.user_id = user.key().id()
                user_tag.url_name = t.url_name
                user_tag.title = t.title
                user_tag.title_lower = t.title_lower
                user_tag.date = datetime.datetime.now()
                user_tag.last_date = users_tag_last_date[email]
                user_tag.cover = users_tag_cover[email]
                user_tag.count = count
                user_tag.put()

            last_url_name = url_name

        task_log = db.TaskLog()
        task_log.task_name = task_name
        task_log.data = json.dumps({
            'tags_processed': tags_processed,
            'artworks_processed': artworks_processed,
            'last_url_name': last_url_name
        })
        task_log.put()

        if tags_processed == 0:
            task_status.finished = True
        task_data['last_url_name'] = last_url_name
        task_data['tags_processed'] += tags_processed
        task_data['artworks_processed'] += artworks_processed
        task_status.data = json.dumps(task_data)
        task_status.put()


class CronUpdateDailyCounters(BasicRequestHandler):
    """
    Move today's counters to daily counters and delete delete old counters
    """
    def get(self):
        today_counters = db.TodayFavoriteCounter.all().order('-count').fetch(100)

        # Copy top 100 counters to DailyFavoriteCounters
        for c in today_counters:
            daily_counter = db.DailyFavoritesCounters()
            daily_counter.artwork = c.artwork
            daily_counter.count = c.count
            daily_counter.save()

        # Clean TodayFavoriteCounter
        while True:
            deleted = False
            today_counters = db.TodayFavoriteCounter.all().order('-count').fetch(1000)
            for c in today_counters:
                c.delete()
                deleted = True
            if not deleted:
                break

        # Delete old daily counters
        old_counter_threshold = datetime.datetime.now() - datetime.timedelta(days=30)
        old_daily_counters = db.DailyFavoritesCounters.all().filter('date <', old_counter_threshold)
        for c in old_daily_counters:
            c.delete()


class CronCalculateLastWeekTop(BasicRequestHandler):
    """
    Calculate most popular artworks for week
    """
    def get(self):
        threshold = datetime.datetime.now() - datetime.timedelta(days=7)
        artwork_id__count = {}
        artwork_id__artwork = {}
        offset = 0
        limit = 1000
        while True:
            daily_counters = db.DailyFavoritesCounters.all().filter('date >', threshold).order('-date').fetch(limit, offset)
            empty = True
            for c in daily_counters:
                empty = False
                artwork_id = c.artwork.key().id()
                if artwork_id in artwork_id__count:
                    artwork_id__count[artwork_id] = artwork_id__count[artwork_id] + c.count
                else:
                    artwork_id__count[artwork_id] = c.count
                    artwork_id__artwork[artwork_id] = c.artwork
            if empty:
                break
            offset += limit

        old_counters = db.LastWeekFavoriteCounters().all()
        for c in old_counters:
            c.delete()

        all_items = artwork_id__count.items()
        all_items.sort(reverse=True, key=lambda item: item[1])
        for artwork_id, count in all_items[:100]:
            counter = db.LastWeekFavoriteCounters()
            counter.artwork = artwork_id__artwork[artwork_id]
            counter.count = count
            counter.put()

        cache.delete(cache.MC_MAIN_PAGE_LAST_WEEK_FAVORITES)


class CronCalculateLastMonthTop(BasicRequestHandler):
    """
    Calculate most popular artworks for month
    """
    def get(self):
        threshold = datetime.datetime.now() - datetime.timedelta(days=30)
        artwork_id__count = {}
        artwork_id__artwork = {}
        offset = 0
        limit = 1000
        while True:
            daily_counters = db.DailyFavoritesCounters.all().filter('date >', threshold).order('-date').fetch(limit, offset)
            empty = True
            for c in daily_counters:
                empty = False
                artwork_id = c.artwork.key().id()
                if artwork_id in artwork_id__count:
                    artwork_id__count[artwork_id] = artwork_id__count[artwork_id] + c.count
                else:
                    artwork_id__count[artwork_id] = c.count
                    artwork_id__artwork[artwork_id] = c.artwork
            if empty:
                break
            offset += limit

        old_counters = db.LastMonthFavoriteCounters().all()
        for c in old_counters:
            c.delete()

        all_items = artwork_id__count.items()
        all_items.sort(reverse=True, key=lambda item: item[1])
        for artwork_id, count in all_items[:100]:
            counter = db.LastMonthFavoriteCounters()
            counter.artwork = artwork_id__artwork[artwork_id]
            counter.count = count
            counter.put()






