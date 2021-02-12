import random
import pyphen
import nltk
import localisation as loc
import argparse

# todo replace pyphen with another library
# todo: think of a way to handle two vowels together and diptongues
# todo: replace WORDS_BAG with data out nltk corpus or scrapped out the internet
# todo: include exceptions
# todo: convert into package to send to Clara
# todo: include explanation about the accentuation system _explanation_about_accents

VOWELS = ["a", "e", "i", "o", "u"]
DIACRITICS = ["á", "é", "í", "ó", "ú"]
N_OR_S = ["n", "s"]
dic = pyphen.Pyphen(lang='es_ES')

DICTIONARY = {"jamón": 1, "bolígrafo": 3, "esdrújula": 3, "salón": 1, "melón": 1, "excursión": 1,
              "césped": 2, "perro": 2, "gato": 2, "perdiz": 1, "equipo": 2
              }

WORDS_BAG = ["abarrotado", "colombia", "mueve", "abarrotes", "comadreja", "nubes", "abasto",
             "come", "nublado", "abeja", "como", "piojos", "pacto", "canal", "pactar", "sentir",
             "onomatopeya", "escabroso", "viernes", "jueves", "ejercicio", "deberes", "comiendo",
             "experiencia", "jaleo", "resumen", "volumen", "carmen", "bote", "rompe", "romper"]

WORD_TYPE = {"1": "aguda", "2": "llana", "3": "esdrújula"}

class Localization:
    def __init__(self, locale):
        self.ADVICE_YES = loc.ADVICE_YES[locale]
        self.ADVICE_NO = loc.ADVICE_NO[locale]
        self.FEEDBACK_OK = loc.FEEDBACK_OK[locale]
        self.FEEDBACK_WRONG = loc.FEEDBACK_WRONG[locale]
        self.GOOD_LUCK = loc.GOOD_LUCK[locale]
        self.HEARD_EMPHASIS = loc.HEARD_EMPHASIS[locale]
        self.HELP_BY_ACCENT_TEXT = loc.HELP_BY_ACCENT_TEXT[locale]
        self.HOW_MANY_TIMES = loc.HOW_MANY_TIMES[locale]
        self.LIKE_THAT = loc.LIKE_THAT[locale]
        self.SYLLABICATION_ERROR = loc.SYLLABICATION_ERROR[locale]
        self.WHICH_SYLLABLE = loc.WHICH_SYLLABLE[locale]
        self.WHICH_WORD = loc.WHICH_WORD[locale]

class Word:
    def __init__(self, word):
        self.word = word
        self._length, self._syllables = self.split_in_syllables()
        self.type = self.determine_type()

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
            to_return = "esdrújula"

        # If words ends with vowel
        # example >> canto
        elif self.ends_with_vowel():
            to_return = "llana"

        # If words ends with n or s
        elif self.ends_with_n_s():
            # example >> camión
            if self._has_diacritic_before():
                to_return = "aguda"
            # example >> carmen
            else:
                to_return = "llana"

        # if words ends with something else
        elif self.ends_with_something_else():
            # example >> cóndor
            if self._diacritic_in_second_syllable():
                to_return = "llana"
            # example >> cantor
            else:
                to_return = "aguda"
        else:
            to_return = "aguda"

        return to_return

    def split_in_syllables(self):
        syllables_list = dic.inserted(self.word).split("-")
        length = len(syllables_list)
        try:
            # we don't accept monosyllabic words
            assert length >= 2
            return length, syllables_list

        except:
            print(f"Hyphenation went wrong {length}")


