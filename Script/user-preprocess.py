import os.path as path
import pandas as pd
import numpy as np
import re
import itertools
import string
import csv
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
from nltk import wordpunct_tokenize
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet')

from collections import Counter, OrderedDict

from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

PATH = '../Profiles/elonmusk.csv'

df = pd.read_csv(PATH)




def common_sentences(text):
    sentences = (list(itertools.chain(text)))
    flat_list = [item for sublist in sentences for item in sublist]
    print(Counter(flat_list).most_common(10))
    text_bow = Counter(flat_list).most_common(20)
    return text_bow

def lowerCase(text):
    text = text.str.lower()
    return text


def decontract(text):
    contractions = {
        "ain't": "am not",
        "aren't": "are not",
        "can't": "cannot",
        "can't've": "cannot have",
        "'cause": "because",
        "could've": "could have",
        "couldn't": "could not",
        "couldn't've": "could not have",
        "didn't": "did not",
        "doesn't": "does not",
        "don't": "do not",
        "hadn't": "had not",
        "hadn't've": "had not have",
        "hasn't": "has not",
        "haven't": "have not",
        "he'd": "he would",
        "he'd've": "he would have",
        "he'll": "he will",
        "he's": "he is",
        "how'd": "how did",
        "how'll": "how will",
        "how's": "how is",
        "i'd": "i would",
        "i'll": "i will",
        "i'm": "i am",
        "i've": "i have",
        "isn't": "is not",
        "it'd": "it would",
        "it'll": "it will",
        "it's": "it is",
        "let's": "let us",
        "ma'am": "madam",
        "mayn't": "may not",
        "might've": "might have",
        "mightn't": "might not",
        "must've": "must have",
        "mustn't": "must not",
        "needn't": "need not",
        "oughtn't": "ought not",
        "shan't": "shall not",
        "sha'n't": "shall not",
        "she'd": "she would",
        "she'll": "she will",
        "she's": "she is",
        "should've": "should have",
        "shouldn't": "should not",
        "that'd": "that would",
        "that's": "that is",
        "there'd": "there had",
        "there's": "there is",
        "they'd": "they would",
        "they'll": "they will",
        "they're": "they are",
        "they've": "they have",
        "wasn't": "was not",
        "we'd": "we would",
        "we'll": "we will",
        "we're": "we are",
        "we've": "we have",
        "weren't": "were not",
        "what'll": "what will",
        "what're": "what are",
        "what's": "what is",
        "what've": "what have",
        "where'd": "where did",
        "where's": "where is",
        "who'll": "who will",
        "who's": "who is",
        "won't": "will not",
        "wouldn't": "would not",
        "you'd": "you would",
        "you'll": "you will",
        "you're": "you are"
    }

    # text = df[attr]
    clean_text = []
    for row in text:
        row = row.split()
        new_row = []
        for word in row:
            if word in contractions:
                new_row.append(contractions[word])
            else:
                new_row.append(word)
        row = " ".join(new_row)
        clean_text.append(row)
    text = clean_text
    return text


def remove_link(text):
    new_text = []
    for row in text:
        new_text.append(re.sub(r"http\S+", "", row))
    return new_text


def tokenize(text):
    tkn = TweetTokenizer()
    new_text = []
    for row in text:
        # tkn.tokenize(row)
        new_text.append(tkn.tokenize(row))
    # text = text.apply(lambda row: tkn.tokenize(row['text']), axis=1)
    return new_text


def remove_stopword(text):
    stop = stopwords.words('english')
    stop = set(stop)
    stop.add('’')
    stop.add('“')
    stop.add('...')
    stop.add('u')
    new_text = []
    for row in text:
        out = []
        for token in row:
            if token not in stop:
                out.append(token)
        new_text.append(out)
    # text = text.apply(lambda x: [item for item in x if item not in stop])
    return new_text


def remove_punct(text):
    punctuation = string.punctuation
    new_text = []
    for row in text:
        out = []
        for token in row:
            token = token.replace("'s", "")
            if token not in punctuation:
                out.append(token)
        new_text.append(out)
    # text = text.apply(lambda x: [item for item in x if item not in punctuation])
    return new_text


def remove_emoji(text):
    new_text = []
    for row in text:
        out = []
        for token in row:
            out.append(token.encode('ascii', 'ignore').decode('ascii'))
        new_text.append(out)
    return new_text


def remove_empty(text):
    new_text = []
    for row in text:
        out = []
        for token in row:
            if token != '':
                out.append(token)
        new_text.append(out)
    return new_text


def lemmatizer(text):
    new_text = []
    lemmatizer = WordNetLemmatizer()
    for row in text:
        out = []
        for token in row:
            out.append(lemmatizer.lemmatize(token))
        new_text.append(out)
    return new_text




'''
----------- START ------------
'''

# Removing hashtags and citations
# df['text'] = df['text'].apply(p.clean)

# We will work on the text column

text = df.text

# Converting to lower case
print('Converting to lower-case...')
text = lowerCase(text)

# Removing contractions from text
print('Removing contractions..')
text = decontract(text)

# Removing links
print('Removing links from text...')
text = remove_link(text)

# Tokenizer
print('Tokenizing sentences..')
text = tokenize(text)

print('Most frequent tokens:')
common_sentences(text)

# Stopwords removal
print('Removing stopwords..')
text = remove_stopword(text)

# Punctuation removal
print('Removing punctuations..')
text = remove_punct(text)

print('Most frequent tokens:')
common_sentences(text)

print('Removing emoji..')
text = remove_emoji(text)

print('Removing empty tokens..')
text = remove_empty(text)

print('Most frequent tokens:')
common_sentences(text)

# Lemmatization!
print('Applying Lemmatization..')
text = lemmatizer(text)

print('Most frequent tokens:')
text_bow = common_sentences(text)

#output bow
str = ' '.join(e[0] for e in text_bow)
bow = str.split()
print(bow)
