#api keys and secrets
consumer_key = 'tS4y2r9250ZHi5DX9PDuhHBJr'
consumer_secret = 'xaMlnJRpHzEhw1ULQJ8xjJVpryPtMiIlvoEClaYEAYh9mMwW0E'
access_token = '1084656297822187521-tuC2n5aOIPPow8fLitFjCwy36Q3PEd'
access_token_secret = 'miY0K6Kqmp9zvji5bRdczhyblrE4QElPDp3j9d5DXrLw4'
#modules 
import tweepy 
import json
import matplotlib.pyplot as plt
#functions
def extractTime(created_at):
    clocktime= created_at.split(" ")
    day = int(clocktime[2])
    hour= clocktime[3].split(":")
    return (day * 24 + int(hour[0]))
def processTweets(A,firstHour,D):
    for i in A:
        time= extractTime(i._json["created_at"])
        D[24-firstHour+time]=D[24-firstHour+time]+1
#main program        
dict={}
for hour in range(0,25):
    dict[hour]=0
    
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
userSearch=input("Search for a term:")
search_results = api.search(q=userSearch, count=100)
firstHour=extractTime(search_results[0]._json["created_at"])
processTweets(search_results,firstHour,dict)

print("loading...")

lastHour=extractTime(search_results[-1]._json["created_at"])
lastId=search_results[-1]._json["id"]
print (lastId, firstHour, search_results[0]._json["created_at"])

while (firstHour - lastHour) < 24:
    search_results=api.search(q=userSearch, count=100, max_id=str(lastId - 1))
    processTweets(search_results,firstHour,dict)
    lastHour=extractTime(search_results[-1]._json["created_at"])
    lastId=search_results[-1]._json["id"]
    print (lastId, lastHour, search_results[-1]._json["created_at"])

print("done")

#graphic
x=dict.keys()
labels=[]
for h in x:
    T=firstHour-24+h
    realTime=str(T%24)
    labels.append(realTime)
y=dict.values()
plt.xlabel("Time(Hours(GMT))")
plt.ylabel("Twitter Mentions of"+userSearch)
plt.title("Twitter Mentions per Hour in the last 24 hours of"+ userSearch)

plt.bar(labels,y,label="Times 1", color="b")
plt.show()

