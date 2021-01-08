from bad_language.profanity_filter import ProfanityFilter
from bad_language.obscene_words_filter import get_default_filter

DIACTRICS_TOP = [768, 769, 770, 771, 772, 773, 774, 775, 776, 777, 778, 779, 780, 781, 782, 783, 784, 785, 786, 787, 788, 789, 794, 795, 829, 830, 831, 832, 833, 834, 835, 836, 836, 838, 842, 843, 844, 848, 849, 850, 855, 856, 859, 861, 861, 864, 865]
DIACTRICS_BOTTOM = [790, 791, 792, 793, 796, 797, 798, 799, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817, 818, 819, 825, 826, 827, 828, 837, 839, 840, 841, 845, 846, 851, 852, 853, 854, 857, 858, 860, 863]
DIACTRICS_MIDDLE = [820, 821, 822, 823, 824]

DIACTRICS_ALL = set([unichr(c) for c in DIACTRICS_TOP + DIACTRICS_BOTTOM + DIACTRICS_MIDDLE])


def remove_diactrics(s):
    """
    Removes diactrics symbols from string
    """
    result = ''
    for c in s:
        if c not in DIACTRICS_ALL:
            result += c
    return result


def hide_bad_language(s):
    """
    Replaces bad words in phrase by '*'
    """
    if not s:
        return s

    s = remove_diactrics(s)

    filter_1 = ProfanityFilter()
    result = filter_1.censor(s)
    
    filter_2 = get_default_filter()
    result = filter_2.mask_bad_words(result)
    
    return result
    

