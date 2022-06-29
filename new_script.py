from numpy import cumsum
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("./information_Germany_extended.csv")
# df = pd.read_csv("./information_montenegro2.csv")
df = pd.read_csv("./information_switzerland.csv")
# df = pd.read_csv("./information_norway2.csv")
# df = pd.read_csv("./information_North Macedonia_extended.csv")

print(df["sentiment_analysis"].mean())
df = df[df["likes"] != 0]
df = df[df["retweets"] != 0]
df = df.sort_values(["retweets", "likes"], ascending=False)
df = df.head(599)
print(df["sentiment_analysis"].mean())
print(df)
