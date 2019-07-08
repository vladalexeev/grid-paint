
from profanity_filter import Filter
from bad_language.obscene_words_filter import get_default_filter

def hide_bad_language(s):
    """
    Replaces bad words in phrase by '*'
    """
    filter_1 = Filter(s)
    result = filter_1.clean()
    
    filter_2 = get_default_filter()
    result = filter_2.mask_bad_words(result)
    
    return result
    
    
    
