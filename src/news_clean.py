
import re
import numpy as np
import pandas as pd



def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)        
    return input_txt
def remove_emojis(input_txt):
    emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                u"\U00002702-\U000027B0"
                u"\U000024C2-\U0001F251"
                u"\U0001f926-\U0001f937"
                u'\U00010000-\U0010ffff'
                u"\u200d"
                u"\u2640-\u2642"
                u"\u2600-\u2B55"
                u"\u23cf"
                u"\u23e9"
                u"\u231a"
                u"\u3030"
                u"\ufe0f"
    "]+")
    input_txt=emoji_pattern.sub(r'',input_txt)
    return input_txt

def cleanData(inputString):
    inputString = inputString.encode('ascii', 'ignore').decode('ascii') # for emoji
    inputString = re.sub(r'http\S+', '', inputString) # for urls
    inputString = re.sub('[^A-Za-z0-9\.\,\'"]+', ' ', inputString) # for special characters
    return inputString

def clean_tweets(lst):
  
    # remove twitter handles (@xxx)
    lst = np.vectorize(cleanData)(lst)
    lst = np.vectorize(cleanData)(lst)
    # remove URL links (httpxxx)
    lst = np.vectorize(cleanData)(lst)
    # remove special characters, numbers, punctuations (except for #)
    lst = np.core.defchararray.replace(lst, "[^a-zA-Z#]", " ")
    lst=np.vectorize(cleanData)(lst)
    return lst
df=pd.read_csv('news.csv')
df['title']=clean_tweets(df['title'])
df['description']=df['description'].astype(str)
df['description']=clean_tweets(df['description'])
df['content']=df['content'].astype(str)
df['content']=clean_tweets(df['content'])

df.to_csv("news_cleaned.csv",index=None,header=True)
df.to_csv("news_cleaned.txt",index=None,header=True)
