from numpy import full
import tweepy
from googletrans import Translator
import pandas as pd
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer


translator = Translator()
print(translator.translate("안녕하세요.", dest="en").text)

apiKey = "jyVEAnlDY1lBPycr8HUNqaWxS"
apiKeySecret = "gScJ1A2l5mCkOrAF37BxLT9oqm7ij6hNNdZLGTaB9gyTvB9GVV"
bearerToken = "AAAAAAAAAAAAAAAAAAAAAKmTeAEAAAAAwAEd0y2qzGa7eBU4bKI%2FJp07yTo%3DkG8KHKQ083AOjeOKxA1MlrZs34usHDmp92Hs3iexv5LxRHJH5O"
accessToken = "1496904203784048640-lYP2vvV1LiBKxqAjNz24ppYKWmnDEG"
accessTokenSecret = "NpDlvtPfdr7pOzdI627fbs9BtBEFKL9jm3HEWCNw9RjQJ"

auth = tweepy.OAuthHandler(apiKey, apiKeySecret)
auth.set_access_token(accessToken, accessTokenSecret)

api = tweepy.API(auth, wait_on_rate_limit=True)
countries = ["Germany"]

for country in countries:
    places = api.search_geo(query=country, granularity="country")
    # print(places)
    place_id = places[0].id
    # tweets = api.search_tweets(q="place:%s" % place_id, count=3, result_type="popular")

    dictionar = {
        "text": [],
        "likes": [],
        "retweets": [],
        "city": [],
        "sentiment_analysis": [],
        "url": [],
    }

    results = [
        status._json
        for status in tweepy.Cursor(
            api.search_tweets,
            q="place:%s" % place_id,
            # result_type="popular",
            tweet_mode="extended",
        ).items(10000)
    ]
    info = []
    print("len results: ", len(results))

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

    # print(dictionar)
    df = pd.DataFrame(dictionar)
    print(df)
    df.to_csv("information_" + country + "_extended.csv")
    df.to_excel("information_" + country + "_extended.xlsx", index=False)
# for result in results:

#     tweet = {
#         "id": result["id"],
#         "tweet text": result["full_text"],
#         "follower count": result["user"]["followers_count"],
#         "likes count": result["user"]["favourites_count"],
#         "city": result["place"]["name"],
#     }
#     info.append(tweet)

# from collections import ChainMap

# d3 = ChainMap(*info)
# new_dict = dict(d3)
# print("new dict\n", new_dict)

# df = pd.DataFrame(
#     new_dict.items(),
#     columns=[new_dict["id"], new_dict["tweet text"]],
# )
# print("Dataframe\n", df)
# df.to_csv("information.csv", sep="\t")


# sia = SentimentIntensityAnalyzer()
# df["sentiment analysis"] = sia.polarity_scores(df["tweet text"])["compound"]
# print(df)


# print(tweets)
# for tweet in tweets:
#     print(translator.translate(tweet.text, dest="en").text + " | " + tweet.place.name)
#     # status = api.get_status(tweet.id_str, tweet_mode="extended")
#     # print(status.extended_tweet["full_text"])
#     print("!!!!!!!!")
#     print(tweet.entities["hashtags"])


# def get_trends(api, loc):
#     # Object that has location's latitude and longitude.
#     g = geocoder.osm(loc)

#     closest_loc = api.closest_trends(g.lat, g.lng)
#     trends = api.get_place_trends(closest_loc[0]["woeid"])
#     return trends[0]["trends"]


# def extract_hashtags(trends):
#     hashtags = [trend["name"] for trend in trends]
#     # if "#" in trend["name"]
#     return hashtags


# def get_n_tweets(api, hashtag, n, lang=None):
#     for status in tweepy.Cursor(api.search_tweets, q=hashtag, lang=lang).items(n):
#         print(f"https://twitter.com/i/web/status/{status.id}")


# if __name__ == "__main__":
#     loc = "UK"
#     trends = get_trends(api, loc)
#     hashtags = extract_hashtags(trends)
#     for hashtag in hashtags:
#         print(translator.translate(hashtag, dest="en").text)
#     hashtag = hashtags[0]
#     print("!!!!!!")
#     print(hashtag)
#     status = get_n_tweets(api, hashtag, 5, "ar")
