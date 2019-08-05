import db
from common import BasicRequestHandler


class ActionUpdateTags(BasicRequestHandler):
    def get(self):
        if not self.user_info.superadmin:
            self.response.set_status(403)
            return

        limit = int(self.request.get('limit'))
        offset = int(self.request.get('offset'))

        tags_pack = db.Tag.all().order('title').fetch(limit, offset)
        count = 0
        for t in tags_pack:
            t.url_name = t.url_name.lower()
            t.put()
            count = count + 1

        self.response.out.write(str(count))
