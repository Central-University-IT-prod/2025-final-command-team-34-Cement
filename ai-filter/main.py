from nltk.corpus import stopwords
import re
from catboost import *
import pandas as pd
import pickle
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import uvicorn


def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r"[^а-яА-Я\s]", "", text)
    tokens = text.split()
    try:
        stop_words = set(stopwords.words("russian"))
        tokens = [token for token in tokens if token not in stop_words]
    except:
        pass

    return " ".join(tokens)

cat = pickle.load(open("cat2.pkl", "rb"))

app = FastAPI()

class TextsInput(BaseModel):
    texts: list[str]
    
class ListTextsInput(BaseModel):
    texts: list[list[str]]

@app.post("/predict/single")
def predict_single(input: TextsInput):
    texts = input.texts
    preprocessed_text1 = preprocess_text(texts[0])
    preprocessed_text2 = preprocess_text(texts[1])
    prediction = cat.predict([preprocessed_text1, preprocessed_text2])
    return prediction

@app.post("/predict/multiple")
def predict_multiple(input: ListTextsInput):
    inputs = input.texts
    predictions = cat.predict(inputs)
    predictions = predictions.tolist()
    
    return predictions

if __name__ == '__main__':
    uvicorn.run(app=app, port=7632, host="0.0.0.0")