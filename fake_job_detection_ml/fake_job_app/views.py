from django.shortcuts import render

import pickle
import pandas as pd

from Crypto.Cipher import AES
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from scipy.sparse import csr_matrix

from wordcloud import WordCloud
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English
from bs4 import BeautifulSoup
import re
# Create your views here.

stop_words = spacy.lang.en.stop_words.STOP_WORDS

#function to lemmatize the text
load_model = spacy.load('en_core_web_sm',disable = ['parser','ner'])
def lemmatize(text):
    doc = load_model(text)
    tex= " ".join([token.lemma_ for token in doc])
    return tex         


#function to clean the whole text
def clean_text(text):
    #Converting to lowercase
    text = text.lower()
    #Removing emails
    text = re.sub(r'([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', '', text)
    #Removing URLs
    text = re.sub(r'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', '', text)
    #Removing HTML tags
    text = BeautifulSoup(text, 'lxml').get_text()
    #Removing punctuations and numbers
    text = re.sub('[^A-Z a-z ]+', ' ', text)
    #Removing Multiple spaces
    text =  " ".join(text.split())
    #Removing Stop words
    text =  " ".join([t for t in text.split() if t not in stop_words])
    #lemmatizing the text
    text = lemmatize(text)
    return text    

def encrypt_message(message, key):
    message = message.encode()
    padding = 16 - (len(message) % 16)
    message += bytes([padding] * padding)
    key = key[:16].encode()
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(message)
    return ciphertext

def decrypt_message(ciphertext, key):
    key = key[:16].encode()
    cipher = AES.new(key, AES.MODE_ECB)
    message = cipher.decrypt(ciphertext)
    padding = message[-1]
    message = message[:-padding]
    message = message.decode()
    return message

key = "machinelearning multinomialnb"


def Home(request):
    return render(request,'fake_job_app/index.html')

def getPredictions(input):
    model = pickle.load(open("C:/Users/Uthra/fake_job_detection_ml/fake_job_app/multinomialNB_SO1.sav", "rb"))
    vectorizer = pickle.load(open("C:/Users/Uthra/fake_job_detection_ml/fake_job_app/vectorizer1.sav", "rb"))
    for i in input:
        mat = vectorizer.transform([str(i)])
        vec_df = pd.DataFrame.sparse.from_spmatrix(mat)
        X_cols = list(vec_df.columns)
        for col in X_cols:
            vec_df[col] = [encrypt_message(str(x), key) for x in vec_df[col]]
            vec_df[col] = [int.from_bytes(x, byteorder='big') for x in vec_df[col]]
            vec_df[col] = pd.to_numeric(vec_df[col], errors='coerce').astype(float)
        Mat = csr_matrix(vec_df.values)
        prediction = model.predict(Mat)
    if prediction == 0:
        return "Not Fraudulent"
    elif prediction == 1:
        return "Fraudulent"
    else:
        return "error"
    
def Result(request):
    title = str(request.GET.get('title'))
    loc = str(request.GET.get('loc'))
    dept = str(request.GET.get('dept'))
    comp_pro = str(request.GET.get('comp_pro'))
    desc = str(request.GET.get('desc'))
    req = str(request.GET.get('req'))
    bene = str(request.GET.get('bene'))
    em_type = str(request.GET.get('em_type'))
    re_exp = str(request.GET.get('re_exp'))
    re_edu = str(request.GET.get('re_edu'))
    ind = str(request.GET.get('ind'))
    fun = str(request.GET.get('fun'))

    input = title + loc + dept + comp_pro + desc + req + bene + em_type + re_exp + re_edu + ind + fun

    input = clean_text(input)

    input =[[input]]

    result = getPredictions(input)

    return render(request, 'fake_job_app/results.html', {'result':result})