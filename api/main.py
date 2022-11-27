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

    for result in results:
        if result["label"] == "POSITIVE":
            positive += 1
        else:
            negative += 1

    return positive, negative


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
    pos, neg = tweet_sentiment(query)
    if neg == pos:
        return {"sentiment": "Neutral", "percent":50}
    if neg > pos:
        return {"sentiment": "Negative", "percent":neg*2}
    else:
        return {"sentiment": "Positive", "percent":pos*2}