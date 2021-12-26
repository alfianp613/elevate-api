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
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
import datetime

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
    import json
    with open(f'data sentiment/sentiment {katakunci}.json', 'w') as f:
      json.dump(output, f)
    
    mix = " ".join(i for i in twt)
    stopwords = set(STOPWORDS)
    wordcloud2 = WordCloud(max_font_size=80, stopwords=stopwords).generate(mix)
    wordcloud2.to_file(f'wordcloud/wordcloud {katakunci}.png')
    return print(f'{katakunci} Selesai')
  
# koin = ['bitcoin','ethereum','binance coin','tether','solana',
#         'cardano','xrp','usd coin','polkadot','dogecoin']
# for i in koin:
#       sentimen(i)




