# -*- coding: utf-8 -*-
'''
Created on 19 nov 2013

@author: Vlad
'''

import tags
import dao

def calc_resize(image_width, image_height, max_width, max_height):
    '''
    Calculates resized image dimensions and return tuple (width,height)
    '''
    width_aspect=float(image_width)/max_width
    height_aspect=float(image_height)/max_height
        
    if width_aspect>height_aspect:
        divisor=width_aspect
    else:
        divisor=height_aspect
        
    if divisor<1:
        divisor=1
    
    return (
            int(image_width/divisor),
            int(image_height/divisor)
            )
    
def auto_nickname(src_nickname):
    a_index = src_nickname.find('@')
    if a_index < 0:
        return src_nickname
    else:
        domain = src_nickname[a_index:]
        if len(domain) == 0:
            return src_nickname
        else:
            point_index = domain.rfind('.')
            if point_index<0 or point_index == len(domain)-1:
                return src_nickname
            else:
                return src_nickname[:a_index+2]+'...'+domain[point_index+1:]
            
        
def convert_notification(notification):
    return {
            'key': notification.key(),
            'recipient': convert_user(notification.recipient),
            'date': notification.date,
            'type': notification.type,
            'artwork': convert_artwork_for_page(notification.artwork,300,300),
            'comment': convert_comment_for_page(notification.comment),
            }
    
def convert_artwork_for_page(artwork, thumbnail_width, thumbnail_height):
    result={
            'key': artwork.key(),
            'name': artwork.name,
            'description': artwork.description,
            'date': artwork.date,
            'grid': artwork.grid,
            'author': convert_user(artwork.author),
            'tags': [tags.tag_by_url_name(t) for t in artwork.tags],
            'full_image_width': artwork.full_image_height,
            'full_image_height': artwork.full_image_height
            }
    
    if artwork.small_image_width<thumbnail_width and artwork.small_image_height<thumbnail_height:
        thumbnail_size = calc_resize(
                                     artwork.full_image_width, 
                                     artwork.full_image_height, 
                                     thumbnail_width, 
                                     thumbnail_height)
        image_name = str(artwork.key().id())+'.png'
    else:
        thumbnail_size = calc_resize(
                                     artwork.small_image_width,
                                     artwork.small_image_height,
                                     thumbnail_width,
                                     thumbnail_height)
        image_name = str(artwork.key().id())+'-small.png'
        
#    if artwork.author:
#        result['author_name'] = auto_nickname(artwork.author.nickname())
#    else:
#        result['author_name'] = 'Unknown'
                
    result['thumbnail_width'] = thumbnail_size[0]
    result['thumbnail_height'] = thumbnail_size[1]
    result['thumbnail_image_name'] = image_name
    
    return result

def convert_comment_for_page(comment):
    result = {
              'key': comment.key(),
              'text': comment.text,
              'author': convert_user(comment.author),
              'date': comment.date,
              'artwork_key': comment.artwork_ref.key(),
              'artwork_name': comment.artwork_ref.name
              }
    
#    if comment.author:
#        result['author_name'] = auto_nickname(comment.author.nickname())
#    else:
#        result['author_name'] = 'Unknown'
    
    return result


def convert_user(user):
    if not user:
        return {
                'nickname': 'Unknown'
                }
    
    user_profile = dao.get_user_profile(user.email())
    if user_profile:
        return convert_user_profile(user_profile)
    else:
        return {
                'email': user.email(),
                'nickname': auto_nickname(user.nickname())+'!!!'
                }
        
def convert_user_profile(user_profile):
    return {
            'email': user_profile.email,
            'nickname': user_profile.nickname,
            'profile_id': user_profile.key().id(),
            'join_date': user_profile.join_date
            }

