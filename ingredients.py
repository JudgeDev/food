"""Make a dictionary of ingredients
Scrape food.ndtv.com
Store ingredients in a dictionary of lists arranged by categories
"""

import json
import requests
from bs4 import BeautifulSoup

URL = 'http://food.ndtv.com/ingredient'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

categories = []

# ingredient categories in following div
results = soup.find(id ='video_listing')
# category url and name in h3 headings
heads = results.find_all('h3')

# make list of tuple of categories and urls
for h in heads:
    categories.append(
        (h.find(itemprop='name').text,
         h.find('a')['href']))

# ingedients is a dictionary of categories
ingredients = {c[0]: [] for c in categories}

# get category pages
for c in categories:
    print(c[0])
    # get first page
    page = requests.get(c[1])
    soup = BeautifulSoup(page.content, 'html.parser')
    # page numbers in following div
    results = soup.find(id='inside_pagination')
    # pages in span elements
    try:
        pages = results.find_all('span', class_='pagination')
        # count number of page numbers from text of links
        pages = len([p.find('a').text for p in pages])
    except:
        pages = 1

    for page in range(pages):
        print(f'Getting page {page + 1}')
        try:
            page = requests.get(f'{c[1]}/page-{page+1}')
        except:
            print(f'Last page of category {c[0]}')
            break

        soup = BeautifulSoup(page.content, 'html.parser')

        # ingredients in following div
        results = soup.find(id ='video_listing')
        # ingredient url and name in h3 headings
        heads = results.find_all('h3')

        # make list of ingredients
        # urls would be in h.find('a')['href']
        for h in heads:
            ingredients[c[0]].append(h.find(itemprop='name').text)

with open('ingredients.json', 'w') as f:
    json.dump(ingredients, f)

print(ingredients)