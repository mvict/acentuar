import unittest
import acentuar


class AcentuarTestCases(unittest.TestCase):

    def test_type_aguda(self):
        types_dictionary = {"cantó": "1", "camión": "1", "cantor": "1"}
        for word in types_dictionary:
            w = acentuar.Word(word)
            self.assertEqual(w.type, types_dictionary[word])

    def test_type_llana(self):
        types_dictionary = {"canto": "2", "cóndor": "2", "carmen": "2"}

        for word in types_dictionary:
            w = acentuar.Word(word)
            self.assertEqual(w.type, types_dictionary[word])

    def test_type_esdrujula(self):
        types_dictionary = {"bolígrafo": "3"}

        for word in types_dictionary:
            w = acentuar.Word(word)
            self.assertEqual(w.type, types_dictionary[word])

    def test_right_advice(self):
        # test if class AccentRules returns the right advice to write the word
        # the value of the dictionary represents the user input
        wordies = {"santo": "2", "condor": "2", "carmen": "2",
                   "colibri": "1", "cantor": "1", "camion": "1",
                   "boligrafo": "3"}
        for key, value in wordies.items():
            print(f"word {key} accent {value}")
            k = acentuar.Word(key)
            acentuation = acentuar.AccentRules(k, value, "es")
            advice, _, _, _ = acentuation.determine_written_accent()
            self.assertEqual(advice, value)

    def test_pyphen(self):
        # not really a unittest but handy to have in place
        for word in acentuar.WORDS_BAG:
            print(acentuar.dic.inserted(word))

    def test_is_esdrujula(self):
        w = acentuar.Word("experiencia")
        self.assertEqual(w._is_esdrujula(), False)


if __name__ == '__main__':
    unittest.main()
