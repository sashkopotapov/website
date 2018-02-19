import json
import ssl
import urllib.error
import urllib.parse
import urllib.request
import folium
from geopy.geocoders import ArcGIS
from task2 import twurl

TWITTER_URL = 'https://api.twitter.com/1.1/users/show.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def latlon(film):
    geolocator = ArcGIS()
    loc = film
    coordinates = geolocator.geocode(loc, timeout=100)
    return [coordinates.latitude, coordinates.longitude]

def user_info(name):
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': name, 'count': '1'})
    print('Retrieving', url)
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    d = json.loads(data)
    headers = dict(connection.getheaders())
    # print('Remaining', headers['x-rate-limit-remaining'])

    for key in d:
        if d[key] == None:
            d[key] = 'unknown'
    name =  'name: ' + d['name'] + '\n'
    sn = 'nickname: ' + d['screen_name'] + '\n'
    locat = 'location: ' + d['location'] + '\n'
    desc = 'prof. description: ' + d['description'] + '\n'
    url = 'url: ' + d['url']+ '\n'
    foll = 'followers: ' + str(d['followers_count'])+ '\n'
    fr = 'friends: ' + str(d['friends_count'])+ '\n'
    dt = 'created at: ' + d['created_at']+ '\n'
    img = 'image: ' + d['profile_image_url']+ '\n'

    map = folium.Map(location=[48, 25], zoom_start=[3])
    loc = folium.FeatureGroup(name ="User location")
    loc.add_child(folium.Marker(location=latlon(d['location']),
                                popup=name + sn + locat + desc
                                + url + foll + fr + dt + img, icon=folium.Icon('cloud')))

    map.add_child(loc)
    map.save('templates//user.html')
