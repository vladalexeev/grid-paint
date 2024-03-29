# -*- coding: utf-8 -*-

from google.appengine.ext import db

artwork_small_image_width=200
artwork_small_image_height=150


class Artwork(db.Expando):
    name = db.TextProperty()
    description = db.TextProperty()
    author_email = db.StringProperty()
    tags = db.StringListProperty()
    date = db.DateTimeProperty()
    json_file_name = db.StringProperty(indexed=False)
    grid = db.StringProperty()
    full_image_file_name = db.TextProperty()
    full_image_width = db.IntegerProperty(indexed=False)
    full_image_height = db.IntegerProperty(indexed=False)
    small_image_file_name = db.TextProperty()
    small_image_width = db.IntegerProperty(indexed=False)
    small_image_height = db.IntegerProperty(indexed=False)
    editor_choice = db.BooleanProperty()
    editor_choice_date = db.DateTimeProperty()


class ArtworkCollaborator(db.Model):
    artwork = db.ReferenceProperty(reference_class=Artwork)
    user_id = db.IntegerProperty()
    join_date = db.DateTimeProperty(auto_now=True)
    last_date = db.DateTimeProperty(auto_now=True)


class Tag(db.Model):
    url_name = db.StringProperty()
    title = db.StringProperty()
    title_lower = db.StringProperty()
    date = db.DateTimeProperty()
    count = db.IntegerProperty()
    last_date = db.DateTimeProperty()
    cover = db.ReferenceProperty(reference_class=Artwork)


class UserTag(db.Model):
    user_id = db.IntegerProperty()
    url_name = db.StringProperty()
    title = db.StringProperty()
    title_lower = db.StringProperty()
    date = db.DateTimeProperty()
    count = db.IntegerProperty()
    last_date = db.DateTimeProperty()
    cover = db.ReferenceProperty(reference_class=Artwork)


class Comment(db.Expando):
    artwork_ref = db.ReferenceProperty(reference_class=Artwork)
    author_email = db.StringProperty()
    text = db.TextProperty(indexed=False)
    date = db.DateTimeProperty(auto_now_add=True)


class Notification(db.Expando):
    date = db.DateTimeProperty(auto_now_add=True)
    recipient_email = db.StringProperty()
    read = db.BooleanProperty(default = False)
    type = db.StringProperty(indexed=False)
    artwork = db.ReferenceProperty(reference_class=Artwork, indexed=False)
    comment = db.ReferenceProperty(reference_class=Comment, indexed=False)
    sender_email = db.StringProperty(indexed=False)


class UserProfile(db.Expando):
    email = db.StringProperty()
    nickname = db.StringProperty()
    join_date = db.DateTimeProperty(auto_now_add=True)
    artworks_count = db.IntegerProperty(default=0)
    favorite_count = db.IntegerProperty(default=0)
    avatar_file = db.StringProperty()


class UserRelationSettings(db.Expando):
    profile_id = db.IntegerProperty()
    related_profile_id = db.IntegerProperty()
    block_collaboration_invitations = db.BooleanProperty()
    last_date = db.DateTimeProperty(auto_now_add=True)
    
    
class Settings(db.Model):
    show_ads = db.BooleanProperty()
    show_analytics = db.BooleanProperty()
    admin_email = db.StringProperty()
    admin_user_id = db.IntegerProperty()
    exchange_url = db.StringProperty()
    exchange_salt = db.StringProperty()


class Favorite(db.Expando):
    user_email = db.StringProperty()
    artwork = db.ReferenceProperty(reference_class=Artwork)
    date = db.DateTimeProperty(auto_now_add=True)


class FavoriteCounter(db.Expando):
    artwork = db.ReferenceProperty(reference_class=Artwork)
    count = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now_add=True)


class Follow(db.Expando):
    leader_email = db.StringProperty()
    follower_email = db.StringProperty()
    since_date = db.DateTimeProperty(auto_now_add=True)
    

class NewsFeed(db.Expando):
    user_email = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    artwork = db.ReferenceProperty(reference_class=Artwork)
    type = db.StringProperty()


class TaskLog(db.Expando):
    date = db.DateTimeProperty(auto_now_add=True)
    task_name = db.StringProperty()
    data = db.StringProperty()


class TaskStatus(db.Expando):
    task_name = db.StringProperty()
    last_date = db.DateTimeProperty()
    data = db.StringProperty()
    finished = db.BooleanProperty()


class UpdateUser(db.Expando):
    """
    Entity for schedule user refresh and update
    """
    profile_id = db.IntegerProperty()
    update_date = db.DateTimeProperty()
    action = db.StringProperty()


class TodayFavoriteCounter(db.Expando):
    """
    Favorite counter for the current day
    """
    artwork = db.ReferenceProperty(reference_class=Artwork)
    count = db.IntegerProperty()


class DailyFavoritesCounters(db.Expando):
    """
    History of artworks' favorites by days
    """
    date = db.DateProperty(auto_now=True)
    artwork = db.ReferenceProperty(reference_class=Artwork)
    count = db.IntegerProperty()


class LastWeekFavoriteCounters(db.Expando):
    """
    Most popular artworks for last week
    """
    artwork = db.ReferenceProperty(reference_class=Artwork)
    count = db.IntegerProperty()


class LastMonthFavoriteCounters(db.Expando):
    """
    Most popular artworks for last month
    """
    artwork = db.ReferenceProperty(reference_class=Artwork)
    count = db.IntegerProperty()
