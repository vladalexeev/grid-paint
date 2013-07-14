from google.appengine.ext import webapp

from pages.common import PageIndex



application = webapp.WSGIApplication([(
                                       '/', PageIndex
                                       )], debug=True)


