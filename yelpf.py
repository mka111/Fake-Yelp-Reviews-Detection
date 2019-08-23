import pandas as pd
import string
import json
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

#enter path to business json, enter number of businesses you want returnes,review required
#will return an array with (businessID, and average rating of that business)
def find_Business(bus_Path,bus_Num,max_review):
    bus_Ret=[]
    with open(bus_Path, encoding="utf8") as fp:  
        line = fp.readline()
        cnt = 1
        cnt2=0
        while line and cnt2<(bus_Num-1):
            line = fp.readline()
            datastore = json.loads(line)
            if(datastore["review_count"]>max_review):
                print(datastore["review_count"])
                bus_Ret.insert(cnt2,[(datastore["business_id"]),(datastore["stars"])])
                cnt2=cnt2+1
            cnt += 1
    return bus_Ret

#enter path, max number of reviews and the business youre working with
#will return array with of all the review as json/dic associated with bus
def review_list(rev_Path_Path,max_review,bus_struct):
    rev_Ret=[]
    with open(rev_Path_Path , encoding="utf8") as fp:  
        line = fp.readline()
        lis=[]
        #cnt = 1
        cnt2=0
        while line and cnt2<max_review:
            line = fp.readline()
            datastore = json.loads(line)
            if(datastore["business_id"]==bus_struct[0]):
                lis.append(datastore)
                #rev_Ret.insert(cnt2,[(datastore["text"]),(datastore["stars"]),(datastore["business_id"]),bus_struct[1]])
                cnt2=cnt2+1
            #cnt += 1
        print(lis)
    return lis

#works with a list of reviews of a particular business
#gives the reviews a dataframe shape, allows to look at columns/rows
#adds the length of the review to the dataframe as "text length"
def import_to_dataframe(reviews):
    df = pd.DataFrame.from_dict(reviews)
    df.shape
    #print(df.describe(), "\n")
    # a new column to store the character length of each review
    df['text length'] = df['text'].apply(len)
    df['pronouns']=0
    df['nouns']=0
    df['verbs']=0
    #print("df: ",df)
    #stars = df.groupby('stars').mean()
    return df

#short reviews are flagged
def short_reviews(rev_list, minLength):
    rev_short = []
    for review in rev_list:
        revText = review[0]
        revLength = len(revText.split())
        if revLength < minLength:
            rev_short.append(review)
    return rev_short

#a function that will split a review into its individual words, and return a list.
#It will also remove the stopwords(a, an, etc) by using NLTK library
#outputs an array of the words
def text_process(text):
    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]

def pr_lis(lis,count):
    i =0
    s = ""
    while i < count:
        s = s+"\ni:"+str(i)+" "+str(lis[i])+"\n"
        print(s)
        i = i+1
    return s

#convert list of tagged tokens to dataframe
def tokens2frame(tok):
    df = pd.DataFrame(tok)
    df.shape
    return df

#find the nouns, verbs and pronouns of each review, and count them
#store back in dataframe as percentages
def tag_sentences(frame, counter):
    i = 0
    while i < counter:
        s = frame['text'][i]
        tokens = " ".join("".join([" " if ch in string.punctuation else ch for ch in s]).split()).split()
        l = len(tokens)
        tagged = nltk.pos_tag(tokens)
        tagframe = tokens2frame(tagged)
        #print(tagframe)
        
        #get list of noun/adj, verb/adv, adj-super, and pronouns
        tag_pro = tagframe[tagframe[1] == 'PRP']
        tag_noun = tagframe[(tagframe[1] == 'NN') |
                            (tagframe[1] == 'NNS') |
                            (tagframe[1] == 'NNP') |
                            (tagframe[1] == 'NNPS')|
                            (tagframe[1] == 'JJ')  |
                            (tagframe[1] == 'JJR') |
                            (tagframe[1] == 'JJS')]
        tag_verb = tagframe[(tagframe[1] == 'RB') |
                            (tagframe[1] == 'RBR')|
                            (tagframe[1] == 'VB') |
                            (tagframe[1] == 'VBD')|
                            (tagframe[1] == 'VBG')|
                            (tagframe[1] == 'VBN')|
                            (tagframe[1] == 'VBZ')|
                            (tagframe[1] == 'VBP')]
        
        #get all the length of the lists and convert to percentage of words in total
        my = round(len(tag_pro)/l*100)
        nou = round(len(tag_noun)/l*100)
        ver = round(len(tag_verb)/l*100)
        
        frame['pronouns'][i] = my
        frame['nouns'][i] = nou
        frame['verbs'][i] = ver
        #add to dataframe 
        
        #print("n: ", nou,"\nver: ",ver,"\nlat: ",lat, "\nmy: ",my) 
        #print('\n')
        i = i+1
    return frame

def print_s(frame):
    rate = frame['stars']
    lis = frame['text']
    i = frame.index.values
    for j in i:
        print("i: ",rate[j],"\n", lis[j])
    return

def comparisons_n_v(frame,length):
    noun_mean = frame['nouns'].median()
    verbs_mean = frame['verbs'].median()
    difference = noun_mean-verbs_mean
    f = frame[frame['verbs']-frame['nouns']>=difference]
    return f

def comparisons_p(frame,length):
    pronoun_max = frame['pronouns'].max()
    pronoun_cutoff = round(pronoun_max*.8)
    #print(pronoun_cutoff)
    f = frame[frame['pronouns']>=pronoun_cutoff]
    return f

def get_lis(frame, col, star):
    lis = frame[col]
    rate = frame[star]
    i =0
    while i < len(frame):
        print("stars: ",rate[i],"\n",lis[i],"\n")
        i=i+1
    return lis
