from google.appengine.ext import webapp


import pages.pages
import pages.actions


application = webapp.WSGIApplication([
                                      ('/', pages.pages.PageIndex),
                                      ('/gallery', pages.pages.PageGallery),
                                      ('/admin',pages.pages.PageAdmin),
                                      ('/admin/saveArtworkProperties', pages.actions.ActionAdminSetArtworkProperties),
                                      ('/admin/update-iterate-artworks', pages.pages.PageAdminUpdateArtworkIterate),
                                      ('/admin/update-iterate-artworks-do', pages.actions.ActionUpdateArtworkIterate),
                                      ('/save-settings', pages.actions.ActionSaveSettings),
                                      ('/new-image', pages.pages.PageNewImage),
                                      ('/painter', pages.pages.PagePainter),
                                      ('/my-images', pages.pages.PageMyImages),
                                      ('/privacy-policy', pages.pages.PagePrivacyPolicy),
                                      ('/history', pages.pages.PageHistory),
                                      ('/save-image', pages.actions.ActionSaveImage),
                                      ('/delete-image', pages.actions.ActionDeleteImage),
                                      ('/save-comment', pages.actions.ActionSaveComment),
                                      ('/delete-comment', pages.actions.ActionDeleteComment),
                                      ('/tag-typeahead', pages.actions.ActionTagTypeahead),
                                      ('/images/png/(.*)-small.png', pages.actions.PNGSmallImageRequest),
                                      ('/images/png/(.*).png', pages.actions.PNGImageRequest),
                                      ('/images/svg/(.*).svg', pages.actions.SVGImageRequest),
                                      ('/images/json/(.*).json', pages.actions.JSONImageRequest),
                                      ('/images/details/(.*)', pages.pages.PageImage),
                                      ('/notifications', pages.pages.PageNotifications),
                                      ('/delete-notification', pages.actions.ActionDeleteNotification),
                                      ('/my-profile', pages.pages.PageMyProfile),
                                      ('/save-profile', pages.actions.ActionSaveProfile),
                                      ('/profiles/(.*)', pages.pages.PageProfile),
                                      ('/editor-choice', pages.pages.PageEditorChoice),
                                      
                                      ('/update', pages.actions.ActionUpdate)
                                      ], debug=True)


