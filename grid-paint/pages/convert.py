# -*- coding: utf-8 -*-
'''
Created on 19 nov 2013

@author: Vlad
'''

import tags
import dao
import logging

DEFAULT_AVATAR_URL = '/img/svg-buttons/empty-avatar.svg'

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

    if hasattr(notification, 'message'):
        result['message'] = notification.message

    if hasattr(notification, 'status'):
        result['status'] = notification.status
    
    return result


def convert_notification_json(notification):
    n = convert_notification(notification)
    result = {
        'id': n['key'].id(),
        'date': n['date'],
        'type': n['type']
        }
    
    if n.get('artwork'):
        result['artwork'] = {
            'id': n['artwork']['key'].id(),
            'name': n['artwork']['name'],
            'date': n['artwork']['date'],
            'author': {
                'nickname': n['artwork'].get('author',{}).get('nickname'),
                'profile_id': n['artwork'].get('author', {}).get('profile_id')
                }
            }
        
    if 'comment' in n:
        result['comment'] = {
              'id': n['comment']['key'],
              'text': n['comment']['text'],
              'author': {
                  'nickname': n['comment'].get('author', {}).get('nickname'),
                  'profile_id': n['comment'].get('author', {}).get('profile_id')
                  },
              'date': n['comment']['date'],
              'artwork_id': n['comment']['artwork_key'],
              'artwork_name': n['comment']['artwork_name'],
            }
        if 'hidden' in n['comment']:
            result['comment']['hidden'] = n['comment']['hidden']
            
    if 'sender' in n:
        result['sender'] = {
            'nickname': n['sender'].get('nickname'),
            'profile_id': n['sender'].get('profile_id')
            }

    if 'message' in n:
        result['message'] = n['message']

    if 'status' in n:
        result['status'] = n['status']
        
    return result
        
    
def convert_artwork_for_page(artwork, thumbnail_width, thumbnail_height):
    try:
        if artwork is None:
            return None
        
        if hasattr(artwork, 'artwork'):
            artwork = artwork.artwork
            
        if artwork is None:
            return None
            
        artwork_description = []
        if hasattr(artwork, 'description') and artwork.description:
            artwork_description = artwork.description.split('\n')            
        
        result={
                'key': artwork.key(),
                'name': artwork.name,
                'description': artwork.description,
                'description_list': artwork_description,
                'date': artwork.date,
                'grid': artwork.grid,
                'author': convert_user(artwork.author_email),
                'tags': [tags.tag_by_url_name(t) for t in artwork.tags],
                'full_image_width': artwork.full_image_width,
                'full_image_height': artwork.full_image_height,
                'full_image_file_name': artwork.full_image_file_name,
                'small_image_width': artwork.small_image_width,
                'small_image_height': artwork.small_image_height,            
                'small_image_file_name': artwork.small_image_file_name,
                'editor_choice': artwork.editor_choice
                }
        
        if hasattr(artwork, 'pixel_image_file_name'):
            result['pixel_image_file_name'] = artwork.pixel_image_file_name
            result['pixel_image_width'] = artwork.pixel_image_width
            result['pixel_image_height'] = artwork.pixel_image_height
        
        if hasattr(artwork, 'copyright_block'):
            result['copyright_block'] = True
            
        if hasattr(artwork, 'block'):
            result['block'] = True
            
        if hasattr(artwork, 'block_reason'):
            result['block_reason'] = artwork.block_reason
    
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
    except Exception:
        logging.exception('Convert error')
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
        result['text'] = []

    if hasattr(comment, 'hidden_by'):
        result['hidden_by'] = comment.hidden_by

    if 'self_block' in result['author']:
        result['text'] = ['[Comment not available]']
        
    return result


def convert_comment_for_page_rich(comment):
    result = convert_comment_for_page(comment)
    result['small_image_file'] = comment.artwork_ref.small_image_file_name
    result['small_image_width'] = int(comment.artwork_ref.small_image_width / 2)
    result['small_image_height'] = int(comment.artwork_ref.small_image_height / 2)
    result['artwork_copyright_block'] = hasattr(comment.artwork_ref, 'copyright_block')
    result['artwork_block'] = hasattr(comment.artwork_ref, 'block')

    import dao
    artwork_author_profile = dao.get_user_profile(comment.artwork_ref.author_email)
    if artwork_author_profile and hasattr(artwork_author_profile, 'self_block'):
        result['artwork_author_self_block'] = True

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


def make_avatar_url(profile_id):
    return '/images/avatar/' + str(profile_id) + '.jpg'


def convert_user_profile(user_profile):
    if getattr(user_profile, 'avatar_file'):
        avatar_url = make_avatar_url(user_profile.key().id())
    else:
        avatar_url = DEFAULT_AVATAR_URL
        
    result = {
            # 'email': user_profile.email,
            'nickname': user_profile.nickname,
            'profile_id': user_profile.key().id(),
            'join_date': user_profile.join_date,
            'artworks_count': user_profile.artworks_count,
            'favorite_count': user_profile.favorite_count,
            'followers_count': getattr(user_profile, 'followers_count', 0),
            'leaders_count': getattr(user_profile, 'leaders_count', 0),
            'read_only': hasattr(user_profile, 'read_only'),
            # 'alternative_emails': getattr(user_profile, 'alternative_emails', []),
            'avatar_url': avatar_url,
            }
    
    if hasattr(user_profile, 'block_date'):
        result['block_date'] = user_profile.block_date
        
    if hasattr(user_profile, 'block_reason'):
        result['block_reason'] = user_profile.block_reason

    if hasattr(user_profile, 'self_block'):
        result['self_block'] = True
        result['nickname'] = '[User deleted]'
        
    return result


def convert_user_profile_for_json(user_profile):
    if getattr(user_profile, 'avatar_file'):
        avatar_url = make_avatar_url(user_profile.key().id())
    else:
        avatar_url = DEFAULT_AVATAR_URL

    result = {
            'nickname': user_profile.nickname,
            'profile_id': user_profile.key().id(),
            'avatar_url': avatar_url
        }
    if hasattr(user_profile, 'self_block'):
        result['nickname'] = '[User deleted]'
        result['self_block'] = True
    return result


def convert_tag_for_page(tag):
    return {
        'tag_id': tag.key().id(),
        'title': tag.title,
        'url_name': tag.url_name,
        'artwork_id': tag.cover.key().id() if tag.cover else None,
        'count': tag.count,
    }