class AccentRules:
    def __init__(self, given_word, heard_accent):
        self.w = Word(given_word)
        self._estimated_type = "No sé"

        if heard_accent == "0":
            print(self._explanation_about_accents())
        else:
            # user input is 1, 2 or 3
            self._estimated_type = WORD_TYPE[heard_accent]

    def _explanation_about_accents(self):
        return "big explanation about how the Spanish accent system works"

    def _write_accent(self, index):
        length, syllables = self.w.split_in_syllables()
        try:
            # assuming there is only one vowel no ai, oi, ei, etc
            for character in syllables[-index]:
                for count, vowel in enumerate(VOWELS):
                    if character == vowel:
                        syllables[-index].replace(character, DIACRITICS[count])
                        new_syllable = syllables[-index].replace(character, DIACRITICS[count])
                        syllables[-index] = new_syllable

            return "".join(syllables)
        except IndexError:
            print(prompt.SYLLABIZATION_ERROR)

    def _determine_written_accent(self):
        """determines whether an accent should be written based on where the user hears the word emphasis"""

        # syllable, write or not, new word
        advice = ("", False, "0")

        if self._estimated_type == 'esdrújula':
            advice = ('3', True, self._write_accent(3))

        elif self._estimated_type == 'aguda':
            if self.w.ends_with_vowel() or self.w.ends_with_n_s():
                advice = ('1', True, self._write_accent(1))
            else:
                advice = ('1', False, self.w.word)

        elif self._estimated_type == 'llana':
            if self.w.ends_with_something_else():
                advice = ('2', True, self._write_accent(2))
            else:
                advice = ('2', False, self.w.word)

        return advice

    def print_advice(self):
        sort, add_accent, correct_word = self._determine_written_accent()

        if add_accent:
            return prompt.ADVICE_YES.format(sort) + prompt.LIKE_THAT.format(correct_word)
        else:
            return prompt.ADVICE_NO.format(self.w.word)


def pick_up_word_at_random():
    """picks up a random value of a list of dictionary keys"""
    return random.choice(list(WORDS_BAG))


def guess_the_type():

    times = int(input(prompt.HOW_MANY_TIMES))
    count_good_one = 0
    count_bad_one = 0

    for t in range(times):
        word = pick_up_word_at_random()
        user_answer = input(prompt.WHICH_SYLLABLE.format(word))

        w = Word(word)
        right_answer = w.determine_type()

        user_answer_value = WORD_TYPE[user_answer]

        if user_answer_value == right_answer:
            print(prompt.FEEDBACK_OK)
            count_good_one += 1
        else:
            print(prompt.FEEDBACK_WRONG.format(right_answer))
            if t < times - 1:
                print(prompt.GOOD_LUCK)
                count_bad_one += 1


def do_i_write_accent(word):

    if word == "":
        word_to_treat = input(prompt.WHICH_WORD)
    else:
        word_to_treat = word

    input_accent = input(prompt.HEARD_EMPHASIS)

    explanation = AccentRules(word_to_treat, input_accent)

    print(explanation.print_advice())


if __name__ == "__main__":
    # usage
    # --guess
    # it will then call guess_the_type()

    # --w catalizador
    # it will call do_i_write_accent("catalizador")

    # without parameters it will ask which word you want to consult
    # it will call do_i_write_accent("")

    parser = argparse.ArgumentParser(description='This program helps you learn your accents in Spanish')
    parser.add_argument('--l', dest='locale', choices=['en', 'es', 'nl'], default="es",
                        help='The locale language you want the program to address you (en, es, nl)')
    parser.add_argument('--w', dest='word', default="",
                        help='The word you want to consult')
    parser.add_argument('--guess', dest='users_choice', action='store_const',
                        const=guess_the_type, default=do_i_write_accent,
                        help="guess will run a program to train you in determining the accent\n"
                             "otherwise you will be able to consult a word")

    arguments = parser.parse_args()

    # LOCALE is by default Spanish but can be changed in cmd line
    LOCALE = arguments.locale
    prompt = Localization(LOCALE)

    function_to_call = arguments.users_choice
    word_to_process = arguments.word
    if function_to_call == guess_the_type:
        function_to_call()
    else:
        function_to_call(word_to_process)