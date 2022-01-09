import tweepy
import pandas as pd
import re
import string
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from datetime import date
import datetime
import pyrebase

def sentimen(katakunci):
    consumerKey = "z3Xe9UNE6tT3hd4J3SbtlZJqJ"
    consumerSecret = "cf0mBeggVK4GaPENxCAleykJroTy1yUiT2NCO3OvsCo2uXvafn"
    accessToken = "2892616411-8HMfz4JoP7tI4W2u7eQxZ2caVmUitv67AjFQiiQ"
    accessTokenSecret = "UO6GeQwqSDrurmfU6p3BhGiMADaZxZ8dvcXV9vpkm0Zpf"
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    today = date.today()
    sekarang = today.strftime("%Y-%m-%d")


    q = katakunci
    q2 = q + " -filter:retweets"
    tweets = tweepy.Cursor(api.search_tweets,
                  q=q2,
                  lang="en",
                  result_type = "mixed",
                  until = sekarang,
                  count = 200,
                  tweet_mode = 'extended').items(1000)
    teks = []
    username = []
    # Iterate and print tweets
    for tweet in tweets:
        # print(tweet.full_text)
        # print(tweet.user.screen_name)
        teks.append(tweet.full_text)
        username.append(tweet.user.screen_name)

    def deEmojify(text):
        regrex_pattern = re.compile(pattern = "["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags = re.UNICODE)
        return regrex_pattern.sub(r'',text)

    def text_processing(sentences):
      kalimat = sentences
      if type(kalimat) == str:
        kalimat = kalimat.lower()
        kalimat_nonum = re.sub(r"\d+", "", kalimat)
        kalimat_nomention = re.sub(r'(@[A-Za-z0-9_]+)', '', kalimat_nonum)
        kalimat_nohashtag = re.sub(r'(#[A-Za-z0-9_]+)','', kalimat_nomention)
        kalimat_nolink = re.sub('http://\S+|https://\S+', '', kalimat_nohashtag)
        kalimat_nopunct = kalimat_nolink.translate(str.maketrans("","",string.punctuation))
        kalimat_nospace = kalimat_nopunct.strip()
        kalimat_noemot = deEmojify(kalimat_nospace)
        tokens = nltk.tokenize.word_tokenize(kalimat_noemot)

        lem = WordNetLemmatizer()
        output = []
        [item.lower() for item in tokens]
        for i in tokens:
          output.append(lem.lemmatize(i))
        return " ".join(output)
      else:
        return str(kalimat)

    twt = pd.Series(teks).apply(text_processing)

    pos = 0
    neg = 0
    net = 0

    from textblob import TextBlob
    for i in range(len(teks)):
      if TextBlob(twt[i]).sentiment.polarity > 0:
        pos += 1
      elif TextBlob(twt[i]).sentiment.polarity < 0:
        neg += 1
      else :
        net +=1
    now = datetime.datetime.now()
    tanggal = f'{now.day}/{now.month}/{now.year}'
    time = f'{now.hour}:{now.strftime("%M")}'
    output = {'sentiment':['Positif','Negatif','Netral'],
        'total':[pos, neg, net],'tanggal':tanggal,'jam':time}
    
    mix = " ".join(i for i in twt)
    stopwords = set(STOPWORDS)
    font_path = 'MADE TOMMY Medium_PERSONAL USE.otf'
    wordcloud2 = WordCloud(max_font_size=80, stopwords=stopwords, background_color='white', max_words=2000, font_path=font_path).generate(mix)
    wordcloud2.to_file(f'wordcloud/wordcloud {katakunci}.png')
    
    # save in firebase
    config = {'apiKey': "AIzaSyBF9zZqQBt2h0RJZN3Xubugse5Ba3qJLdw",
          'authDomain': "elevate-66775.firebaseapp.com",
          'projectId': "elevate-66775",
          'databaseURL': "https://elevate-66775-default-rtdb.asia-southeast1.firebasedatabase.app/",
          'storageBucket': "elevate-66775.appspot.com",
          'messagingSenderId': "1008765930388",
          'appId': "1:1008765930388:web:5ad1f3c8464d8f8d859d81",
          'measurementId': "G-0Q4Y5MFCVD"}
    firebase = pyrebase.initialize_app(config)
    # Get a reference to the auth service
    auth = firebase.auth()

    email = 'alfianp613@gmail.com'
    password = 'DummyDummy631'
    # Log the user in
    user = auth.sign_in_with_email_and_password(email, password)
    database = firebase.database()
    a = database.child("Sentiment").child(katakunci).set(output,user['idToken'])
    
    storage = firebase.storage()
    path_on_cloud = f"wordcloud/wordcloud {katakunci}.png"
    path_local = f'wordcloud/wordcloud {katakunci}.png'
    
    storage.child(path_on_cloud).put(path_local, user['idToken'])
    
    return print(f'sentiment {katakunci} Selesai')


sentimen('bitcoin')
