from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import twint
from transformers import pipeline





def tweet_sentiment(keyword, amount=50):
    sentiment_pipeline = pipeline("sentiment-analysis")

    c = twint.Config()

    c.Search = [keyword]
    c.Limit = amount
    c.Lang = "en"
    c.Pandas = True
    c.Store_csv = False

    twint.run.Search(c)
    df = twint.storage.panda.Tweets_df

    negative = 0
    positive = 0


    results = sentiment_pipeline(list(df["tweet"]))
    
    print(len(results))

    best_rated_index = 0
    best_rated = 0
    worst_rated_index = 0
    worst_rated = 0

    for i, result in enumerate(results):
        if result["label"] == "POSITIVE":
            if (result["score"] > best_rated):
                best_rated_index = i
            positive += 1
        else:
            if (result["score"] > worst_rated):
                worst_rated_index = i
            negative += 1
    print(list(df["tweet"])[worst_rated_index])
    print(list(df["name"])[worst_rated_index])
    print(list(df["username"])[worst_rated_index])

    return positive/len(results)*100, negative/len(results)*100, list(df["tweet"])[best_rated_index], list(df["name"])[best_rated_index], list(df["username"])[best_rated_index], list(df["tweet"])[worst_rated_index], list(df["name"])[worst_rated_index], list(df["username"])[worst_rated_index],


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/{query}")
def read_root(query: str):
    print(query)
    pos, neg, best_tweet, best_name, best_username, worst_tweet, worst_name, worst_username = tweet_sentiment(query)
    if neg == pos:
        return {"sentiment": "Neutral", "percent":50}
    if neg > pos:
        return {"sentiment": "Negative", "percent":neg}
    else:
        return {"sentiment": "Positive", "percent":pos}