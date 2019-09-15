import db
import json
import dao

from common import BasicRequestHandler


class TaskAddArtworkToNews(BasicRequestHandler):
    def post(self):
        news_type = self.request.get('type')
        artwork_id = int(self.request.get('artwork_id'))

        artwork = dao.get_artwork(artwork_id)
        if not artwork:
            self.response.out.write(json.dumps('OK'))
            return

        author_email = artwork.author_email
        limit = 200
        offset = 0

        count = limit
        while count == limit:
            count = 0        
            followers = db.Follow.all().filter('leader_email =', author_email).order('follower_email').fetch(limit,offset)
            for f in followers:
                dao.add_to_news_feed(f.follower_email, artwork, news_type)
                count = count + 1
            offset += limit
                 
        self.response.out.write(json.dumps('OK'))
