from google.appengine.ext import webapp


import pages.pages
import pages.actions


application = webapp.WSGIApplication([
                                      ('/', pages.pages.PageAllImages),
                                      ('/new-image', pages.pages.PageNewImage),
                                      ('/painter', pages.pages.PagePainter),
                                      ('/my-images', pages.pages.PageMyImages),
                                      ('/save-image', pages.actions.ActionSaveImage),
                                      ('/delete-image', pages.actions.ActionDeleteImage),
                                      ('/save-comment', pages.actions.ActionSaveComment),
                                      ('/delete-comment', pages.actions.ActionDeleteComment),
                                      ('/tag-typeahead', pages.actions.ActionTagTypeahead),
                                      ('/images/png/(.*).png', pages.actions.PNGImageRequest),
                                      ('/images/svg/(.*).svg', pages.actions.SVGImageRequest),
                                      ('/images/details/(.*)', pages.pages.PageImage)
                                      ], debug=True)


