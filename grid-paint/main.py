from google.appengine.ext import webapp


import pages.pages
import pages.actions
import pages.tasks


application = webapp.WSGIApplication([
                                      ('/', pages.pages.PageIndex),
                                      ('/gallery', pages.pages.PageGallery),
                                      ('/admin',pages.pages.PageAdmin),
                                      ('/admin/delete-comment', pages.actions.ActionDeleteComment),
                                      ('/admin/saveArtworkProperties', pages.actions.ActionAdminSetArtworkProperties),
                                      ('/admin/updateUserFavorites', pages.actions.ActionAdminUpdateUserFavoritesCount),
                                      ('/admin/updateArtworkFavorites', pages.actions.ActionAdminUpdateArtworkFavoriteCount),
                                      ('/admin/update-iterate', pages.pages.PageAdminUpdateIterate),
                                      ('/admin/update-iterate-do', pages.actions.ActionUpdateIterate),
                                      ('/admin/hide-comment', pages.actions.ActionHideComment),
                                      ('/admin/show-comment', pages.actions.ActionShowComment),
                                      ('/admin/block-user', pages.actions.ActionAdminBlockUser),
                                      ('/admin/unblock-user', pages.actions.ActionAdminUnblockUser),
                                      ('/admin/refresh-index-page', pages.actions.ActionAdminFlushMemcacheForIndexPage),
                                      ('/admin/update-editor-choice', pages.actions.ActionUpdateEditorChoice),
                                      ('/save-settings', pages.actions.ActionSaveSettings),
                                      ('/new-image', pages.pages.PageNewImage),
                                      ('/painter', pages.pages.PagePainter),
                                      ('/my-images', pages.pages.PageMyImages),
                                      ('/my-favorites', pages.pages.PageMyFavorites),
                                      ('/my-followers', pages.pages.PageMyFollowers),
                                      ('/my-leaders', pages.pages.PageMyLeaders),
                                      ('/privacy-policy', pages.pages.PagePrivacyPolicy),
                                      ('/rules', pages.pages.PageRules),
                                      ('/history', pages.pages.PageHistory),
                                      ('/save-image', pages.actions.ActionSaveImage),
                                      ('/delete-image', pages.actions.ActionDeleteImage),
                                      ('/save-comment', pages.actions.ActionSaveComment),
                                      ('/complain-comment', pages.actions.ActionComlainComment),
                                      ('/tag-typeahead', pages.actions.ActionTagTypeahead),
                                      ('/images/details/(.*)', pages.pages.PageImage),
                                      ('/images/png/(.*)', pages.actions.PNGImageRequest),
                                      ('/images/svg/(.*).svg', pages.actions.SVGImageRequest),
                                      ('/images/json/(.*).json', pages.actions.JSONImageRequest),
                                      ('/notifications', pages.pages.PageNotifications),
                                      ('/delete-notification', pages.actions.ActionDeleteNotification),
                                      ('/delete-all-notifications', pages.actions.ActionDeleteAllNotifications),
                                      ('/my-profile', pages.pages.PageMyProfile),
                                      ('/save-profile', pages.actions.ActionSaveProfile),
                                      ('/profiles', pages.pages.PageProfiles),
                                      ('/profiles/', pages.pages.PageProfiles),
                                      ('/profiles/by-artwork-count', pages.pages.PageUsersByArtworksCount),
                                      ('/profiles/by-stars-count', pages.pages.PageUsersByFavortiesCount),
                                      ('/profiles/blocked', pages.pages.PageUsersBlocked),
                                      ('/profiles/(.*)/favorites', pages.pages.PageUserFavorites),
                                      ('/profiles/(.*)/comments', pages.pages.PageUserComments),
                                      ('/profiles/(.*)/followers', pages.pages.PageUserFollowers),
                                      ('/top-favorites', pages.pages.PageTopFavorites),
                                      ('/profiles/(.*)', pages.pages.PageProfile),
                                      ('/editor-choice', pages.pages.PageEditorChoice),
                                      ('/favorites', pages.pages.PageRecentFavorites),
                                      ('/toggle-favorite', pages.actions.ActionToggleFavorite),
                                      ('/json/comments', pages.actions.JSONComments),
                                      ('/json/get-user-id-by-nickname', pages.actions.JSONGetUserIdByNickname),
                                      ('/json/save-alternative-email', pages.actions.JSONSaveAlternativeEmail),
                                      ('/json/delete-alternative-email', pages.actions.JsonDeleteAlternativeEmail),
                                      ('/json/notifications', pages.actions.JSONNotifications),
                                      ('/json/followers', pages.actions.JSONFollowers),
                                      ('/json/leaders', pages.actions.JSONLeaders),
                                      ('/comments', pages.pages.PageComments),
                                      ('/follow', pages.actions.ActionFollow),
                                      ('/unfollow', pages.actions.ActionUnfollow),
                                      ('/cron/clean-notifications', pages.actions.CronCleanNotifications),
                                      ('/tasks/add-artwork-to-news', pages.tasks.TaskAddArtworkToNews),
                                      ], debug=True)


