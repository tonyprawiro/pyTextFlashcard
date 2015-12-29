# pyTextFlashcard
A simple text-based flashcard engine to help with memorizing concepts

Usage: `$ python flashcards-engine.py FLASHCARDSNAME`

E.g: `$ python flashcards-engine.py HISTORICALFIGURES`

The flashcard is assumed to be a simple Keywords-Definitions.

The engine shuffles the flashcards set, and show the cards for user to guess.

Either a keyword or a definition of a card is shown, randomly. User is asked to press Enter to reveal the entire card. And then enter 1 if they guessed correctly, or 0 if they guessed incorrectly. An honest assessment is expected :-)

A session will last forever unless user enters "Q" which means start assessment. Assessment is done based on sections (chapters, modules) so that the user can evaluate themselves and figure out which sections are their weaknesses and read more on that chapters.

The cards are stored as text file with the following format:

```
[Section Name 1]
---
Keyword
KeywordAlternative
|
Definition
DefinitionAlternative
---

[Section Name 2]

---
Keyword
KeywordAlternative
|
Definition
DefinitionAlternative
---
```
