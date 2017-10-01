
import cache
from datetime import datetime, timedelta

COMMENT_CACHE_PREFIX='as_comment_'

VALUE_COMMENT = 'comment'
VALUE_DATE = 'date'
VALUE_ARTWORK_ID = 'artwork_id'

COMMENT_MIN_INTERVAL = timedelta(seconds=5)

def check_comment(user_email, artwork_id, comment_text):
    cache_key = COMMENT_CACHE_PREFIX + user_email
    cache_value = cache.get(cache_key)
    result = False
    if cache_value is None:
        result = True
    else:
        if datetime.now() - cache_value[VALUE_DATE] > COMMENT_MIN_INTERVAL:
            if artwork_id <> cache_value[VALUE_ARTWORK_ID]:
                result = True
            else:
                if comment_text <> cache_value[VALUE_COMMENT]:
                    result = True
                    
    cache_value = {
        VALUE_DATE: datetime.now(),
        VALUE_ARTWORK_ID: artwork_id,
        VALUE_COMMENT: comment_text
        }
    cache.add(cache_key, cache_value)
                    
    return result

