from google.appengine.ext import webapp

from pages.common import PageIndex
from pages.common import PageNewImage
from pages.common import PagePainter



application = webapp.WSGIApplication([
                                      ('/', PageIndex),
                                      ('/new-image', PageNewImage),
                                      ('/painter', PagePainter)
                                      ], debug=True)


