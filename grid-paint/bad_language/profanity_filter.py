import re

default_bad_words = [
    'a55', 'anal', 'anus', 'ar5e', 'arrse', 'arse', 'ass', 'ass-fucker', 'asses', 'assfucker', 
    'assfukka', 'asshole', 'assholes', 'asswhole', 'a_s_s', 'b!tch', 'b00bs', 'b17ch', 'b1tch', 
    'ballbag', 'balls', 'ballsack', 'bastard', 'beastial', 'beastiality', 'bellend', 'bestial', 
    'bestiality', 'bi\\+ch', 'biatch', 'bitch', 'bitcher', 'bitchers', 'bitches', 'bitchin', 
    'bitching', 'bloody', 'blow job', 'blowjob', 'blowjobs', 'boiolas', 'bollock', 'bollok', 
    'boner', 'boob', 'boobs', 'booobs', 'boooobs', 'booooobs', 'booooooobs', 'breasts', 'buceta', 
    'bugger', 'bum', 'bunny fucker', 'butt', 'butthole', 'buttmuch', 'buttplug', 'c0ck', 'c0cksucker', 
    'carpet muncher', 'cawk', 'chink', 'cipa', 'cl1t', 'clit', 'clitoris', 'clits', 'cnut', 'cock', 
    'cock-sucker', 'cock sucker', 'cockface', 'cockhead', 'cockmunch', 'cockmuncher', 'cocks', 
    'cocksuck', 'cocksucked', 'cocksucker', 'cocksucking', 'cocksucks', 'cocksuka', 'cocksukka', 
    'cok', 'cokmuncher', 'coksucka', 'coon', 'cox', 'crap', 'cum', 'cummer', 'cumming', 'cums', 'cumshot', 
    'cunilingus', 'cunillingus', 'cunnilingus', 'cunt', 'cuntlick', 'cuntlicker', 'cuntlicking', 'cunts', 
    'cyalis', 'cyberfuc', 'cyberfuck', 'cyberfucked', 'cyberfucker', 'cyberfuckers', 'cyberfucking', 
    'd1ck', 'damn', 'dick', 'dickhead', 'dildo', 'dildos', 'dink', 'dinks', 'dirsa', 'dlck', 'dog-fucker', 
    'doggin', 'dogging', 'donkeyribber', 'doosh', 'duche', 'dyke', 'ejaculate', 'ejaculated', 'ejaculates', 
    'ejaculating', 'ejaculatings', 'ejaculation', 'ejakulate', 'f u c k', 'f u c k e r', 'f4nny', 'fag', 
    'fagging', 'faggitt', 'faggot', 'faggs', 'fagot', 'fagots', 'fags', 'fanny', 'fannyflaps', 'fannyfucker', 
    'fanyy', 'fatass', 'fcuk', 'fcuker', 'fcuking', 'feck', 'fecker', 'felching', 'fellate', 'fellatio', 
    'fingerfuck', 'fingerfucked', 'fingerfucker', 'fingerfuckers', 'fingerfucking', 'fingerfucks', 'fistfuck', 
    'fistfucked', 'fistfucker', 'fistfuckers', 'fistfucking', 'fistfuckings', 'fistfucks', 'flange', 'fook', 
    'fooker', 'fuck', 'fucka', 'fucked', 'fucker', 'fuckers', 'fuckhead', 'fuckheads', 'fuckin', 'fucking', 
    'fuckings', 'fuckingshitmotherfucker', 'fuckme', 'fucks', 'fuckwhit', 'fuckwit', 'fudge packer', 
    'fudgepacker', 'fuk', 'fuker', 'fukker', 'fukkin', 'fuks', 'fukwhit', 'fukwit', 'fux', 'fux0r', 'f_u_c_k', 
    'gangbang', 'gangbanged', 'gangbangs', 'gaylord', 'gaysex', 'goatse', 'god-dam', 'god-damned',
    'goddamn', 'goddamned', 'hardcoresex', 'hell', 'heshe', 'hoar', 'hoare', 'hoer', 'homo', 'hore', 'horniest', 
    'horny', 'hotsex', 'jack-off', 'jackoff', 'jap', 'jerk-off', 'jism', 'jiz', 'jizm', 'jizz', 'kawk', 'knob', 
    'knobead', 'knobed', 'knobend', 'knobhead', 'knobjocky', 'knobjokey', 'kock', 'kondum', 'kondums', 'kum', 
    'kummer', 'kumming', 'kums', 'kunilingus', 'l3i\\+ch', 'l3itch', 'labia', 'lmfao', 'lust', 'lusting', 'm0f0', 
    'm0fo', 'm45terbate', 'ma5terb8', 'ma5terbate', 'masochist', 'master-bate', 'masterb8', 'masterbat', 
    'masterbat3', 'masterbate', 'masterbation', 'masterbations', 'masturbate', 'mo-fo', 'mof0', 'mofo', 
    'mothafuck', 'mothafucka', 'mothafuckas', 'mothafuckaz', 'mothafucked', 'mothafucker', 'mothafuckers', 
    'mothafuckin', 'mothafucking', 'mothafuckings', 'mothafucks', 'motherfuck', 'motherfucked', 'motherfucker', 
    'motherfuckers', 'motherfuckin', 'motherfucking', 'motherfuckings', 'motherfuckka', 'motherfucks', 'muff', 
    'mutha', 'muthafecker', 'muthafuckker', 'muther', 'mutherfucker', 'n1gga', 'n1gger', 'nazi', 'nigg3r', 
    'nigg4h', 'nigga', 'niggah', 'niggas', 'niggaz', 'nigger', 'niggers', 'nob', 'nobhead', 'nobjocky', 'nobjokey', 
    'numbnuts', 'nutsack', 'orgasim', 'orgasims', 'orgasm', 'orgasms', 'p0rn', 'pawn', 'pecker', 'penis', 
    'penisfucker', 'phonesex', 'phuck', 'phuk', 'phuked', 'phuking', 'phukked', 'phukking', 'phuks', 'phuq', 
    'pigfucker', 'pimpis', 'piss', 'pissed', 'pisser', 'pissers', 'pisses', 'pissflaps', 'pissin', 'pissing', 
    'pissoff', 'poop', 'porn', 'porno', 'pornography', 'pornos', 'prick', 'pron', 'pube', 'pusse', 'pussi', 
    'pussies', 'pussy', 'rectum', 'retard', 'rimjaw', 'rimming', 's.o.b.', 'sadist', 'schlong', 'screwing', 
    'scroat', 'scrote', 'scrotum', 'semen', 'sex', 'sh!\\+', 'sh!t', 'sh1t', 'shag', 'shagger', 'shaggin', 
    'shagging', 'shemale', 'shi\\+', 'shit', 'shitdick', 'shite', 'shited', 'shitey', 'shitfuck', 'shitfull', 
    'shithead', 'shiting', 'shits', 'shitted', 'shitter', 'shitting', 'shitty', 'skank', 'slut', 'sluts', 'smegma', 
    'smut', 'snatch', 'son-of-a-bitch', 'spac', 'spunk', 's_h_i_t', 't1tt1e5', 't1tties', 'teets', 'teez', 'testical', 
    'testicle', 'tit', 'titfuck', 'tits', 'titt', 'tittie5', 'tittiefucker', 'titties', 'tittyfuck', 'tittywank', 
    'titwank', 'tosser', 'turd', 'tw4t', 'twat', 'twathead', 'twatty', 'twunt', 'twunter', 'v14gra', 'v1gra', 
    'vagina', 'viagra', 'vulva', 'w00se', 'wang', 'wank', 'wanker', 'wanky', 'whoar', 'whore', 'willies', 'willy', 
    'xrated', 'xxx']


