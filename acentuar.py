import argparse
import random
import pyphen
import localisation as loc
import sys
from re import match, compile


VOWELS = ["a", "e", "i", "o", "u"]
DIACRITICS = ["á", "é", "í", "ó", "ú"]
N_OR_S = ["n", "s"]

# locale will be overridden by args
locale = "es"

# dic to split in syllables
dic = pyphen.Pyphen(lang='es_ES')

DICTIONARY = {"jamón": 1, "bolígrafo": 3, "esdrújula": 3, "salón": 1, "melón": 1, "excursión": 1,
              "césped": 2, "perro": 2, "gato": 2, "perdiz": 1, "equipo": 2
              }

UNFAMILIAR_WORDS = ["cotiledón", "origen", "margen", "pesquisa", "diptongo", "caracteres", "márgenes",
                    "orate", "vagido", "burdégano", "sapenco", "livógiro", "especimen", "lápiz"]

WORDS_BAG = ["abarrotado", "colombia", "mueve", "abarrotes", "comadreja", "nubes", "abasto",
             "come", "nublado", "abeja", "como", "piojos", "pacto", "canal", "pactar", "sentir",
             "onomatopeya", "escabroso", "viernes", "jueves", "ejercicio", "deberes", "comiendo",
             "experiencia", "jaleo", "resumen", "volumen", "carmen", "bote", "rompe", "romper"]

WORD_TYPE = {"1": "aguda", "2": "llana", "3": "esdrújula"}


class Localization:
    """
        Localisation defines prompts used outside classes.
        Mostly used for user interaction prompts.
    """
    def __init__(self, locale):
        self.ACCENT_OR_NOT = loc.ACCENT_OR_NOT[locale]
        self.DIACRITIC_ALREADY_USED = loc.DIACRITIC_ALREADY_USED[locale]
        self.FEEDBACK_OK = loc.FEEDBACK_OK[locale]
        self.FEEDBACK_WRONG = loc.FEEDBACK_WRONG[locale]
        self.GOOD_LUCK = loc.GOOD_LUCK[locale]
        self.HEARD_EMPHASIS = loc.HEARD_EMPHASIS[locale]
        self.HOW_MANY_TIMES = loc.HOW_MANY_TIMES[locale]
        self.WHICH_SYLLABLE = loc.WHICH_SYLLABLE[locale]
        self.WHICH_WORD = loc.WHICH_WORD[locale]
        self.WRONG_INPUT_NUMBER = loc.WRONG_INPUT_NUMBER[locale]
        self.WRONG_INPUT_YESNO = loc.WRONG_INPUT_YESNO[locale]


class Word:
    def __init__(self, word):
        self.word = word
        self._length, self._syllables = self.split_in_syllables()
        self.type = self.determine_type()
        self.SYLLABICATION_ERROR = loc.SYLLABICATION_ERROR[locale]

    def ends_with_vowel(self):
        return self.word[-1] in VOWELS

    def _ends_with_diacritic(self):
        return self.word[-1] in DIACRITICS

    def ends_with_n_s(self):
        return self.word[-1] in N_OR_S

    def ends_with_something_else(self):
        return not (self.ends_with_vowel() or self._ends_with_diacritic() or self.ends_with_n_s())

    def _has_diacritic_before(self):
        return self.word[-2] in DIACRITICS

    def _diacritic_in_second_syllable(self):
        syllable = self._syllables[-2]
        for char in syllable:
            if char in DIACRITICS:
                return True
        return False

    def diacritic_in_word(self):
        for char in self.word:
            if char in DIACRITICS:
                return True
        return False

    def _is_aguda(self):
        if self._ends_with_diacritic():
            return True
        elif self.ends_with_n_s() and self._has_diacritic_before():
            return True
        elif self.ends_with_something_else() and not self._diacritic_in_second_syllable():
            return True
        else:
            return False

    def _is_llana(self):
        if self.ends_with_vowel():
            return True
        elif self.ends_with_n_s() and not self._has_diacritic_before():
            return True
        elif self.ends_with_something_else() and self._diacritic_in_second_syllable():
            return True
        else:
            return False

    def _is_esdrujula(self):
        syllable = self._syllables[-3]
        for char in syllable:
            if char in DIACRITICS:
                return True
        return False

    def determine_type(self):
        """determines the word type based on its written form"""

        # if word is esdrujula
        if self._length >= 3 and self._is_esdrujula():
            to_return = "3"

        # If words ends with vowel, the word is llana
        # It is llana, example >> canto
        elif self.ends_with_vowel():
            to_return = "2"

        # If words ends with n or s
        elif self.ends_with_n_s():
            # It is aguda, example >> camión
            if self._has_diacritic_before():
                to_return = "1"
            # It is llana, example >> carmen
            else:
                to_return = "2"

        # if words ends with something else
        elif self.ends_with_something_else():
            # It is llana, example >> cóndor
            if self._diacritic_in_second_syllable():
                to_return = "2"
            # It is aguda, example >> cantor
            else:
                to_return = "1"
        else:
            to_return = "1"

        return to_return

    def split_in_syllables(self):
        syllables_list = dic.inserted(self.word).split("-")
        length = len(syllables_list)
        try:
            # we don't accept monosyllabic words
            assert length >= 2
            return length, syllables_list
        except:
            print(self.SYLLABICATION_ERROR)


