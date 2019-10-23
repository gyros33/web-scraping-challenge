#!/usr/bin/env python
# coding: utf-8

# In[77]:


from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    data = {}

    #Mars News
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text


    # # JPL Mars Space Images - Featured Image
    url = "https://www.jpl.nasa.gov"
    url2 = "/spaceimages/?search=&category=Mars"
    browser.visit(url+url2)

    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    featured_image_url = url + soup.find("a", class_="button fancybox")["data-fancybox-href"]

    #Mars Weather
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text


    # # Mars Facts

    url = "https://space-facts.com/mars/"
    browser.visit(url)

    tables = pd.read_html(url)
    mars_df = tables[1].set_index(0).rename(columns={1:"Facts"})
    mars_df.index = mars_df.index.rename("")

    mars_html = mars_df.to_html()

    # # Mars Hemispheres

    url = "https://astrogeology.usgs.gov"
    url2 = "/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url+url2)

    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    divs = soup.find_all("div",class_="description")
    links = [x.a["href"] for x in divs]
    images = []

    for x in links:
        response = requests.get(url+str(x))
        soup2 = BeautifulSoup(response.text, 'lxml')
        images.append(url+str(soup2.find("img",class_="wide-image")["src"]))

    hemisphere_image_urls = [
        {"title": "Cerberus Hemisphere", "img_url": images[0]},
        {"title": "Schiaparelli Hemisphere", "img_url": images[1]},
        {"title": "Syrtis Major Hemisphere", "img_url": images[2]},
        {"title": "Valles Marineris Hemisphere", "img_url": images[3]},
    ]

    data["news_title"] = news_title
    data["news_text"] = news_p
    data["featured_image"] = featured_image_url
    data["mars_weather"] = mars_weather
    data["mars_facts"] = mars_html
    data["mars_hems"] = hemisphere_image_urls

    return data
