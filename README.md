# acentuar
Workspace to learn how to use diacritics in Spanish

### Virtual environment
Para activar el virtual environment 

Abrir una powershell en la terminal y 
    & d:/git/acentuar/venv/Scripts/Activate.ps1

##### Usage
     python acentuar.py -guess
     It will call guess_the_type()
     This will start an exercise to practice classification of words in llanas, agudas or esdrújulas

     python acentuar.py -w catalizador
     It will call do_i_write_accent("catalizador")
     This will answer the question of catalizador needs a diacritic or not and why.

     python acentuar.py
     without parameters acentuar.py will ask which word you want to consult
     by calling do_i_write_accent("")
     This is the fastest way to get your answer

     python acentuar.py -learn
     It will call do_you_write_an_accent()
     It will ask you to determine whether an unusual word needs accent or not
     and will give you feedback about your answer

##### UI language
LOCALE is by default Spanish but can be changed in cmd line

    -l en
    will use English as UI language. Use nl for Dutch

##### Possible functionalities to extend the program

* replace pyphen with another library
* handle digtongues: two or three vowels together
  * 'caligrafía' can't be handle correctly, for instance
* handle exceptions:
  * right now acentuar does not handle monosyllabic words like 'sí' or 'si'
  * 'solo' or 'sólo', 'esta' or 'ésta'
* replace WORDS_BAG with data out nltk corpus or scrapped out the internet
* convert into package
* chose how many times you want to practice with -learn


##### about using Hunspell dictionaries
https://www.researchgate.net/publication/220948080_Building_and_Using_Existing_Hunspell_Dictionaries_and_TeX_Hyphenators_as_Finite-State_Automata
