import itertools
import re
import string
from collections import Counter
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer

import nltk
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')

def create_bow(text):
    sentences = (list(itertools.chain(text)))
    flat_list = [item for sublist in sentences for item in sublist]
    print(Counter(flat_list).most_common(15))
    text_bow = Counter(flat_list).most_common(15)
    return text_bow

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


def link_removal(text):
    nl_text = []
    for row in text:
        nl_text.append(re.sub(r"http\S+", "", row))
    return nl_text


def tokenize_text(text):
    tkn = TweetTokenizer()
    tkn_text = []
    for row in text:
        tkn_text.append(tkn.tokenize(row))
    return tkn_text


def stopword_removal(text):
    stop = stopwords.words('english')
    stop = set(stop)
    stop.add('’')
    stop.add('“')
    stop.add('...')
    stop.add('think')
    stop.add('ever')
    stop.add("anyone")
    stop.add('could')
    stop.add('need')
    stop.add('look')
    stop.add('may')
    stop.add('said')
    stop.add('come')
    stop.add('live')
    stop.add('here')
    stop.add('piece')
    stop.add('many')
    stop.add('sunday')
    stop.add('watching')
    stop.add('much')
    stop.add('11pm')
    stop.add('end')
    stop.add('please')
    stop.add('helping')
    stop.add('real')
    stop.add("going")
    stop.add("thing")
    stop.add("know")
    stop.add('rt')
    stop.add("1")
    stop.add("2")
    stop.add("3")
    stop.add("4")
    stop.add("5")
    stop.add("6")
    stop.add("7")
    stop.add("8")
    stop.add("9")
    stop.add("0")
    stop.add("10")
    stop.add("11")
    stop.add("like")
    stop.add("large")
    stop.add("laughing")
    stop.add("funny")
    stop.add("way")
    stop.add("full")
    stop.add("crew")
    stop.add("call")
    stop.add("one")
    stop.add("life")
    stop.add("join")
    stop.add("back")
    stop.add("news")
    stop.add("win")
    stop.add("fan")
    stop.add("done")
    stop.add("morning")
    stop.add("next")
    stop.add("male")
    stop.add("water")
    stop.add("love")
    stop.add("damn")
    stop.add("amazing")
    stop.add("make")
    stop.add("tonight")
    stop.add("man")
    stop.add("irresponsible")
    stop.add("best")
    stop.add('show')
    stop.add("gooooooooo")
    stop.add("evening")
    stop.add("night")
    stop.add("today")
    stop.add("day")
    stop.add("everyone")
    stop.add("great")
    stop.add("let")
    stop.add("get")
    stop.add("see")
    stop.add("thank")
    stop.add("thanks")
    stop.add("new")
    stop.add("go")
    stop.add(":-)")
    stop.add("first")
    stop.add("great")
    stop.add("would")
    stop.add("de")
    stop.add("la")
    stop.add("le")
    stop.add("read")
    stop.add("que")
    stop.add("say")
    stop.add("good")
    stop.add("via")
    stop.add("want")
    stop.add("last")
    stop.add("huge")
    stop.add("week")
    stop.add("w")
    stop.add('work')
    stop.add('got')
    stop.add('really')
    stop.add('even')
    stop.add('bit')
    #che non si riescono a togliere
    stop.add('guy')
    stop.add('u')
    stop.add('year')
    stop.add('time')
    stop.add('here')
    
    sr_text = []
    for row in text:
        out_text = []
        for token in row:
            if token not in stop:
                out_text.append(token)
        sr_text.append(out_text)
    return sr_text


def punctuation_removal(text):
    punctuation = string.punctuation
    pr_text = []
    for row in text:
        out_text = []
        for token in row:
            token = token.replace("'s", "")
            if token not in punctuation:
                out_text.append(token)
        pr_text.append(out_text)
    return pr_text


def emoji_removal(text):
    er_text = []
    for row in text:
        out_text = []
        for token in row:
            out_text.append(token.encode('ascii', 'ignore').decode('ascii'))
        er_text.append(out_text)
    return er_text


def empty_removal(text):
    er_text = []
    for row in text:
        out_text = []
        for token in row:
            if token != '':
                out_text.append(token)
        er_text.append(out_text)
    return er_text


def lemmatizer_text(text):
    lemm_text = []
    lemmatizer = WordNetLemmatizer()
    for row in text:
        out_text = []
        for token in row:
            out_text.append(lemmatizer.lemmatize(token))
        lemm_text.append(out_text)
    return lemm_text


def preProcess(df):
    text = df.text

    print('lower-case phase')
    text = text.str.lower()

    print('contractions phase')
    text = decontract(text)

    print('Removing links from text...')
    text = link_removal(text)

    print('Tokenizing phase')
    text = tokenize_text(text)

    print('stopwords phase')
    text = stopword_removal(text)

    print('punctuations phase')
    text = punctuation_removal(text)

    print('emoji phase')
    text = emoji_removal(text)

    print('Removing empty tokens created in preprocess')
    text = empty_removal(text)

    print('Lemmatization phase')
    text = lemmatizer_text(text)

    print('Bag of Words:')
    text_bow = create_bow(text)

    # output bow
    str = ' '.join(e[0] for e in text_bow)
    bow = str.split()
    print(bow)
    return bow

def ProfilesBow():
    users = ['PaulNicklen','KevinHart4real','ProfBrianCox','elonmusk',
             'Snowden','jeffjarvis','iamjohnoliver','JimCameron','JeremyClarkson','JimWhite']    
    tutto = pd.DataFrame(columns=['bow'])
    for user in users:
        print(user)
        PATH = '../Profiles/'+user+'.csv'
        df = pd.read_csv(PATH)
        bow = preProcess(df)
        df_new = pd.DataFrame(data=bow, columns=['bow'])
        df_new['user'] = user
        tutto = tutto.append(df_new)
    tutto.to_csv(r'../Tweets-csv/users-bows.csv', index=None, header=True)

def getUserBow(users_bow, u):
    return(users_bow[users_bow['user'] == u]['bow'].tolist())

def getUsersNotCurrent(users_bow, u):
    return(users_bow[users_bow['user']!= u]['user'].unique().tolist())

def getUsers(users_bow):
    return(users_bow['user'].unique().tolist())

def getUsersBows():
    bow = pd.read_csv('../Tweets-csv/users-bows.csv')
    return(bow)