class ProfanityFilter:
    def __init__(self, **kwargs):
        """
        Returns a ProfanityFilter instance.
        Kwargs:
            - custom_censor_list (list):
                A custom list of bad words to be used instead of the default list.
            - extra_censor_list (list):
                A custom list of bad words to be used in conjunction with the default list.
            - no_word_boundaries (bool):
                False means no word boundaries will be used in the regex for bad words.
                i.e abc\ **badword**\ abc will be treated as profane.
        """

        # If defined, use this instead of _censor_list
        self._custom_censor_list = kwargs.get("custom_censor_list", [])

        # Words to be used in conjunction with _censor_list
        self._extra_censor_list = kwargs.get("extra_censor_list", [])

        # Toggle use of word boundaries in regex
        self._no_word_boundaries = kwargs.get("no_word_boundaries", False)

        # What to be censored -- should not be modified by user
        self._censor_list = []

        # What to censor the words with
        self._censor_char = "*"

        # Where to find the censored words
        self._censor_list = default_bad_words

    def define_words(self, word_list):
        """Define a custom list of profane words to be used instead of the default list."""
        self._custom_censor_list = word_list

    def append_words(self, word_list):
        """Define a custom list of profane words to be used in conjunction with the default list."""
        self._extra_censor_list.extend(word_list)

    def remove_word(self, word):
        """Remove given word from censor list."""
        self._censor_list.remove(word)

    def set_censor(self, character):
        """Replaces the original censor character '*' with ``character``."""
        # TODO: what if character isn't str()-able?
        if isinstance(character, int):
            character = str(character)
        self._censor_char = character

    def has_bad_word(self, text):
        """Returns True if text contains profanity, False otherwise."""
        return self.censor(text) != text

    def get_custom_censor_list(self):
        """Returns the list of custom profane words."""
        return self._custom_censor_list

    def get_extra_censor_list(self):
        """Returns the list of custom additional profane words."""
        return self._extra_censor_list

    def get_profane_words(self):
        """Returns all profane words currently in use."""
        profane_words = []

        if self._custom_censor_list:
            profane_words = [w for w in self._custom_censor_list]  # Previous versions of Python don't have list.copy()
        else:
            profane_words = [w for w in self._censor_list]

        profane_words.extend(self._extra_censor_list)
        #profane_words.extend([inflection.pluralize(word) for word in profane_words])
        profane_words = list(set(profane_words))

        # We sort the list based on decreasing word length so that words like
        # 'fu' aren't substituted before 'fuck' if no_word_boundaries = true
        profane_words.sort(key=len)
        profane_words.reverse()

        return profane_words

    def restore_words(self):
        """Clears all custom censor lists and reloads the default censor list."""
        self._custom_censor_list = []
        self._extra_censor_list = []
        self._censor_list = default_bad_words

    def censor(self, input_text):
        """Returns input_text with any profane words censored."""
        bad_words = self.get_profane_words()
        res = input_text

        for word in bad_words:
            # Apply word boundaries to the bad word
            regex_string = r'{0}' if self._no_word_boundaries else r'\b{0}\b'
            regex_string = regex_string.format(word)
            regex = re.compile(regex_string, re.IGNORECASE)
            res = regex.sub(self._censor_char * len(word), res)

        return res

    def is_clean(self, input_text):
        """Returns True if input_text doesn't contain any profane words, False otherwise."""
        return not self.has_bad_word(input_text)

    def is_profane(self, input_text):
        """Returns True if input_text contains any profane words, False otherwise."""
        return self.has_bad_word(input_text)


