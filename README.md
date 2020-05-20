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

-------------------------------------
# Automated zen update bot

As I sourced all my quotes from a single source, with possible access through an API, I created a bot.
The `twitter2fortunes.py` script will automate the update for me.
It will fetch the new quotes, clean the data, compare and purge duplicates, and update the `zen` text file and the `zen.dat` file.

I created this bot in order to be ***cron* job** friendly.

However, if you want to use this bot in a cron job, the environment variables are not recognised as if you launch this script in your terminal. I would advise, in *production*, to update this file with your ***real** variables* in place. *(If you know how to set a cron job to use environment variables, or where to set env. var. for cron job... Pleas tell me!)* Or you can set and import your variables from a json file.

To edit the crontab, from your terminal: `crontab -e`

Advised Cron Job setting:

    Add (copy & paste) the following line in your crontab:

        # ┌───────────── minute (0 - 59)
        # │ ┌───────────── hour (0 - 23)
        # │ │ ┌───────────── day of month (1 - 31)
        # │ │ │ ┌───────────── month (1 - 12)
        # │ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday;
        # │ │ │ │ │                                       7 is also Sunday on some systems)
        # │ │ │ │ │
        # │ │ │ │ │
        # * * * * *  command_to_execute
        # m h  dom mon dow   command
        0 0 * * * /usr/bin/python3 /home/<your-username-here>/zen/twitter2fortunes.py

-------------------------------------
# Jupiter Notebook - Checkup and Overview

You may also use the Jupiter Notebook available in this repository.

If you use the automated bot mentioned above, this J-notebook allows you to check for any anomalies, and pin-point their locations to you.

Otherwise, it will give you a basic Overview:

    - Sampling the database

    - The number of Quotes

    - Which Author has been the most quoted
