import requests
from bs4 import BeautifulSoup
import re

# Initialize search parameters
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Connection": "keep-alive",
}
destination = "paris"
checkIn = "2023-03-16"
checkOut = "2023-03-18"
adultsNum = "2"
roomsNum = "1"
firstParam = "?"
#url = "https://www.booking.com/searchresults.es.html?ss=londres&checkin=2023-02-16&checkout=2023-02-18&group_adults=2&no_rooms=1&order=price"
url = "https://www.booking.com/searchresults.es.html"

# Generate the url
if destination: 
    url += firstParam + "ss=" + destination
    firstParam = "&"

if checkIn: 
    url += firstParam + "checkin=" + checkIn
    firstParam = "&"

if checkOut: 
    url += firstParam + "checkout=" + checkOut
    firstParam = "&"

if adultsNum: 
    url += firstParam + "group_adults=" + adultsNum
    firstParam = "&"

if roomsNum: 
    url += firstParam + "no_rooms=" + roomsNum
    firstParam = "&"

url += firstParam + "order=price"

print(url)

# Search the results and scrap the information
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'lxml')

blocksName = soup.find_all("div", {"class": "fcab3ed991 a23c043802"})
blocksLink = soup.find_all("a", {"data-testid": "title-link"})
blocksAddress = soup.find_all("span", {"data-testid": "address"})
blocksDistanceFromCenter = soup.find_all("span", {"data-testid": "distance"})
blocksPuntuation = soup.find_all("div", {"class": "b5cd09854e d10a6220b4"})
blocksPrice = soup.find_all("span", {"data-testid": "price-and-discounted-price"})

hotels = []

# Extract the important data and save it
for name in blocksName:
    dict = {"name":re.search('>(.*)<', str(name)).group(1)}
    hotels.append(dict)

i = 0
for link in blocksLink:
    hasLink = re.search('href="(.*)" rel=', str(link)).group(1)
    if hasLink:
        hotels[i]["link"] = hasLink
        i += 1

i = 0
for address in blocksAddress:
    hasAddress = re.search('>(.*)<', str(address)).group(1)
    if hasAddress:
        hotels[i]["address"] = hasAddress
        i += 1

i = 0
for distance in blocksDistanceFromCenter:
    hasDistance = re.search('>(.*)<', str(distance)).group(1)
    if hasDistance:
        hotels[i]["distanceFromCenter"] = hasDistance
        i += 1

i = 0
for puntuation in blocksPuntuation:
    hasPuntuation = re.search('>(.*)<', str(puntuation)).group(1)
    if hasPuntuation:
        hotels[i]["puntuation"] = hasPuntuation
        i += 1

i = 0
for price in blocksPrice:
    hasPrice = re.search('>(.*)<', str(price)).group(1).replace("€\xa0", "")
    if hasPrice:
        hotels[i]["price"] = hasPrice
        i += 1



print (hotels)