"""Make a dictionary of recipes
Scrape deliaonline.com
Store recipies in a dictionary of lists arranged by categories

Uses a recursive scraping strategy:

Load a page
If it is the data we are looking for:
    Scrape it and return
Get the number of pages
Loop through the pages:
    Loop through items on page:
        Call itself
"""

import json
import requests
from bs4 import BeautifulSoup


SITE_URL = 'http://deliaonline.com'
# page with categories of dish
CATEGORY_URL = f'{SITE_URL}/recipes/type-of-dish'


def get_soup(url):
    """Get a soup for a url"""
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def get_number_of_pages(soup):
    """Get number of pages from a page """
    # page numbers in following li
    page_numbers = soup.find(class_='pager-current')
    # pages in i element
    try:
        pages = page_numbers.find('i', class_='mobile')
        # number of pages is last characters in text
        pages = pages.text.split()[-1]
    except Exception:
        pages = 1
    print(f'Found {pages} pages')
    return int(pages)


def get_categories(soup):
    """Get categories from a category page"""
    categories = []
    # recipes categories in following div
    results = soup.find(class_='term-listing-content')
    # category url and name in h3 headings
    heads = results.find_all('h3')
    # make list of tuple of categories and urls
    for h in heads:
        categories.append(
            (h.find('a').find(text=True, recursive=False),  # only first text
             h.find('a')['href']))
    return categories


def is_target_data(soup):
    # target page has ingredients class
    # find_all returns a list of found classes
    return soup.find_all(class_='field-name-field-ingredient-groups')


def get_target_data(soup):
    # recipe name
    name = soup.find(class_='recipe-information').find('h1').text
    # ingredients are in a link or text in following div
    results = soup.find(class_='field-name-field-ingredient-groups').find_all(itemprop='recipeIngredient')
    # make list of ingredients
    # might be able to use url with find('a')['href']
    ingredients = [r.text.strip() for r in results]
    return name, ingredients


def recursive_scrape(page):
    """ Recursive scrape function
    Load the page
    If it is the data we are looking for:
        Scrape it and return
    Get the number of pages
    Loop through the pages:
        Loop through items on page:
            Call itself
    """
    print(f'Getting page {page}')
    # get soup of page
    soup = get_soup(page)
    if is_target_data(soup):
        print('Recipe page')
        name, ingredients = get_target_data(soup)
        recipes['name'] = ingredients
        print(name, recipes['name'])
        return
    # get number of pages
    pages = get_number_of_pages(soup)
    # loop through the pages
    for new_page in range(pages):
        categories = get_categories(soup)
        for category in categories:
            recursive_scrape(SITE_URL + category[1])
    return


# recipe has name as key and category list, ingredients, method as entry
# e.g A mixed grill with apricot barbecue glaze:
#   ['barbecue and outdoor food', 'barbecue meat and fish', 'mixed grill']
#   ['6 xxx', '2 large xxx, ...']
#   'Begin by ...'
recipes = {}
recursive_scrape(CATEGORY_URL)
with open('recipes.json', 'w') as f:
    json.dump(recipes, f)
