# acentuar
Workspace to learn how to use diacritics in Spanish

##### Usage
     --guess
     it will call guess_the_type()

     --w catalizador
     it will call do_i_write_accent("catalizador")

     without parameters acentuar.py will ask which word you want to consult
     by calling do_i_write_accent("")

##### UI language
LOCALE is by default Spanish but can be changed in cmd line

##### Possible functionalities to extend the program

* replace pyphen with another library
* handle digtongues: two or three vowels together
* replace WORDS_BAG with data out nltk corpus or scrapped out the internet
* convert into package

##### about using Hunspell dictionaries
https://www.researchgate.net/publication/220948080_Building_and_Using_Existing_Hunspell_Dictionaries_and_TeX_Hyphenators_as_Finite-State_Automata