class AccentRules:
    def __init__(self, given_word, heard_accent, locale):
        self.w = given_word
        self._estimated_type = "No sé"

        # prompts
        self.ADVICE_NO = loc.ADVICE_NO[locale]
        self.ADVICE_YES = loc.ADVICE_YES[locale]
        self.AGUDAS_SOMETHING_ELSE = loc.AGUDAS_SOMETHING_ELSE[locale]
        self.AGUDAS_VOWEL_N_S = loc.AGUDAS_VOWEL_N_S[locale]
        self.ALL_ESDRUJULAS = loc.ALL_ESDRUJULAS[locale]
        self.EMPHASIS_EXPLANATION = loc.EMPHASIS_EXPLANATION[locale]
        self.LIKE_THAT = loc.LIKE_THAT[locale]
        self.LLANAS_SOMETHING_ELSE = loc.LLANAS_SOMETHING_ELSE
        self.LLANAS_VOWEL_N_S = loc.LLANAS_VOWEL_N_S[locale]
        self.SYLLABICATION_ERROR = loc.SYLLABICATION_ERROR[locale]

        # user doesn't know where the emphasis is
        if heard_accent == "0":
            print(self.EMPHASIS_EXPLANATION)
        else:
            # user input is 1, 2 or 3
            # self._estimated_type = WORD_TYPE[heard_accent]
            self._estimated_type = heard_accent

    def _write_accent(self, index):
        length, syllables = self.w.split_in_syllables()
        try:
            # assuming there is only one vowel no ai, oi, ei, etc
            for character in syllables[-index]:
                for count, vowel in enumerate(VOWELS):
                    if character == vowel:
                        syllables[-index].replace(character, DIACRITICS[count])
                        new_syllable = syllables[-index].\
                                       replace(character, DIACRITICS[count])
                        syllables[-index] = new_syllable

            return "".join(syllables)
        except IndexError:
            print(self.SYLLABICATION_ERROR)

    def determine_written_accent(self):
        """
        determines whether an accent should be written based
        on where the user hears the word emphasis
        :returns a tuple representing the advise
        (word type, True if diatritic needed, word correct spelled, message)
        """

        # word type, write or not, new word, explanation
        diacritic = False
        correct_form = ""
        message = ""

        # esdrújula
        if self._estimated_type == '3':
            diacritic = True
            correct_form = self._write_accent(3)
            message = self.ALL_ESDRUJULAS

        # aguda
        elif self._estimated_type == '1':
            if self.w.ends_with_vowel() or self.w.ends_with_n_s():
                diacritic = True
                correct_form = self._write_accent(1)
                message = self.AGUDAS_VOWEL_N_S
            else:
                diacritic = False
                correct_form = self.w.word
                message = self.AGUDAS_SOMETHING_ELSE
        # llana
        elif self._estimated_type == '2':
            if self.w.ends_with_something_else():
                diacritic = True
                correct_form = self._write_accent(2)
                message = self.LLANAS_SOMETHING_ELSE
            else:
                diacritic = False
                correct_form = self.w.word
                message = self.LLANAS_VOWEL_N_S

        # return advice
        return self._estimated_type, diacritic, correct_form, message

    def build_advice_prompt(self):
        sort, add_accent, correct_word, explanation = self.determine_written_accent()

        if add_accent:
            return self.ADVICE_YES.format(sort) + self.LIKE_THAT.format(correct_word), explanation
        else:
            return self.ADVICE_NO.format(self.w.word), explanation


def pick_up_word_at_random():
    """
    picks up a random value of a list of dictionary keys
    """
    return random.choice(list(WORDS_BAG))


def check_input_value(user_input):
    """
        :raises a KeyError if the value given is not correct
    """
    try:
        if user_input not in ["0", "1", "2", "3"]:
            raise KeyError
    except KeyError:
        print(prompt.WRONG_INPUT_NUMBER)
        sys.exit()


def guess_the_type():
    """
        creates an exercise to practice the classification
         of words in aguda, llana or esdrújula
    """

    times = int(input(prompt.HOW_MANY_TIMES))
    count_good_one = 0
    count_bad_one = 0

    for t in range(times):
        word = pick_up_word_at_random()
        user_answer = input(prompt.WHICH_SYLLABLE.format(word))

        # check_input_value will raise exception if wrong value
        check_input_value(user_answer)

        w = Word(word)
        right_answer = w.determine_type()

        # user or system answer is "1", "2", "3 or "0"
        right_answer_value = WORD_TYPE[right_answer]

        # TODO unify feedback procedure with "do_you_write..."
        if user_answer == right_answer:
            print(prompt.FEEDBACK_OK)
            count_good_one += 1
        else:
            print(prompt.FEEDBACK_WRONG.format(right_answer_value))
            if t < times - 1:
                print(prompt.GOOD_LUCK)
                count_bad_one += 1


