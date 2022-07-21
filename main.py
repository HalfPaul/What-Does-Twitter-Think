from typing import Union
import os
from fastapi import FastAPI

import twint
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline


def tweet_sentiment(keyword, amount=100):
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


@app.get("/{query}")
def read_root(query: str):
    pos, neg = tweet_sentiment(query)
    if neg == 0:
        return {"sentiment": "Positive", "color": "green"}
    if pos == 0:
        return {"sentiment": "Negative", "color": "red"}
    score = pos * 100 / neg
    if score == 100:
        return {"sentiment": "Neutral", "color": "grey"}
    elif score < 100 and score > 0:
        return {"sentiment": "Mostly Negative", "color": "red"}
    else:
        return {"sentiment": "Mostly Positive", "color": "red"}
