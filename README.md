# fortunes-zen
[English] Compilation of zen quotes, set up to use in fortune-mod

************************

This small project sets to customize a quotes database for the application [fortune-mod (cf wikipage)](https://en.wikipedia.org/wiki/Fortune_%28Unix%29), providing fortune cookies on demand.
Fortune program returns a random quote from a given database, and allows its users to add up new database.

-------------------------
## ***Copyghts Diclaimer:***
This project is under **MIT Licencing 2020**. Non Profits.

The usages of this mini program lawfully engages the user's responsability, only.

This program is intended for private uses.

----------------------------
# Installation

1. Clone this repository.

    `git clone https://github.com/NicolasFlandrois/fortunes-zen.git`

2. Paste this 2 files (*zen* and *zen.dat*) in following fortunes directory (Unix/Linux files system here):

    `/usr/share/games/fortunes`

3. Run your fortune application with zen

    `fortune zen`

-------------------------------------
# How to customize your own database

1. Create (or modify) your file. a simple file, with or without .txt extension.

    (Unix/Linux)

    `touch my_zen_quotes`

2. Edit this file with your new quotes. Use the text editeur of your choice. Each quotes must be contained in between 2 % symboles.

    >
    >%
    >
    >"Zen is not some kind of excitement, but concentration on our usual everyday routine."
    > — Shunryu Suzuki
    >
    >%
    >
    >"Since the time we were born from our mother's womb, the only thing we have seen is the present. We have never seen the past and we have never seen the future. Wherever we are, whatever time it is, it is only the present."
    > — Khenpo Tsultrim Rinpoche
    >
    >%
    >
    >...etc

3. Save the edited file.

4. Transform your file into a .dat file

    (Unix/Linux)

    `strfile my_zen_quotes`

    The output file will be *my_zen_quotes.dat*

5. Then repeate steps in installation section.
