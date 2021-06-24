#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode, unquote
import ssl

# For part 4 of TP -> cache memoization
cache = {}

def getJSON(page):
    # 2.1
    params = urlencode({
      'action': 'parse',  # TODO: API wiki 1er paramètre action
      'format': 'json',  # TODO: API wiki 2nd paramètre format
      'prop': 'text',  # TODO: API wiki 3eme paramètre prop text or wikitext ? -> to test with print(getJSON)
                        # bien text car sinon on a pas les balises html besoin pour le test 2 avec startwith "<div"
      'redirects': 'true', # Si le paramètre page ou pageid est positionné sur une redirection, la résoudre. -> boolean
      'page': page})
    API = "https://fr.wikipedia.org/w/api.php"  # TODO: API de wiki
    # désactivation de la vérification SSL pour contourner un problème sur le
    # serveur d'évaluation -- ne pas modifier
    gcontext = ssl.SSLContext()
    response = urlopen(API + "?" + params, context=gcontext)
    return response.read().decode('utf-8')


def getRawPage(page):
    # 2.2
    parsed = loads(getJSON(page))
    # print(parsed["parse"])
    try:
        title = parsed["parse"]["title"]  # TODO: remplacer ceci
        content = parsed["parse"]["text"]['*']  # TODO: remplacer ceci
        return title, content
    except KeyError:
        # La page demandée n'existe pas
        return None, None


def getPage(page):
    if page in cache:
        return page, cache[page]
    else:
    # 2.3
        title, content = getRawPage(page)
        if title is None:
            return None, [] # couple(None, [])
        else:
            soup = BeautifulSoup(content, 'html.parser')
            # print(soup)
            # 2.4
            filtered_list = soup.div.find_all("p", recursive=False)
            href_list = []
            # find all link tags in filtered_list and append hyperlinks to href_list
            for entry in filtered_list:
                for link_tag in entry.find_all('a'):
                    link = link_tag.get('href')
                    #print(link)
                    #if link:
                    # 2.5
                    if link.startswith("/wiki/") and "redlink" not in link:
                        ### 2.6
                        # also cut /wiki/ first letters
                        # get all element after # paramter url
                        filtered_link0 = unquote(link[6:]).split("#")[0]
                        # replace underscore with space
                        filtered_link = filtered_link0.replace('_', ' ')
                        if (not filtered_link) or (':' in filtered_link):
                            pass
                        else:
                            href_list.append(filtered_link)
            href_list = list(dict.fromkeys(href_list))
            # 2.7
            max_element = min(10, len(href_list))
            filtered_href_list = href_list[:max_element]
            # print(filtered_href_list)
            cache[title] = filtered_href_list
            return title, filtered_href_list


if __name__ == '__main__':
    # Ce code est exécuté lorsque l'on exécute le fichier
    print("Ça fonctionne!")
    
    # Voici des idées pour tester vos fonctions :
    # print(getJSON("Utilisateur:A3nm/INF344"))
    # print(getJSON("Bonjour"))
    # print(getRawPage("Utilisateur:A3nm/INF344"))
    # print(getPage("Bonjour"))
    # print(getRawPage("Histoire"))

