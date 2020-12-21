from bad_language.profanity_filter import ProfanityFilter
from bad_language.obscene_words_filter import get_default_filter
import unidecode


def hide_bad_language(s):
    """
    Replaces bad words in phrase by '*'
    """
    if not s:
        return s

    result = unidecode.unidecode(s)  # remove accents from the string
    result = result.replace('[?]', '')

    filter_1 = ProfanityFilter()
    result = filter_1.censor(result)
    
    filter_2 = get_default_filter()
    result = filter_2.mask_bad_words(result)
    
    return result
    

