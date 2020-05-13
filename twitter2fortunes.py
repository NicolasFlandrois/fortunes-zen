#!/usr/bin/python3
# Date: Monday, May 11rd, 2020
# https://tweepy.readthedocs.io/en/latest/
# This version is ready to be used in a CRONTAB schedule
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime as dt
import pandas as pd
import numpy as np
import tweepy

# print(f'\nTime :\t{dt.now()}\n\nTwitter Script starting. Please wait.')


def send_email(from_addr, gmail_key,
               to_addrs, subject,
               body_txt='DEFAULT - This is a plain text email',
               body_html=None, attached_file=None):
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = from_addr
        msg['To'] = to_addrs

        msg.set_content(body_txt)  # Body as text

        if body_html is not None:
            msg.add_alternative(body_html, subtype='html')  # Body as HTML

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(from_addr, gmail_key)
            smtp.send_message(msg)
            print('Email sent successfully')

    except Exception as e:
        print(e)
        print('\nEmail failed to send.')


def twtr_bot(API_Key, API_Secret_Key, AccessToken, AccessTokenSecret, usernames_list):
    auth = tweepy.OAuthHandler(API_Key, API_Secret_Key)
    auth.set_access_token(AccessToken, AccessTokenSecret)

    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    twt_txt = []

    for username in usernames_list:
        tmpTweets = api.user_timeline(
            screen_name=username)

        for tweet in tmpTweets:
            try:
                twt_txt.append(tweet.text)

            except:
                pass

    return twt_txt


def fortune2dataframe(source_file):
    """Given the Source file path/name, this function will transform the raw
    data into a Pandas' dataframe. This function is specifically made to suite
    a fortune-mod standardized format, as an input."""
    with open(source_file, 'r') as f:
        data = f.read()
        quote_list = data.replace('\n', '').split('%')
        clean_list = [x.strip() for x in quote_list if x]
        splited_quotes = [n.split('     — ') for n in clean_list]

        df = pd.DataFrame(splited_quotes, columns=['Quotes', 'Authors'])

        return df


def new_fortunes(source_dataframe, tweet_input: list, output_file_name):
    """This function will use Pandas module. Given a database and
    a list of input, as arguments. Then it will parse and standardize the input,
    before comparing if the same input already exist in the database.
    The format Used here is specific for a specific source, from '@ZenProverbs'
    twitter Zen quotation bot."""

    # Setting  source dataframe
    source_df = source_dataframe

    # Managing New Data
    new_df = pd.DataFrame([item.replace('"', '').replace(
        'ﾟ', '').replace('\n', '').replace(
        '#', "- ").strip().split('     — ') for item in tweet_input], columns=['Quotes', 'Authors'])
    df_filtered = new_df[~new_df['Quotes'].str.contains('https://')]

    # Concatenate both dtatframes (Source + New_clean) & Purge Duplicates
    concat_df = pd.concat([source_df, df_filtered])
    concat_df.drop_duplicates(
        subset=['Quotes'], inplace=True, keep='last')

    # Export to txt fortunes format file
    quotes_string = "\n%\n".join([
        f'{n[0]}\n\n     — {n[1]}' for n in concat_df.values.tolist()])
    # output_string = f'%\n{quotes_string}\n%'

    with open(output_file_name, "w") as f:
        f.write(f'%\n{quotes_string}\n%')

    concat_rows = concat_df['Quotes'].count()
    source_rows = source_df['Quotes'].count()

    return int(concat_rows - source_rows)


##############################################################################
#                                Variables                                   #
##############################################################################



# Twitter Variables
API_Key = os.environ.get('TWTR_API_KEY')
API_Secret_Key = os.environ.get('TWTR_API_SECRET_KEY')

AccessToken = os.environ.get('TWTR_ACCESS_TOKEN')
AccessTokenSecret = os.environ.get('TWTR_ACCESS_TOKEN_SECRET')

usernames_list = ['@ZenProverbs']

# Email Variables
from_addr = os.environ.get('EMAIL_USER')
gmail_key = os.environ.get('EMAIL_PASS')

to_addrs = from_addr

# Succeed
subject_success = f'Zen Fortunes Compile Bot - UPDATED - \
{dt.now().strftime("%A, %d. %B %Y %I:%M%p")}'

msg_success = f"""This email was automatically sent by your Twitter bot.
Your Twitter Account Successfully liked your favorit twitter-friends.
{dt.now().strftime("%A, %d. %B %Y %I:%M%p")}
"""

# Failed
subject_failed = f'Zen Fortunes Compile Bot - NO UPDATES - \
{dt.now().strftime("%A, %d. %B %Y %I:%M%p")}'

msg_failed = f"""This email was automatically sent by your Twitter bot.
No New Tweets were append to your database.
{dt.now().strftime("%A, %d. %B %Y %I:%M%p")}
"""

body_html_failed = f"""<!DOCTYPE html>
<html>
    <body>
        <h1 style="color:SlateGray;">The update <b>FAILED</b> to append new quotes.</h1>
        <p>This email was automatically sent by your Twitter bot.</p>
        <p>The Twitter bot last worked on {dt.now().strftime("%A, %d. %B %Y %I:%M%p")}.</p>
    </body>
</html>"""

##############################################################################
#                              End of Variables                              #
##############################################################################


if __name__ == "__main__":

    delta = new_fortunes(fortune2dataframe('zen'), twtr_bot(API_Key, API_Secret_Key, AccessToken,
                                                            AccessTokenSecret, usernames_list), 'zen')

    if delta == 0:
        send_email(from_addr, gmail_key, to_addrs,
                   subject_failed, msg_failed, body_html_failed)
    else:
        body_html_success = f"""<!DOCTYPE html>
<html>
    <body>
        <h1 style="color:SlateGray;">Your Zen_Fortune auto update bot successfully updated {delta} new quotes.</p>
        <p>Your Twitter-bot is setup to check and update the last 20 tweets written, from each twitter target's account in your list.</p>
        <p>Target Account: {usernames_list}
        <p>This Twitter bot last worked on {dt.now().strftime("%A, %d. %B %Y %I:%M%p")}.</p>
    </body>
</html>"""

        send_email(from_addr, gmail_key, to_addrs,
                   subject_success, msg_success, body_html_success)

    os.system('strfile zen')
