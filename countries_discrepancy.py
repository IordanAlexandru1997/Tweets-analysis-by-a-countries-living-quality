from mimetypes import init
from numpy import place
import tweepy
from googletrans import Translator
import pandas as pd
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from api_file import apiKey, apiKeySecret, accessToken, accessTokenSecret

translator = Translator()

auth = tweepy.OAuthHandler(apiKey, apiKeySecret)
auth.set_access_token(accessToken, accessTokenSecret)

api = tweepy.API(auth, wait_on_rate_limit=True)


def getTweetsByCountry(country, n=1000):
    places = api.search_geo(query=country, granularity="country")
    place_id = places[0].id

    results = [
        status._json
        for status in tweepy.Cursor(
            api.search_tweets,
            q="place:%s" % place_id,
            tweet_mode="extended",
        ).items(n)
    ]
    return results


def processData(results):
    dictionar = {
        "text": [],
        "likes": [],
        "retweets": [],
        "city": [],
        "sentiment_analysis": [],
        "url": [],
    }
    sia = SentimentIntensityAnalyzer()
    for result in results:
        full_text = translator.translate(result["full_text"], dest="en").text
        dictionar["text"].append(full_text)
        dictionar["sentiment_analysis"].append(
            sia.polarity_scores(full_text)["compound"]
        )
        dictionar["likes"].append(result["favorite_count"])
        dictionar["retweets"].append(result["retweet_count"])
        dictionar["city"].append(result["place"]["name"])
        result = re.search("(?P<url>https?://[^\s]+)", full_text)
        if result:
            dictionar["url"].append(result.group(1))
        else:
            dictionar["url"].append("")
    return dictionar


def exportToFile(country, df, tag):
    df.to_csv("datasets/information_" + country + "_" + tag + ".csv")
    df.to_excel("datasets/information_" + country + "_" + tag + ".xlsx", index=False)


if __name__ == "__main__":
    countries = ["Germany", "Norway", "Romania", "Switzerland"]
    for country in countries:
        tweets = getTweetsByCountry(country, 10)
        tweetsDictionary = processData(tweets)
        df = pd.DataFrame(tweetsDictionary)
        exportToFile(country, df, "simple")
