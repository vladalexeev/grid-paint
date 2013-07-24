from google.appengine.ext import webapp


import pages.pages
import pages.actions


application = webapp.WSGIApplication([
                                      ('/', pages.pages.PageIndex),
                                      ('/new-image', pages.pages.PageNewImage),
                                      ('/painter', pages.pages.PagePainter),
                                      ('/images/my', pages.pages.PageMyImages),
                                      ('/save-image', pages.actions.ActionSaveArtwork)
                                      ], debug=True)


