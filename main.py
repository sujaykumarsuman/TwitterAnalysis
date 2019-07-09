import matplotlib.pyplot as plt
import tweepy
from textblob import TextBlob
import app
import twitterCredentials


def percentage(part, whole):
    return 100 * float(part) / float(whole)


def check_poll(sen):
    if sen == 0.0:
        return 'Neutral'
    elif sen > 0.0:
        return 'Positive'
    else:
        return 'Negative'


def analyse_tweet():

    auth = tweepy.OAuthHandler(twitterCredentials.CONSUMER_KEY, twitterCredentials.CONSUMER_SECRET)
    auth.set_access_token(twitterCredentials.ACCESS_TOKEN, twitterCredentials.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    terms = app.tweet_terms.get()
    no_of_tweets = int(app.tweet_count.get())

    tweets = tweepy.Cursor(api.search, q=terms, lang="en").items(no_of_tweets)

    positive = 0
    negative = 0
    neutral = 0
    polarity = 0

    for tweet in tweets:
        analysis = TextBlob(tweet.text)
        polarity += analysis.sentiment.polarity
        print("Tweet =>", tweet.text)
        print("Sentiment =>", check_poll(analysis.sentiment[0]))
        print("\n")
        if analysis.sentiment.polarity == 0.00:
            neutral += 1
        elif analysis.sentiment.polarity < 0.00:
            negative += 1
        elif analysis.sentiment.polarity > 0.00:
            positive += 1

    positive = percentage(positive, no_of_tweets)
    negative = percentage(negative, no_of_tweets)
    neutral = percentage(neutral, no_of_tweets)

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

    app.result['text'] = f"By analysing {str(no_of_tweets)} Tweets, the overall sentiment\nturns out to be {poll}"

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
