import sys
from pyspark import SparkContext, SparkConf 
import re,string
#Setting the spark context to run on master
conf = SparkConf().setAppName('Word_Frequency_Count').setMaster('spark://****')
sc = SparkContext(conf=conf)
tweet_file=sc.textFile("tweet_cleaned.txt")
#Converting the tet file to lower and removing punctuations
def uni_to_clean_str(x):
                converted = x.encode('utf-8')
                lowercased_str = converted.lower()
              
                lowercased_str = lowercased_str.replace('--',' ')
                clean_str = lowercased_str.translate(None, string.punctuation) #Change 1
                return clean_str
#Text file is split into single words and map reduce performed to get the count          
single_word=tweet_file.flatMap(lambda x: uni_to_clean_str(x).split())
single_word=single_word.map(lambda x: (x,1))
single_word=single_word.reduceByKey(lambda x,y :x+y)
#RDD is converted to Dictionary
single_dict=single_word.collectAsMap()

def word_pairs(line):
            words = line.split()
            return [a + " " + b for a,b in zip(words, words[1:])]
#For bi-grams count , words is split by spaces and joined and performed map reduce to get the count         
two_pair=tweet_file.flatMap(word_pairs)
two_pair=two_pair.map(lambda x :(x,1)).reduceByKey(lambda a, b:a+b)
two_dict=two_pair.collectAsMap()


new_file=sc.textFile("news_cleaned.txt")
news_single_word=new_file.flatMap(lambda x: uni_to_clean_str(x).split())
news_single_word=news_single_word.map(lambda x:(x,1))
news_single_word=news_single_word.reduceByKey(lambda x,y :x+y)
news_single_dict=news_single_word.collectAsMap()

news_pair_word=new_file.flatMap(word_pairs)
news_pair_word=news_pair_word.map(lambda x:(x,1)).reduceByKey(lambda a,b:a+b)
news_pair_dict=news_pair_word.collectAsMap()

list=['education','canada','university','dalhousie','expensive','good school','good schools','bad school' ,'bad schools' ,'poor school' , 'poor schools','faculty','computer science','graduate']

 
for i in list:
            if single_dict.get(i) is None:
                    single_dict.update({i : 0})
            if news_single_dict.get(i) is None:
                    news_single_dict.update({i: 0})
            if two_dict.get(i) is None:
                    two_dict.update({i : 0})
            if news_pair_dict.get(i) is None:
                    news_pair_dict.update({i:0})
          
#Writing the output word count to text file
val=('word count from tweets and article ' \
          +'\neducation: ' + str(single_dict.get('education')+news_single_dict.get('education')) \
          +'\nCanada: ' + str(single_dict.get('canada')+news_single_dict.get('canada')) \
          +"\nuniversity: " + str(single_dict.get('university')+news_single_dict.get('university')) \
          +"\ndalhousie: " + str(single_dict.get('dalhousie')+news_single_dict.get('dalhousie')) \
          +"\nexpensive: " + str(single_dict.get('expensive')+news_single_dict.get('expensive')) \
           +"\ngood school or good schools : " + str(two_dict.get('good school')+news_pair_dict.get('good school')+two_dict.get('good schools')+news_pair_dict.get('good schools')) \
          
           +"\nbad school or bad schools or poor school or poor schools: " + str(two_dict.get('bad school')+news_pair_dict.get('bad school')+two_dict.get('bad schools')+news_pair_dict.get('bad schools')+two_dict.get('poor school')+news_pair_dict.get('poor school')+two_dict.get('poor schools')+news_pair_dict.get('poor schools')) \
          
          +"\nfaculty: " + str(single_dict.get('faculty')+news_single_dict.get('faculty')) \
          +"\ncomputer science: " + str(two_dict.get('computer science')+news_pair_dict.get('computer science')) \
          +"\ngraduate: " + str(single_dict.get('graduate')+news_single_dict.get('graduate')))
print(val)

with open('Output.txt', 'w+') as file: 
            file.write(val)
          

 

