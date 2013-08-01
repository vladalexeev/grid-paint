from google.appengine.ext import webapp


import pages.pages
import pages.actions


application = webapp.WSGIApplication([
                                      ('/', pages.pages.PageIndex),
                                      ('/new-image', pages.pages.PageNewImage),
                                      ('/painter', pages.pages.PagePainter),
                                      ('/my-images', pages.pages.PageMyImages),
                                      ('/save-image', pages.actions.ActionSaveArtwork),
                                      ('/delete-image', pages.actions.ActionDeleteArtwork),
                                      ('/images/png/(.*).png', pages.actions.PNGImageRequest),
                                      ('/images/svg/(.*).svg', pages.actions.SVGImageRequest),
                                      ('/images/details/(.*)', pages.pages.PageImage)
                                      ], debug=True)


