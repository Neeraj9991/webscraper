from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np


# Functions to extract Product Title
def get_title(page):
    try:
        title = page.find("span", attrs={'id': 'productTitle'})

        title_value = title.text.strip()

    except AttributeError:
        title_value = ""

    return title_value


# Functions to extract Product Price
def get_price(page):
    try:
        price = page.find("div", attrs={'class': 'a-section a-spacing-none aok-align-center'})
        price = price.find('span', attrs={'class': 'a-offscreen'}).text

    except AttributeError:
        price = ""

    return price


# Functions to extract Product Rating
def get_rating(page):
    try:
        rating = page.find("span", attrs={'class': 'a-icon-alt'})

        rating_value = rating.text.strip()

    except AttributeError:
        rating_value = ""

    return rating_value


# Functions to extract Number of user reviews
def get_reviews(page):
    try:
        review_count = page.find("span", attrs={'id': 'acrCustomerReviewText'}).text.strip()

    except AttributeError:
        review_count = ""

    return review_count


# Functions to extract Product Title
def get_availability(page):
    try:
        available = page.find("div", attrs={'id': 'availability'})

        available = available.find("span").text.strip()

    except AttributeError:
        available = ""

    return available


if __name__ == '__main__':

    # Headers for request 
    HEADERS = ({
        'User-Agent': '', # add your user agent
        'Accept-Language': 'en-US, en;q=0.5'
    })

    # Webpage URL
    URL = 'https://www.amazon.in/s?k=mobile&ref=nb_sb_noss_1'

    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Soup object containing all data
    soup = BeautifulSoup(webpage.content, 'html.parser')

    # Fetch links as List of Tag Objects
    links = soup.find_all('a', attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

    links_list = []

    # loop for extracting links from Tag Objects
    for link in links:
        links_list.append(link.get('href'))

    d = {
        'title': [],
        'price': [],
        'rating': [],
        'reviews': [],
        'availability': []
    }

    # Loop for extracting product detail from each ink
    for link in links_list:
        new_webpage = requests.get('https://www.amazon.in' + link, headers=HEADERS)

        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        # Function calls to display all necessary product information
        d['title'].append((get_title(new_soup)))
        d['price'].append((get_price(new_soup)))
        d['rating'].append((get_rating(new_soup)))
        d['reviews'].append((get_reviews(new_soup)))
        d['availability'].append((get_availability(new_soup)))

    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'].replace('', np.NAN, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])
    amazon_df.to_csv('amazon_data.csv', header=True, index=False)
