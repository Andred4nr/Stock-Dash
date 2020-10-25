from bs4 import BeautifulSoup
import requests
import nltk
from datetime import datetime


def targets(symbol):
    try:
        url = 'https://money.cnn.com/quote/forecast/forecast.html?symb=' + symbol
        content = requests.get(url)
        soup = BeautifulSoup(content.text, 'lxml')
        result = soup.find("div", {"class": "wsod_twoCol clearfix"}).find("p").text
        tokens = nltk.word_tokenize(result)
        median = tokens.index('median') + 3
        high = tokens.index('high') + 3
        low = tokens.index('low') + 3

        data = {'low': tokens[low], 'meadian': tokens[median], 'high': tokens[high],
                'date': datetime.date(datetime.now()).strftime("%d-%m-%Y")}

    except:
        data = {'low': 'N/A', 'meadian': 'N/A', 'high': 'N/A',
                'date': datetime.date(datetime.now()).strftime("%d-%m-%Y")}

    finally:
        return data

if __name__ == '__main__':
    print(targets('IBM'))
