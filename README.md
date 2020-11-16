# powertamil

The 63,000+ words and their meanings in a Tamil to Tamil Dictionary.

[![License](https://img.shields.io/:license-mit-blue.svg)](./LICENSE.md)

The Tamil-Tamil AgaraMuthali (also known as Agaramuthali) is a public domain pronouncing dictionary created by Tamilnadu Textbook Society, Chennai. It defines a mapping from Tamil words to their Tamil meanings, and is commonly used in Natural Language Processing applications.


Crawled from http://www.tamilvu.org/library/ldttam/html/ldttamin.htm

AgaraMuthali is authored by :
[M.Shanmugam Pillai]()

Supervised by
    [Prof. A.S.GnanaSambhandam](),
    [Prof. A.M.ParamaSivanandham](),
    [Prof. Kondal S.Mahadevan]()

# Build
Building on windows 10:

1.Install Qt for Python.

2.Use pip to install PySide2 and its dependency Shiboken2(Python binding generator).
    pip install PySide2

3.Use VSCode IDE to compile and run the PTDictionary.py file.

# Other information
The words in the dictionary may have an ambiguous, figurative or meaning other than widespread use. Also, the dictionary is seeded with the contents of AgaraMuthali as a starter.

Anyone can take part in the compilation of the dictionary. You can suggest a new term, open a translation discussion, or simply correct a mistake or inaccuracy by opening an issue.


# Compiling a dictionary
There are two ways to get involved in building a frontend dictionary:

    1.Suggest a new term for translation
    2.Suggest a better translation of an existing term.

Any of these actions is best done using a pull request, but you can just start a task with discussion. Until there is a clear approach to the design of a dictionary entry, formulate new terms based on existing examples.

Attention, do not forget to sync your fork with the main repository before starting editing to avoid conflicts, see the help. If your pull request closes some issue, add a phrase to automatically close the issue when you merge.

The dictionary has a editor(yours truly), so be prepared for the fact that the quality of the text will be monitored, and not all ideas and approaches will find their place.


# License
Built with ♥ by Rajkumar Palani under the `MIT License`.