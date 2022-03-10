from sqlite3 import Date
import urllib.request
import re
from bs4 import BeautifulSoup
import requests
import json
import urllib
import pprint
from flask import Flask, render_template
from pytube import YouTube
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def getHourMinAndSec(seconds):
    h = seconds // 3600
    m = seconds % 3600 // 60
    s = seconds % 3600 % 60
    return '{:02d}:{:02d}:{:02d}'.format(h, m, s)

def videoMetaData(getVideoUrl):
    response = requests.request("GET", getVideoUrl)
    soup = BeautifulSoup(response.text, "html.parser")
    body = soup.find_all("body")[0]
    scripts = body.find_all("script")
    result = json.loads(scripts[0].string[30:-1])
    getTitle=result['videoDetails']['title']
    ## Also this part can be used to access metadata
    # response = requests.request("GET", "https://www.youtube.com/watch?v=" + video_ids[i])
    # params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % video_ids[i]}
    # url = "https://www.youtube.com/oembed"
    # query_string = urllib.parse.urlencode(params)
    # url = url + "?" + query_string
    # with urllib.request.urlopen(url) as response:
    #     response_text = response.read()
    #     data = json.loads(response_text.decode())
    #     pprint.pprint(data)
    #     videoTitle = (data['title'])


def findVideo(getKeyword,maxResults=5):
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + getKeyword)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        liste = {"youtubeVideoUrlList":[],"message":[]}
        if maxResults<=len(video_ids):
            for i in range(0,maxResults):
                yt = YouTube("https://www.youtube.com/watch?v=" + video_ids[i])
                videoTitle = yt.title
                videoViews=yt.views
                print(videoTitle)
                videoUrlData = {'id':i,'videoUrl':"https://www.youtube.com/watch?v=" + video_ids[i],
                                'imgUrl':"https://img.youtube.com/vi/"+video_ids[i]+"/default.jpg",'title':videoTitle,'views':videoViews}
                liste["youtubeVideoUrlList"].append(videoUrlData)
                message = {'verisiGelenVideoSayisi':maxResults,'message':"success",'description':'Veri Başarıyla Getirildi'}
            liste["message"].append(message)
        else:
            message = {'message':"error",'description':'maxResults değişkeninin değeri video_ids dizisinin eleman sayısının değerini geçmiş olabilir'}
            liste["message"].append(message)
        return liste

@app.route("/<string:getKeyword>",methods =['GET'])
@cross_origin()
def defaultSearch(getKeyword):
        if(getKeyword!=""):
            return findVideo(getKeyword)
        else:
            return "Not Working"

@app.route("/<string:getKeyword>/<int:maxResults>",methods =['GET'])
@cross_origin()
def search(getKeyword,maxResults):
        if(getKeyword!="" and maxResults!=0):
            return findVideo(getKeyword,maxResults)
        else:
            return "Not Working"

@app.route("/",methods =['GET'])
@cross_origin()
def home():
    return render_template("/index.html")

if __name__ == "__main__":
    app.run(debug=True,port=7501)


