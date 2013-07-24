from google.appengine.ext import webapp


import pages.pages
import pages.actions


application = webapp.WSGIApplication([
                                      ('/', pages.pages.PageIndex),
                                      ('/new-image', pages.pages.PageNewImage),
                                      ('/painter', pages.pages.PagePainter),
                                      ('/my-images', pages.pages.PageMyImages),
                                      ('/save-image', pages.actions.ActionSaveArtwork),
                                      ('/images/png/(.*)', pages.pages.FullImageRequest)
                                      ], debug=True)


