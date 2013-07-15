from google.appengine.ext import webapp

from pages.common import PageIndex
from pages.common import PageNewImage



application = webapp.WSGIApplication([
                                      ('/', PageIndex),
                                      ('/new-image',PageNewImage)
                                      ], debug=True)


