from tkinter import *

import matplotlib.pyplot as plt
import tweepy
from textblob import TextBlob

import driver_functions as df
import twitterCredentials

# GUI begin

home = Tk()
home.title("TSA")
home.iconbitmap('twitter.ico')
# Heading
head = Label(home, text="Twitter Sentiment Analyzer")
head.pack(padx=15, pady=5)

# Input frame for required args
args = Frame(home)
args.pack(padx=10, pady=10, fill=X)

# Input field
Label(args, text="Enter the terms: ").grid(row=0, column=0)
tweet_terms = Entry(args, font=('MS Sans', 13))
tweet_terms.grid(row=0, column=1)

Label(args, text="Enter number of tweets: ").grid(row=1, column=0)
tweet_count = Entry(args, font=('MS Sans', 13))
tweet_count.grid(row=1, column=1)
args.grid_columnconfigure(0, weight=1)


# GUI Ends

def analyse_tweet():
    auth = tweepy.OAuthHandler(twitterCredentials.CONSUMER_KEY, twitterCredentials.CONSUMER_SECRET)
    auth.set_access_token(twitterCredentials.ACCESS_TOKEN, twitterCredentials.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    terms = tweet_terms.get()
    no_of_tweets = int(tweet_count.get())

    tweets = tweepy.Cursor(api.search, q=terms, lang="en").items(no_of_tweets)

    positive = 0
    negative = 0
    neutral = 0
    polarity = 0

    for tweet in tweets:
        analysis = TextBlob(tweet.text)
        polarity += analysis.sentiment.polarity
        print("Tweet =>", tweet.text)
        print("Sentiment =>", df.check_poll(analysis.sentiment[0]))
        print("\n")
        if analysis.sentiment.polarity == 0.00:
            neutral += 1
        elif analysis.sentiment.polarity < 0.00:
            negative += 1
        elif analysis.sentiment.polarity > 0.00:
            positive += 1

    positive = df.percentage(positive, no_of_tweets)
    negative = df.percentage(negative, no_of_tweets)
    neutral = df.percentage(neutral, no_of_tweets)

    positive = format(positive, '.2f')
    negative = format(negative, '.2f')
    neutral = format(neutral, '.2f')

    if positive > neutral:
        if positive > negative:
            poll = "Positive"
        else:
            poll = "Negative"
    else:
        if neutral > negative:
            poll = "Neutral"
        else:
            poll = "Negative"

    result['text'] = f"By analysing {str(no_of_tweets)} Tweets, the overall sentiment\nturns out to be {poll}"

    # Graph plot
    labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]',
              'Negative [' + str(negative) + '%]']
    sizes = [positive, neutral, negative]
    colors = ['green', 'blue', 'red']
    patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.title("By analysing " + str(no_of_tweets) + " Tweets")
    plt.axis("equal")
    plt.tight_layout()
    plt.show()


analyse = Button(home, text="Analyse", command=analyse_tweet)
analyse.pack(pady=5)

# Result frame

result = Label(home, text="")
result.pack(fill=X, padx=10, pady=10)

home.mainloop()
