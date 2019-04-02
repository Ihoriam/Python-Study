from urllib.request import urlopen
from bs4 import BeautifulSoup
# import csv
import re

# get urls of each games
def getMovieUrls(url):
    html = urlopen(url)
    bs = BeautifulSoup(html, 'html.parser')
    movieUrls = []

    for link in bs.findAll('a', {'class': 'btn-tooltip',
                                 'itemprop':'url'}):
        movieUrls.append(link.attrs['href'])
    return movieUrls

def getStat(url):
    html = urlopen(url)
    bs = BeautifulSoup(html, 'html.parser')

    localName = bs.find('h1', {'class': 'name',
                             'itemprop':'name'})
    originName = bs.find('div', {'class': 'origin-name',
                             'itemprop':'alternativeHeadline'})
    rateKinoP = bs.find('span', {'class': 'kinopoisk btn-tooltip icon-kinopoisk'}).findAll('p')
    rateIMDB = bs.find('span', {'class': 'imdb btn-tooltip icon-imdb'}).findAll('p')
    quality = bs.find('div', {'class': 'quality'})
    year =  bs.find('a', {'itemprop': 'copyrightYear'})
    time = bs.find('div', {'class': 'item durarion',
                           'itemprop': 'duration'}).span.next_sibling

    statistic = [localName, originName, rateKinoP[0],rateKinoP[1], rateIMDB[0], rateIMDB[1], quality, year, time]
    statistic = list(map(lambda x: x.getText(), statistic))
    return statistic

def writeToCsv(data, fileName):
    with open(fileName + '.csv', 'a') as fp:
        # writer = csv.writer(fp, delimiter=',')
        # # writer.writerow(["your", "header", "foo"])  # write header
        # writer.writerows(data)
        try:
            fp.write(','.join(data))
            fp.write('\n')
        except Exception as ex:
            print('Oppsy Doopsy')
            print(ex)



def findNextPage(url):
    html = urlopen(url)
    bs = BeautifulSoup(html, 'html.parser')
    nextPage = bs.find('a', {'class': 'next icon-arowRight btn-tooltip'})
    return nextPage.attrs['href']

def startParse(site, numPage):
    dataFile = 'myData'
    for time in range(numPage):
        movieUrls = getMovieUrls(site)
        for page in movieUrls:
            writeToCsv(getStat(page), dataFile)
        site = findNextPage(site)

if __name__ == '__main__':
    site = 'https://filmix.co/films'
    numPage = 2
    startParse(site, numPage)





