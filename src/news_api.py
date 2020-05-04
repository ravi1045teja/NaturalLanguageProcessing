import requests

import csv

# The headers remain the same for all the requests
headers = {'Authorization': 'bc9437f6137c45b8979887ac8800ec54'}

everything_news_url = 'https://newsapi.org/v2/everything'

#KeyWords to extract data
keywords =  ['Canada', 'University', 'Dalhousie University', 'Halifax', 'Canada Education']
with open('news.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['author', 'title', 'description','content','date'])
for word in keywords:
    params_to={
        'q':word,
        'language':'en',
        'pageSize':100
        
        }
    response = requests.get(url=everything_news_url, headers=headers, params=params_to)
    response_json=response.json()
    for i in response_json['articles']:
        with open('news.csv','a') as f:
            writer=csv.writer(f)
            writer.writerow([i['author'],i['title'],i['description'],i['content'],i['publishedAt']])


    

    
