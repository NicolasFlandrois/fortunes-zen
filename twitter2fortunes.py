#!/usr/bin/python3
# Date: Monday, May 11rd, 2020
# https://tweepy.readthedocs.io/en/latest/
# This version is ready to be used in a CRONTAB schedule
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime as dt
import pandas as pd
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
        splited_quotes = [n.split('    — ') for n in clean_list]

        df = pd.DataFrame(splited_quotes, columns=['Quotes', 'Authors'])

        return df


def new_fortunes(source_dataframe, tweet_input: list):
    """This function will use Pandas module. Given a database and
    a list of input, as arguments. Then it will parse and standardize the input,
    before comparing if the same input already exist in the database.
    The format Used here is specific for a specific source, from '@ZenProverbs'
    twitter Zen quotation bot."""
    source_df = source_dataframe

    new_data = tweet_input
    clean_quotes = [item.replace('"', '').replace(
        'ﾟ', '').replace('\n', '').replace(
        '#', "- ").strip().split('      — ') for item in new_data]
    new_df = pd.DataFrame(clean_quotes, columns=['Quotes', 'Authors'])
    df_filtered = new_df[~new_df['Quotes'].str.contains('https://')]

    concat_df = pd.concat([source_df, df_filtered])
    concat_df.drop_duplicates(subset=['Quotes'], inplace=True, keep='last')
    # Test
    print(source_df)
    print(df_filtered.to_string())
    print(concat_df)

    # with open(destination_file, 'w') as f:
    #     pass


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
subject_success = f'Twitter Bot - SUCCESS - \
{dt.now().strftime("%A, %d. %B %Y %I:%M%p")}'

msg_success = f"""This email was automatically sent by your Twitter bot.
Your Twitter Account Successfully liked your favorit twitter-friends.
{dt.now().strftime("%A, %d. %B %Y %I:%M%p")}
"""

body_html_success = f"""<!DOCTYPE html>
<html>
    <body>
        <h1 style="color:SlateGray;">Your Twitter Account Successfully liked your favorit twitter-friends.</h1>
        <p>This email was automatically sent by your Twitter bot.</p>
        <p>Your Twitter-bot is setup to like the last 20 tweets not liked yet, from each friend's account in your list.</p>
        <p>The Twitter bot last worked on {dt.now().strftime("%A, %d. %B %Y %I:%M%p")}.</p>
    </body>
</html>"""

# Failed
subject_failed = f'Twitter Bot - FAILED - \
{dt.now().strftime("%A, %d. %B %Y %I:%M%p")}'

msg_failed = f"""This email was automatically sent by your Twitter bot.
Your Twitter Account failed to like your favorit twitter-friends.
{dt.now().strftime("%A, %d. %B %Y %I:%M%p")}
"""

body_html_failed = f"""<!DOCTYPE html>
<html>
    <body>
        <h1 style="color:SlateGray;">Your Twitter Account <b>FAILED</b> to like your favorit twitter-friends.</h1>
        <p>This email was automatically sent by your Twitter bot.</p>
        <p>The Twitter bot last worked on {dt.now().strftime("%A, %d. %B %Y %I:%M%p")}.</p>
    </body>
</html>"""

##############################################################################
#                              End of Variables                              #
##############################################################################


if __name__ == "__main__":

    new_fortunes(fortune2dataframe('zen'), twtr_bot(API_Key, API_Secret_Key, AccessToken,
                                                    AccessTokenSecret, usernames_list))

# In order to send or not the email, we can check if new data has been appended ?
#     send_email(from_addr, gmail_key, to_addrs,
#                subject_success, msg_success, body_html_success)
# else:
#     send_email(from_addr, gmail_key, to_addrs,
#                subject_failed, msg_failed, body_html_failed)

##############################################################################
# Checkpoints
# X 1/ Check the text from that username 's twitter
# 2/ Clean & Standardize the tweet txt data
#       X a/ remove quotation marks (All kind)
#       X b/ remove '\n'
#       X c/ IGNORE data containing "https://" > Thoses data are useless, quote isn't completed
#       ~ d/ remove unwanted caracters, trailing symboles
#       X e/ Split quote/author
# X 3/ Download zen fortunes data from source file >> Use Pandas
# X 4/ Check if new quote already exist in my DB (DB from n° 3)
# X 5/ Append the DB
# 6/ Export/Write DB into destination file zen_fortunes 'zen'