def do_i_write_accent(word, locale):
    """
        gives advice to the user on how to write a word
        prints the correct word
        explains the rule used
    """
    # if no word was given in command line
    if word == "":
        word_to_treat = input(prompt.WHICH_WORD)
    else:
        word_to_treat = word
    try:
        w = Word(word_to_treat)

        # check that the user didn't used á, é, í, ó or ú
        assert not w.diacritic_in_word()

        # ask user where the emphasis is heard
        input_accent = input(prompt.HEARD_EMPHASIS)

        # check_input_value will raise exception if wrong value
        check_input_value(input_accent)

        # give advice, show correct word and explain
        explanation = AccentRules(w, input_accent, locale)
        word_advice, why = explanation.build_advice_prompt()
        print(word_advice, why)

    except AssertionError:
        print(prompt.DIACRITIC_ALREADY_USED)


def is_answer_yes(answer):
    # TODO localize in localisation.py
    # possible answers are: yes, yeah, 1, ja
    yes = compile(r"^[yY]([eE][(ah|AH)sS])|1|[jJ][aA]|s[iIíÍ]")
    return yes.match(answer)


def is_answer_no(answer):
    # TODO localize in localisation.py
    # No, Nee, no, nee, NEE, NO, nEE, nO or 0
    no = compile(r"((^[nN]([oO]|[eE]{2})$)|0)")


def clean_split_word(word_list):
    show_word = []
    for syllable in word_list:
        for diacritic in DIACRITICS:
            vowel_index = DIACRITICS.index(diacritic)
            syllable = syllable.replace(diacritic, VOWELS[vowel_index])
        show_word.append(syllable)
    return show_word


def clean_split_word1(word_list):
    show_word = []
    for syllable in word_list:
        for diacritic in DIACRITICS:
            if diacritic in syllable:
                vowel_index = DIACRITICS.index(diacritic)
                syllable = syllable.replace(diacritic, VOWELS[vowel_index])
        show_word.append(syllable)
    return show_word


def clean_split_word2(word_list):
    show_word = []
    for syllable in word_list:
        syllable = syllable.replace("á", "a")\
                           .replace("é", "e")\
                           .replace("í", "i")\
                           .replace("ó", "o")\
                           .replace("ú", "u")
        show_word.append(syllable)
    return show_word


def do_you_write_accent():
    # chose word for question
    chosen_word = random.choice(list(UNFAMILIAR_WORDS))

    # instantiate word
    w = Word(chosen_word)

    # determine word type: 2 llana, 1 aguda or 3 esdrújula
    word_type = w.determine_type()

    # split word in syllable
    _, word_splitsing = w.split_in_syllables()

    # determine write advice
    # right_answer True if diacritic needed
    # right now is locale a global variable, hummmm
    explanation = AccentRules(w, word_type, locale)
    _, right_answer, _, feedback = explanation.determine_written_accent()

    # hide diacritics, look type up and make a question
    cleaned_word = clean_split_word1(word_splitsing)
    word_type = WORD_TYPE[word_type]
    answer = input(prompt.ACCENT_OR_NOT.format(cleaned_word, word_type))

    # user_answer initialisation
    user_answer = False

    # check user input
    try:
        if is_answer_yes(answer):
            user_answer = True
        elif is_answer_no(answer):
            user_answer = False
        else:
            raise ValueError
    except ValueError:
        print(prompt.WRONG_INPUT_YESNO)
        sys.exit()

    # primitive feedback
    if right_answer == user_answer:
        print(prompt.FEEDBACK_OK)
    else:
        print(prompt.FEEDBACK_WRONG.format(word_type), feedback)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='This program helps you how'
                                                 ' to use accents in Spanish')
    parser.add_argument('-l', dest='locale', choices=['en', 'es', 'nl'], default="es",
                        help='The locale language the program will use (en, es, nl)')
    parser.add_argument('-w', dest='word', default="",
                        help='The word you want to consult')
    parser.add_argument('-guess', dest='users_choice', action='store_const',
                        const=guess_the_type, default=do_i_write_accent,
                        help="-guess will run a program to train you "
                             "in determining the word type,\notherwise you will"
                             " be able to consult a word")
    parser.add_argument('-learn', dest='users_choice', action='store_const',
                        const=do_you_write_accent, default=do_i_write_accent,
                        help="-learn will run a program to train you in "
                              "determining the accent\n otherwise you will be "
                             "able to consult a word")
    arguments = parser.parse_args()

    # locale` is by default Spanish but can be changed in cmd line
    locale = arguments.locale

    # prompt read the prompts in localisation.py according to locale
    prompt = Localization(locale)

    function_to_call = arguments.users_choice
    word_to_process = arguments.word

    # do_i_write_accent takes 2 args: word_to_process (by default "") and locale
    # TODO
    if function_to_call == do_i_write_accent:
        function_to_call(word_to_process, locale)

    # do_you_write_an_accent and guess_the_type don't take parameters
    else:
        function_to_call()
