import requests
from datetime import (date, timedelta)
from flask import (
    Blueprint, g, redirect, render_template, session, url_for
)


bp = Blueprint('charts', __name__, url_prefix = '/charts')

@bp.route('/hot10')
def hot10():
    chartDate = date.today() - timedelta(days = 1)
    url = "https://billboard-api2.p.rapidapi.com/hot-100"
    querystring = {"range":"1-10","date":str(chartDate)}

    headers = {
        "X-RapidAPI-Host": "billboard-api2.p.rapidapi.com",
        "X-RapidAPI-Key": "e2a5add9f5msh458ae5409b8239cp1bfecdjsnde7abb95e17c"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    #data= {'info': {'category': 'Billboard', 'chart': 'HOT 100', 'date': '2022-06-11', 'source': 'Billboard-API'}, 'content': {'1': {'rank': '1', 'title': 'As It Was', 'artist': 'Harry Styles', 'weeks at no.1': '2', 'last week': '1', 'peak position': '1', 'weeks on chart': '9', 'detail': 'same'}, '2': {'rank': '2', 'title': 'First Class', 'artist': 'Jack Harlow', 'last week': '2', 'peak position': '1', 'weeks on chart': '8', 'detail': 'same'}, '3': {'rank': '3', 'title': 'Wait For U', 'artist': 'Future Featuring Drake & Tems', 'last week': '3', 'peak position': '1', 'weeks on chart': '5', 'detail': 'same'}, '4': {'rank': '4', 'title': 'About Damn Time', 'artist': 'Lizzo', 'last week': '5', 'peak position': '4', 'weeks on chart': '7', 'detail': 'up'}, '5': {'rank': '5', 'title': 'Heat Waves', 'artist': 'Glass Animals', 'last week': '6', 'peak position': '1', 'weeks on chart': '72', 'detail': 'up'}, '6': {'rank': '6', 'title': 'Big Energy', 'artist': 'Latto', 'last week': '7', 'peak position': '3', 'weeks on chart': '32', 'detail': 'up'}, '7': {'rank': '7', 'title': 'Me Porto Bonito', 'artist': 'Bad Bunny & Chencho Corleone', 'last week': '10', 'peak position': '7', 'weeks on chart': '4', 'detail': 'up'}, '8': {'rank': '8', 'title': 'Running Up That Hill (A Deal With God)', 'artist': 'Kate Bush', 'last week': 'None', 'peak position': '8', 'weeks on chart': '21', 'detail': 're-entry'}, '9': {'rank': '9', 'title': 'Late Night Talking', 'artist': 'Harry Styles', 'last week': '4', 'peak position': '4', 'weeks on chart': '2', 'detail': 'down'}, '10': {'rank': '10', 'title': 'Stay', 'artist': 'The Kid LAROI & Justin Bieber', 'last week': '12', 'peak position': '1', 'weeks on chart': '47', 'detail': 'up'}}}
    useable = {}
    j = 1
    for key, value in data.items():
        if(key == 'content'):
            for key1, value1 in value.items():
                rank = value1['rank']
                title = value1['title']
                artist = value1['artist']
                useable[str(j)] = {'rank': rank, 'title' : title, 'artist' : artist}
                j = j+1
    return render_template('charts/hot10.html', chart = useable)

@bp.route('/album10')
def album10():
    chartDate = date.today() - timedelta(days = 1)
    url = "https://billboard-api2.p.rapidapi.com/billboard-200"
    querystring = {"date":str(chartDate),"range":"1-10"}

    headers = {
        "X-RapidAPI-Key": "e2a5add9f5msh458ae5409b8239cp1bfecdjsnde7abb95e17c",
	    "X-RapidAPI-Host": "billboard-api2.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    useable = {}
    j = 1
    for key, value in data.items():
        if(key == 'content'):
            for key1, value1 in value.items():
                rank = value1['rank']
                album = value1['album']
                artist = value1['artist']
                useable[str(j)] = {'rank': rank, 'album' : album, 'artist' : artist}
                j = j+1
    return render_template('charts/album10.html', chart = useable)

@bp.route('/artist10')
def artist10():
    chartDate = date.today() - timedelta(days = 1)

    url = "https://billboard-api2.p.rapidapi.com/artist-100"
    querystring = {"range":"1-10", "date":str(chartDate)}
    headers = {
        "X-RapidAPI-Key": "e2a5add9f5msh458ae5409b8239cp1bfecdjsnde7abb95e17c",
	    "X-RapidAPI-Host": "billboard-api2.p.rapidapi.com"  
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    useable = {}
    j = 1
    for key, value in data.items():
        if(key == 'content'):
            for key1, value1 in value.items():
                rank = value1['rank']
                artist = value1['artist']
                useable[str(j)] = {'rank': rank, 'artist' : artist}
                j = j+1
    return render_template('charts/artist10.html', chart = useable)