# -*- coding: utf-8 -*-
'''
Created on 19 nov 2013

@author: Vlad
'''

import tags
import dao
import logging

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
    result =  {
            'key': notification.key(),
            'recipient': convert_user(notification.recipient_email),
            'date': notification.date,
            'type': notification.type
            }
    
    try:
        result['artwork'] = convert_artwork_for_page(notification.artwork,300,300)
    except:
        pass
        
    try:
        result['comment'] = convert_comment_for_page(notification.comment)
    except:
        pass
    
    try:
        result['sender'] = convert_user(notification.sender_email)
    except:
        pass
    
    return result;
    
def convert_artwork_for_page(artwork, thumbnail_width, thumbnail_height):
    try:
        if hasattr(artwork, 'artwork'):
            artwork = artwork.artwork
        
        result={
                'key': artwork.key(),
                'name': artwork.name,
                'description': artwork.description,
                'description_list': artwork.description.split('\n'),
                'date': artwork.date,
                'grid': artwork.grid,
                'author': convert_user(artwork.author_email),
                'tags': [tags.tag_by_url_name(t) for t in artwork.tags],
                'full_image_width': artwork.full_image_height,
                'full_image_height': artwork.full_image_height,
                'full_image_file_name': artwork.full_image_file_name,
                'small_image_width': artwork.small_image_height,
                'small_image_height': artwork.small_image_height,            
                'small_image_file_name': artwork.small_image_file_name,
                'editor_choice': artwork.editor_choice
                }
        
        if hasattr(artwork, 'copyright_block'):
            result['copyright_block'] = True
    
        if artwork.small_image_width<thumbnail_width and artwork.small_image_height<thumbnail_height:
            thumbnail_size = calc_resize(
                                         artwork.full_image_width, 
                                         artwork.full_image_height, 
                                         thumbnail_width, 
                                         thumbnail_height)
            image_name = artwork.full_image_file_name
        else:
            thumbnail_size = calc_resize(
                                         artwork.small_image_width,
                                         artwork.small_image_height,
                                         thumbnail_width,
                                         thumbnail_height)
            image_name = artwork.small_image_file_name
        
        result['thumbnail_width'] = thumbnail_size[0]
        result['thumbnail_height'] = thumbnail_size[1]
        result['thumbnail_image_name'] = image_name
    except Exception, e:
        logging.error('Error', e)
        result = {
                  'key': artwork.key(),
                  'not_found': True
                  }
    
    return result

def convert_comment_for_page(comment):
    result = {
              'key': comment.key().id(),
              'text': comment.text.split('\n'),
              'author': convert_user(comment.author_email),
              'date': comment.date,
              'artwork_key': comment.artwork_ref.key().id(),
              'artwork_name': comment.artwork_ref.name
              }
    if hasattr(comment, 'hidden'):
        result['hidden'] = True
        
    return result

def convert_comment_for_page_rich(comment):
    result = convert_comment_for_page(comment)
    result['small_image_file'] = comment.artwork_ref.small_image_file_name
    result['small_image_width'] = int(comment.artwork_ref.small_image_width / 2)
    result['small_image_height'] = int(comment.artwork_ref.small_image_height / 2)
    return result


def convert_user(user_email):
    if not user_email:
        return {
                'nickname': 'Unknown'
                }
    
    user_profile = dao.get_user_profile(user_email)
    if user_profile:
        return convert_user_profile(user_profile)
    else:
        return {
                'email': user_email,
                'nickname': auto_nickname(user_email)
                }
        
def convert_user_profile(user_profile):
    return {
            'email': user_profile.email,
            'nickname': user_profile.nickname,
            'profile_id': user_profile.key().id(),
            'join_date': user_profile.join_date,
            'artworks_count': user_profile.artworks_count,
            'favorite_count': user_profile.favorite_count,
            'read_only': hasattr(user_profile, 'read_only')
            }

