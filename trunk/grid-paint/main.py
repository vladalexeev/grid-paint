from google.appengine.ext import webapp

from pages.pages import PageIndex
from pages.pages import PageNewImage
from pages.pages import PagePainter



application = webapp.WSGIApplication([
                                      ('/', PageIndex),
                                      ('/new-image', PageNewImage),
                                      ('/painter', PagePainter)
                                      ], debug=True)


