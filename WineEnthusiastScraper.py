# This Python file uses the following encoding: utf-8
import requests;
from urllib.request import Request, urlopen;
from bs4 import BeautifulSoup;
import sys;
import re
import threading
import time
import io
import argparse
import timeit

#class WineBottle:
#1    URL,
#2    Year
#3    Description
#4    Rating
#5    Price
#6    Designation
#7    Variety
#8    Appellation
#9    Winery
#10    Size
#11    Category
#12    Importer
#13    Date
#14    Self Rated Status

def write_wine_data(pageNumber):
    #file to write to
    writing_file = io.open("Data/WineData%s.txt" % str(pageNumber), "w", encoding="utf-8")

    list_url = "https://www.winemag.com/?s=&drink_type=wine&pub_date_web=2&page=" + str(pageNumber)

    print(list_url)

    list_request = Request(list_url, headers={'User-Agent': 'Mozilla/5.0'})

    list_webpage = urlopen(list_request).read()

    list_soup = BeautifulSoup(list_webpage, 'html.parser')

    list_results = list_soup.find_all("li", {"class": "review-item"})

    count = 0
    for list_result in list_results:
        #list of bottle details
        bottle_details_list = list()

        bottle_url = list_result.find('a')['href']
        bottle_details_list.insert(0, bottle_url)
        #print("Link: %s" % (bottle_url))

        bottle_request = Request(bottle_url, headers={'User-Agent': 'Mozilla/5.0'})
        bottle_webpage = urlopen(bottle_request).read()
        bottle_soup = BeautifulSoup(bottle_webpage, 'html.parser')

        bottle_year = re.search('\d\d\d\d', str(bottle_soup.find_all('div', {"class": "header__title"})[0].find_all('h1')[0]))
        if(str(bottle_year)!='None'):
            bottle_details_list.insert(0, bottle_year.group(0))
        else:
            bottle_details_list.insert(0, "")

        bottle_review = re.search('(?<=(\"description\"\>))((\S| |\n)+)(?=(\<span))', str(bottle_soup.find_all('p', {"class": "description"})[0]))
        if(str(bottle_review)!='None'):
            bottle_details_list.insert(0, bottle_review.group(0).strip())
        else:
            bottle_details_list.insert(0, "")

        bottle_informations = bottle_soup.find_all('div', {"class": "medium-8 large-push-1 columns info-section"})[0].find_all('li', {"class":"row"})
        for info in bottle_informations:
            spans = info.find_all('span')
            general = re.search('(?<=(\>))((\w+| |\,|\/|\$|\"|\.|\'|\n|\%|\-|\=|\!|\*|\&|\;|\:|\–|\xa0)+)(?=(\<))', str(spans[1]))
            if(str(general)!='None'):
                bottle_details_list.insert(0, general.group(0))
        if len(bottle_details_list)==13:
            bottle_details_list.insert(8, "")
        writing_file.write("\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\"\n" % (
            bottle_details_list.pop(), bottle_details_list.pop(), bottle_details_list.pop(),
            bottle_details_list.pop(), bottle_details_list.pop(), bottle_details_list.pop(),
            bottle_details_list.pop(), bottle_details_list.pop(), bottle_details_list.pop(),
            bottle_details_list.pop(), bottle_details_list.pop(), bottle_details_list.pop(),
                bottle_details_list.pop(), bottle_details_list.pop()))

        count = count+1
        print("Writing Page %d, #%d..." % (pageNumber, count))

    writing_file.close()
    print("Page %s finished at: %s" % (pageNumber, time.ctime(time.time())))

parser = argparse.ArgumentParser()
parser.add_argument("first", type=int, help="first page to scrape")
parser.add_argument("last", type=int, help="last page to scrape")
args = parser.parse_args()

start = timeit.default_timer()

for x in range(int(args.first), int(args.last)+1):
    write_wine_data(x)

#Your statements here

stop = timeit.default_timer()

print("Data collection complete for pages %d-%d finished in: %d seconds." % (args.first, args.last, stop - start))