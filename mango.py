import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('mongodb+srv://port99:BBRnaAd7f3Hadhrq@cluster0.5l5eay2.mongodb.net/?retryWrites=true&w=majority')
db = client.milmmelier

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('http://www.mangoplate.com/search/%EB%B0%80%ED%81%AC%ED%8B%B0', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')
cafes = soup.select('body > main > article > div.column-wrapper > div > div > section > div.search-list-restaurants-inner-wrap > ul > li')
for cafe in cafes:
    a = cafe.select_one('figure > figcaption > div > a > h2')
    if a is not None:
        title = " ".join(a.text.split())
        star = cafe.select_one('div:nth-child(1) > figure > figcaption > div > strong').text
        address = cafe.select_one('div:nth-child(1) > figure > a > div > img')['alt'].split("-",maxsplit=1)[1]

        headers = {import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('mongodb+srv://jong6598:hyun4198@cluster0.tuvzlln.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.milmmelier

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('http://www.mangoplate.com/search/%EB%B0%80%ED%81%AC%ED%8B%B0', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')
cafes = soup.select('body > main > article > div.column-wrapper > div > div > section > div.search-list-restaurants-inner-wrap > ul > li')
for cafe in cafes:
    a = cafe.select_one('figure > figcaption > div > a > h2')
    if a is not None:
        title = " ".join(a.text.split())
        star = cafe.select_one('div:nth-child(1) > figure > figcaption > div > strong').text
        address = cafe.select_one('div:nth-child(1) > figure > a > div > img')['alt'].split("-",maxsplit=1)[1]

        headers = {
            "X-NCP-APIGW-API-KEY-ID": "m1qc7sxv4t",
            "X-NCP-APIGW-API-KEY": "utc5druQG9LHR1sV4W18XLDVS562LrTLqVTFLCS4"
        }
        r = requests.get(f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={address}",
                         headers=headers)
        response = r.json()

        if response["status"] == "OK":
            if len(response["addresses"]) > 0:
                x = float(response["addresses"][0]["x"])
                y = float(response["addresses"][0]["y"])
                print(title, address, star, x, y)
                doc = {
                    'star': star,
                    'title': title,
                    'address': address,
                    "mapx": x,
                    "mapy": y}
                db.matjips.insert_one(doc)


            "X-NCP-APIGW-API-KEY-ID": "m1qc7sxv4t",
            "X-NCP-APIGW-API-KEY": "utc5druQG9LHR1sV4W18XLDVS562LrTLqVTFLCS4"
        }
        r = requests.get(f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={address}",
                         headers=headers)
        response = r.json()

        if response["status"] == "OK":
            if len(response["addresses"]) > 0:
                x = float(response["addresses"][0]["x"])
                y = float(response["addresses"][0]["y"])
                print(title, address, star, x, y)
                doc = {
                    'star': star,
                    'title': title,
                    'address': address,
                    "mapx": x,
                    "mapy": y}
                db.matjips.insert_one(doc)

