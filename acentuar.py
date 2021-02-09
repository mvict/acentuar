import random
import pyphen
import nltk

# todo write a bilingual version using string constants and user input for choice
# todo replace pyphen with another library
# todo: think of a way to handle two vowels together and diptongues
# todo: replace WORDS_BAG with data out nltk corpus or wrapped out the internet

VOWELS = ["a", "e", "i", "o", "u"]
DIACRITICS = ["á", "é", "í", "ó", "ú"]
N_OR_S = ["n", "s"]
dic = pyphen.Pyphen(lang='es_ES')

HELP_BY_ACCENT_TEXT = "accent help text"
SYLLABICATION_ERROR = "Something went wrong with Pyphen"


DICTIONARY = {"jamón": 1, "bolígrafo": 3, "esdrújula": 3, "salón": 1, "melón": 1, "excursión": 1,
              "césped": 2, "perro": 2, "gato": 2, "perdiz": 1, "equipo": 2
              }

WORDS_BAG = ["abarrotado", "colombia", "mueve", "abarrotes", "comadreja", "nubes", "abasto",
             "come", "nublado", "abeja", "como", "piojos", "pacto", "canal", "pactar", "sentir",
             "onomatopeya", "escabroso", "viernes", "jueves", "ejercicio", "deberes", "comiendo",
             "experiencia", "jaleo", "resumen", "volumen", "carmen", "bote", "rompe", "romper"]

WORD_TYPE = {"1": "aguda", "2": "llana", "3": "esdrújula"}


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
            print(SYLLABIZATION_ERROR)

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
            print(f"Yes, you should write an accent in {sort} syllable, like that: {correct_word}\n")
        else:
            print(f"No, don't write the accent in {sort}, leave it like that: {correct_word}\n")



def pick_up_word_at_random():
    """picks up a random value of a list of dictionary keys"""
    return random.choice(list(WORDS_BAG))


def guess_the_type():

    times = int(input("¿Cuántas veces quieres jugar? (1-10)   >>>  "))
    count_good_one = 0
    count_bad_one = 0

    for t in range(times):
        word = pick_up_word_at_random()
        user_answer = input(f"¿En qué sílaba se acentúa {word}? >> ")

        w = Word(word)
        right_answer = w.determine_type()

        user_answer_value = WORD_TYPE[user_answer]

        if user_answer_value == right_answer:
            print("Muy bien.")
            count_good_one += 1
        else:
            print(f"No, no, no, es {right_answer}")
            if t < times - 1:
                print("A ver si hay más suerte con la siguiente")
                count_bad_one += 1


def do_i_write_accent():

    input_word = input("Give me a word you don't know how to write >> ")
    input_accent = input("In which syllable do you hear the accent? 1,2,3 (counting from behind).\nSay 0 if you don't know >>> ")

    explanation = AccentRules(input_word, input_accent)
    print(explanation.print_advice())


if __name__ == "__main__":

    choice = input("What would you like to do? Guess emphasis(1) or know how to write(2) >> ")
    if choice == "1":
        guess_the_type()
    elif choice == "2":
        do_i_write_accent()
    else:
        print("Your choices where 1 or 2")
